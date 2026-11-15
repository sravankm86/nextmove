import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import tracker_values as v


class TrackerValuesTests(unittest.TestCase):
    def test_structured_equity_is_not_salary(self):
        comp = {'components': [
            {'compensationType': 'EquityCashValue', 'currencyCode': 'USD', 'minValue': 10000, 'maxValue': 90000},
            {'compensationType': 'Salary', 'currencyCode': 'USD', 'minValue': 260000, 'maxValue': 340000, 'interval': '1 YEAR'}]}
        self.assertEqual(v.salary_ranges(comp), ['USD 260,000–340,000'])

    def test_location_bands_keep_currency_and_do_not_make_envelope(self):
        result = v.compact_salary('Base $260,000 USD - $340,000 USD; Canada $180,000 CAD and $230,000 CAD')
        self.assertEqual(result, 'USD 260,000–340,000; CAD 180,000–230,000')

    def test_yearly_rates_and_and_separator(self):
        self.assertEqual(v.salary_ranges('USD $190,000 per year - USD $211,000 per year'), ['USD 190,000–211,000'])
        self.assertEqual(v.salary_ranges('between £150K and £315K'), ['£150,000–315,000'])

    def test_metrics_are_not_pay(self):
        self.assertEqual(v.salary_ranges('Manage 1,000–2,000 customers; experience 2020–2025'), [])
        self.assertEqual(v.salary_ranges('Equity grants of $10,000–$30,000', description=True), [])
        self.assertEqual(v.salary_ranges('Manage payments for a range of customers with $1M–$10M revenue.', description=True), [])

    def test_optional_equity_and_pay_equity_are_distinct(self):
        self.assertEqual(v.additional_compensation('We support pay equity and equal opportunity.'), ['Not stated'])
        self.assertEqual(v.additional_compensation('May receive equity grants and an annual bonus.'), ['Equity', 'Bonus'])
        self.assertEqual(v.additional_compensation('Eligible for annual bonus OR commission.'), ['Bonus or commission'])

    def test_addresses_and_placeholders_do_not_become_location_labels(self):
        source = {'city': 'Berlin', 'country': 'DE', 'street_name': 'Example Street', 'arrival_instructions': 'Call reception'}
        self.assertEqual(v.locations(source), ['Berlin, Germany'])
        self.assertEqual(v.locations('3 Locations'), [])
        self.assertEqual(v.locations([{'address': {'addressLocality': 'Boston', 'addressCountry': 'US'}}]), ['Boston, United States'])


if __name__ == '__main__':
    unittest.main()
