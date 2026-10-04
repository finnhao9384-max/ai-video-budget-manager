"""Independent offline budget checker; not invoked by the TapNow Skill.

Reads explicit tasks and a versioned price catalog, validates supported settings,
and recomputes scenario costs. It does not interpret scripts, allocate retries,
generate media, validate asset ownership, or verify live prices and settlement.
"""
import argparse
from datetime import date
from decimal import Decimal
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / 'data/pricing/tapnow-2026-09-26.json'


def positive_integer(value, label):
    if type(value) is not int or value < 1:
        raise ValueError(f'{label} must be a positive integer')
    return value


def unique_id(value, seen):
    if not isinstance(value, str) or not value.strip() or value in seen:
        raise ValueError('Task and asset IDs must be nonempty and unique')
    seen.add(value)


def calculate(plan, catalog):
    """Return reproducible priced subtotals; reject unknown or ambiguous settings."""
    when = date.fromisoformat(plan['pricing_date'])
    image_total = video_total = image_first = video_first = 0
    details, seen = [], set()
    for item in plan.get('images', []):
        unique_id(item['asset_id'], seen)
        quantity = positive_integer(item['quantity'], 'Image quantity')
        attempts = positive_integer(item['attempts'], 'Image attempts')
        if item.get('existing', False):
            raise ValueError('List only new charged tasks; omit existing assets from this checker')
        keys = ('model', 'mode', 'resolution', 'detail', 'web_search')
        matches = [row for row in catalog['images']
                   if all(item.get(k) == row.get(k) for k in keys)]
        if len(matches) != 1:
            raise ValueError(f'Unknown or ambiguous image configuration: {item["asset_id"]}')
        row = matches[0]
        if 'promotion_ends' in row and when >= date.fromisoformat(row['promotion_ends'][:10]):
            raise ValueError('Promotion expired or at an unverified timezone boundary')
        base = quantity * row['credits']
        image_first += base
        image_total += base * attempts
        details.append({'id':item['asset_id'], 'first_pass':base,
                        'attempts':attempts, 'scenario':base * attempts})
    for item in plan.get('videos', []):
        unique_id(item['task_id'], seen)
        duration = positive_integer(item['duration_seconds'], 'Generated seconds')
        attempts = positive_integer(item['attempts'], 'Video attempts')
        matches = [row for row in catalog['videos']
                   if all(item[k] == row[k] for k in ('model','mode','resolution'))]
        if len(matches) != 1:
            raise ValueError(f'Unknown or ambiguous video configuration: {item["task_id"]}')
        row = matches[0]
        if not row['min_seconds'] <= duration <= row['max_seconds']:
            raise ValueError(f'Unsupported generated duration: {item["task_id"]}')
        base = duration * row['credits_per_second']
        video_first += base
        video_total += base * attempts
        details.append({'id':item['task_id'], 'first_pass':base,
                        'attempts':attempts, 'scenario':base * attempts})
    if not details:
        raise ValueError('At least one priced task is required')
    total = image_total + video_total
    result = {'catalog_version':catalog['version'], 'unit':catalog['unit'],
              'image_credits':image_total, 'video_credits':video_total,
              'first_pass_credits':image_first + video_first,
              'scenario_credits':total, 'details':details,
              'scope':'Quoted generation tasks only; unknown fees excluded.'}
    if plan.get('budget') is not None:
        if isinstance(plan['budget'], bool):
            raise ValueError('Budget must be numeric, not boolean')
        budget = Decimal(str(plan['budget']))
        if not budget.is_finite() or budget < 0:
            raise ValueError('Budget must be finite and nonnegative')
        result['within_quoted_budget'] = Decimal(total) <= budget
        result['remaining_credits'] = str(budget - total)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        result = calculate(json.loads(args.plan.read_text()),
                           json.loads(args.catalog.read_text()))
    except (ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'Invalid plan: {exc}\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
