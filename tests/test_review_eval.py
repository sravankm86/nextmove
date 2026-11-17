import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from review_eval import outcome, score


class ReviewEvalTest(unittest.TestCase):
    def test_outcomes(self):
        self.assertEqual(outcome('Pursue', 'Queued'), 'agree')
        self.assertEqual(outcome('Not pursuing', 'Not pursuing'), 'agree')
        self.assertEqual(outcome('Not pursuing', 'Queued'), 'false_queue')
        self.assertEqual(outcome('Pursue', 'Not pursuing'), 'missed')
        self.assertEqual(outcome('Pursue', 'Need review'), 'deferred')
        with self.assertRaises(ValueError):
            outcome('Maybe', 'Queued')

    def test_score_filters_inactive_and_split(self):
        rows = [
            {'verdict': 'Pursue', 'prediction': 'Queued', 'split': 'Train'},
            {'verdict': 'Not pursuing', 'prediction': 'Queued', 'split': 'Holdout'},
            {'verdict': 'Pursue', 'prediction': 'Need review', 'split': 'Train', 'active': False},
        ]
        self.assertEqual(score(rows)['status_match'], 0.5)
        self.assertEqual(score(rows, 'Holdout')['false_queue'], 1)
        self.assertIsNone(score([])['status_match'])


if __name__ == '__main__':
    unittest.main()
