import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from company_policy import funding_qualifies, scan_enabled

class CompanyPolicyTests(unittest.TestCase):
    def test_funding_needs_user_minimum_and_verified_maturity(self):
        self.assertTrue(funding_qualifies('Series C', 'Series B'))
        self.assertTrue(funding_qualifies('Public', 'Series B'))
        self.assertFalse(funding_qualifies('Series A', 'Series B'))
        self.assertFalse(funding_qualifies('Unknown', 'Series B'))
        self.assertFalse(funding_qualifies('Series C', 'Unknown'))
        with self.assertRaises(ValueError):funding_qualifies('Public', None)
        with self.assertRaises(TypeError):funding_qualifies('Public')

    def test_minimal_targeting_has_no_submission_policy_dependency(self):
        self.assertTrue(scan_enabled({'Search status':'Allow'}))
        for status in ['Proposed','Exclude',None]:
            self.assertFalse(scan_enabled({'Search status':status}))
        self.assertFalse(scan_enabled({'Search status':'Allow','Application hold status':'Blocked (permanent)'}))
        self.assertTrue(scan_enabled({'Search status':'Allow','Application hold status':'Held'}))

if __name__=='__main__':unittest.main()
