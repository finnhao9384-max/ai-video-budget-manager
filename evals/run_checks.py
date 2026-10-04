"""Recompute selected transcript claims without changing the original evidence.

Inputs are manually extracted arithmetic terms plus retained transcript rows.
Results measure selected calculation consistency, not global Skill reliability.
Writes results/calculation-checks.json; never calls a model or paid service.
"""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    cases = json.loads((ROOT/'evals/test_cases.json').read_text())['cases']
    results = []
    for case in cases:
        total = sum(q*p*a for q,p,a in case['image_terms']+case['video_terms'])
        source = (ROOT/'data/transcripts'/case['transcript']).read_text()
        present = f'{case["reported_total"]:,}' in source
        results.append({'id':case['id'],'calculated':total,
                        'reported':case['reported_total'],
                        'reported_number_found':present,
                        'pass':total==case['reported_total'] and present})
    # Independent check of the retained AURA follow-up detail rows.
    aura = (ROOT/'data/transcripts/aura.md').read_text()
    section = aura.split('Cost explanation (Candidate A detail)',1)[1].split('Operating sequence',1)[0]
    detail_total = 0
    reported = None
    for line in section.splitlines():
        if not line.startswith('|'): continue
        cells = [x.strip() for x in line.strip('|').split('|')]
        if len(cells)!=5 or not cells[-1].replace(',','').isdigit(): continue
        amount = int(cells[-1].replace(',',''))
        if cells[0]=='Total': reported=amount
        else: detail_total += amount
    assert reported is not None
    # Independently sum the Right Frequency shot table, not its aggregate text.
    frequency = (ROOT/'data/transcripts/right-frequency.md').read_text()
    shots=[]
    for line in frequency.splitlines():
        if re.match(r'\| S\d{2} \|',line):
            cells=[x.strip() for x in line.strip('|').split('|')]
            shots.append((int(cells[2]),int(cells[3])))
    output = {
        'method':'Offline deterministic checks of selected creator-supplied transcript claims.',
        'tier_totals':results,
        'tier_totals_passed':sum(x['pass'] for x in results),
        'tier_totals_scored':len(results),
        'aura_detail_reconciliation':{'sum_of_listed_subtotals':detail_total,
            'reported_total':reported,'pass':detail_total==reported,
            'finding':'One text-to-image entry is absent from the detail table.'},
        'right_frequency_shot_aggregates':{'shots':len(shots),
            'edit_seconds':sum(x[0] for x in shots),
            'generated_seconds':sum(x[1] for x in shots),
            'five_second_minimum_seconds':sum(max(5,x[0]) for x in shots)},
        'limits':'Selected calculations only; no live Agent calls, independent billing verification or full semantic scoring.'}
    target = ROOT/'evals/results/calculation-checks.json'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
    # A documented Agent failure is a finding, not a failure to run this audit.
    if not all(x['pass'] for x in results): raise SystemExit(1)


if __name__=='__main__': main()
