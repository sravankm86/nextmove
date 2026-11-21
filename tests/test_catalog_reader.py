import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from catalog_reader import enumerate_catalog

class CatalogReaderTests(unittest.TestCase):
    def test_complete_nonpaginated_and_empty_feeds(self):
        for provider in ['greenhouse','ashby']:
            self.assertEqual(enumerate_catalog(provider,lambda o:{'jobs':[]})['observed_count'],0)
        x=enumerate_catalog('greenhouse',lambda o:{'jobs':[{'id':1}],'meta':{'total':1}})
        self.assertTrue(x['end_verified']);self.assertEqual(x['pages_read'],1)
        with self.assertRaises(ValueError):enumerate_catalog('greenhouse',lambda o:{'jobs':[{'id':1}],'meta':{'total':2}})

    def test_lever_follows_actual_count_until_empty_even_when_capped(self):
        calls=[]
        def page(offset):
            calls.append(offset);return {0:[{'id':'a'}],1:[{'id':'b'}],2:[]}[offset]
        x=enumerate_catalog('lever',page)
        self.assertEqual(calls,[0,1,2]);self.assertEqual(x['observed_count'],2)
        self.assertEqual(x['end_basis'],'terminal empty page')

    def test_errors_and_repeated_pages_never_claim_completion(self):
        with self.assertRaises(ValueError):enumerate_catalog('ashby',lambda o:{'error':'Not found'})
        with self.assertRaises(ValueError):enumerate_catalog('lever',lambda o:[{'id':'same'}])
        with self.assertRaises(ValueError):enumerate_catalog('greenhouse',lambda o:{'jobs':[{}]})
        with self.assertRaises(ValueError):enumerate_catalog('ashby',lambda o:{'jobs':'bad'})

if __name__=='__main__':unittest.main()
