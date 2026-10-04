"""Offline checks for budget arithmetic and invalid planning configurations.

These test the independent checker, not TapNow's LLM or actual billing.
"""
import copy
import json
from pathlib import Path
import unittest
from tools.check_budget import calculate

ROOT = Path(__file__).resolve().parents[1]


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.catalog = json.loads((ROOT/'data/pricing/tapnow-2026-09-26.json').read_text())
        self.plan = json.loads((ROOT/'data/examples/commercial-medium-plan.json').read_text())

    def test_commercial_medium_reconciles(self):
        r = calculate(self.plan, self.catalog)
        self.assertEqual((r['image_credits'],r['video_credits'],r['scenario_credits']),
                         (975,4320,5295))
        self.assertEqual(r['first_pass_credits'],1059)

    def test_budget_boundaries(self):
        for budget,expected in [(5294,False),(5295,True),(5296,True)]:
            self.plan['budget']=budget
            self.assertEqual(calculate(self.plan,self.catalog)['within_quoted_budget'],expected)

    def test_duplicate_asset_rejected(self):
        self.plan['images'].append(copy.deepcopy(self.plan['images'][0]))
        with self.assertRaises(ValueError): calculate(self.plan,self.catalog)

    def test_unknown_price_rejected(self):
        self.plan['images'][0]['resolution']='8K'
        with self.assertRaises(ValueError): calculate(self.plan,self.catalog)

    def test_reference_price_differs_for_gpt(self):
        self.plan['videos']=[]
        self.plan['images']=[dict(asset_id='I01',quantity=1,attempts=1,
            model='GPT Image 2.5 Flare',mode='Text-to-image',resolution='1K',detail='Low',web_search=None)]
        self.assertEqual(calculate(self.plan,self.catalog)['scenario_credits'],3)
        self.plan['images'][0]['mode']='Reference'
        self.assertEqual(calculate(self.plan,self.catalog)['scenario_credits'],18)

    def test_model_change_requires_duration_recheck(self):
        self.plan['videos'][0]['model']='MiniMax H3 Max'
        self.plan['videos'][0]['resolution']='768P'
        with self.assertRaises(ValueError): calculate(self.plan,self.catalog)
        self.plan['videos'][0]['duration_seconds']=5
        self.assertEqual(calculate(self.plan,self.catalog)['video_credits'],4290)

    def test_too_long_and_fractional_durations(self):
        for duration in [16,4.5,True]:
            self.plan['videos'][0]['duration_seconds']=duration
            with self.assertRaises(ValueError): calculate(self.plan,self.catalog)

    def test_nonpositive_attempts_rejected(self):
        for attempts in [0,-1,1.5,True]:
            self.plan['images'][0]['attempts']=attempts
            with self.assertRaises(ValueError): calculate(self.plan,self.catalog)

    def test_promotion_boundary(self):
        self.plan['videos']=[]
        self.plan['images']=[dict(asset_id='I01',quantity=1,attempts=1,
            model='Seedream 5.0 Pro',mode='Reference',resolution='1K',detail=None,web_search=None)]
        self.plan['pricing_date']='2026-10-06'
        self.assertEqual(calculate(self.plan,self.catalog)['scenario_credits'],3)
        for day in ['2026-10-07','2026-10-08']:
            self.plan['pricing_date']=day
            with self.assertRaises(ValueError): calculate(self.plan,self.catalog)

    def test_invalid_budget(self):
        for budget in [-1,'NaN','Infinity',True]:
            self.plan['budget']=budget
            with self.assertRaises(ValueError): calculate(self.plan,self.catalog)


if __name__ == '__main__': unittest.main()
