"""Compact display values. Source evidence remains authoritative for Review."""
import ast
import html
import json
import math
import re


def text(value):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', ' ', str(value or '')))).strip()


def decoded(value):
    if not isinstance(value, str):
        return value
    if value.strip().startswith(('{', '[')):
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                pass
    return value


def unique(values):
    return list(dict.fromkeys(x for x in values if x))


def amount(value):
    value = str(value).replace(',', '').replace(' ', '')
    scale = 1000 if value.lower().endswith('k') else 1000000 if value.lower().endswith('m') else 1
    number = float(value.rstrip('kKmM')) * scale
    return f'{number:,.2f}'.rstrip('0').rstrip('.') if number % 1 else f'{int(number):,}'


CODE = r'(?:USD|GBP|EUR|CAD|AUD|INR|PLN|JPY|SGD|CHF|ILS|SEK|NOK|CZK|BRL|AED)'
MONEY = rf'(?:{CODE}\s*[$£€₹]?|US\$|CA\$|A\$|[$£€₹])'
NUM = r'\d[\d,]*(?:\.\d+)?\s*[kKmM]?'
RANGE = re.compile(rf'(?P<c>{MONEY})\s*(?P<lo>{NUM})\s*(?P<lc>{CODE})?\s*(?:per\s+(?:year|annum|hour|month))?\s*(?:-|–|—|\bto\b|\band\b)\s*(?P<hc>{MONEY})?\s*(?P<hi>{NUM})\s*(?P<tc>{CODE})?(?!\d)', re.I)
SUFFIX_RANGE = re.compile(rf'(?P<lo>{NUM})\s*(?:-|–|—|\bto\b|\band\b)\s*(?P<hi>{NUM})\s*(?P<c>{CODE})\b', re.I)


def salary_ranges(value, *, description=False):
    """Keep separate advertised bands; never create an envelope or convert currency."""
    value = decoded(value)
    if isinstance(value, list):
        return unique([s for v in value for s in salary_ranges(v, description=description)])
    if isinstance(value, dict):
        kind = value.get('compensationType', '')
        if kind and kind != 'Salary':
            return []
        if kind == 'Salary' and value.get('minValue') is not None and value.get('maxValue') is not None:
            unit = value.get('interval', '')
            suffix = '/h' if 'HOUR' in unit.upper() else '/mo' if 'MONTH' in unit.upper() else ''
            currency = value.get('currencyCode') or ''
            return [f'{currency} {amount(value["minValue"])}–{amount(value["maxValue"])}{suffix}'.strip()]
        # Only actual compensation/advertised-range structures, never raw job IDs/metrics.
        keys = ['compensation', 'components', 'summaryComponents', 'compensationTiers', 'salary_data', 'compensation_evidence']
        found = [s for k in keys if k in value for s in salary_ranges(value[k])]
        if found:
            return unique(found)
        for k in ['scrapeableCompensationSalarySummary', 'compensationTierSummary', 'posted_salary', 'quoted_range_contexts']:
            if value.get(k):
                found += salary_ranges(value[k])
        return unique(found)
    content = text(value)
    found = []
    spans = []
    for m in list(RANGE.finditer(content)) + list(SUFFIX_RANGE.finditer(content)):
        if any(a <= m.start() < b for a,b in spans):
            continue
        prior = content[max(0, m.start()-130):m.start()].lower()
        if description and not re.search(r'\b(?:salary|pay|compensation)\b', prior):
            continue
        if re.search(r'(?:equity|stock|bonus|on.target earnings|\bote\b)[^.;]{0,55}$', prior) and not re.search(r'(?:base|salary)[^.;]{0,40}$', prior):
            continue
        codes = [c.upper() for c in re.findall(CODE, ' '.join(str(m.groupdict().get(k)or'')for k in ['c','lc','hc','tc']), re.I)]
        if len(set(codes)) > 1:
            continue
        code = codes[0] if codes else m['c']
        try:
            lo, hi = amount(m['lo']), amount(m['hi'])
        except ValueError:
            continue
        following = content[m.end():m.end()+35].lower()
        suffix = '/h' if re.search(r'per hour|/hour|/hr|hourly', following) else '/mo' if re.search(r'per month|/month|monthly', following) else ''
        found.append(f'{code}{" " if code.isalpha() else ""}{lo}–{hi}{suffix}')
        spans.append(m.span())
    return unique(found)


def compact_salary(*values):
    ranges = unique([s for v in values for s in salary_ranges(v)])
    # A source may repeat the same band with a symbol and an explicit currency.
    specific = {re.sub(r'^[^\d]+', '', s) for s in ranges if re.match(CODE, s, re.I)}
    return '; '.join(s for s in ranges if not s.startswith('$') or re.sub(r'^[^\d]+', '', s) not in specific)


def salary_endpoints(bands, *, currency, period='year', basis='base'):
    """Select one verified advertised band, never an envelope or FX conversion.

    Callers verify posting identity, units, basis and band conditions from the
    official source. Selection is the highest advertised maximum in the chosen
    display currency; Review must still check location/level applicability.
    All source bands and conditions remain in evidence. Equal maxima retain
    source order. Unknown or incompatible values return two missing values.
    """
    valid = []
    for band in bands:
        if (band.get('currency'), band.get('period'), band.get('basis')) != (currency, period, basis):
            continue
        lo, hi = band.get('minimum'), band.get('maximum')
        if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in (lo, hi)):
            continue
        if 0 < lo <= hi:
            valid.append(band)
    if not valid:
        return None, None
    selected = max(valid, key=lambda band: band['maximum'])
    return selected['minimum'], selected['maximum']


def additional_compensation(*values):
    content = ' '.join(text(json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for v in values)
    labels = []
    # Pay-equity and equal-opportunity language are not grants.
    if re.search(r'offers equity|equity(?:cashvalue|percentage)|stock options|restricted stock|\brsus?\b|equity (?:awards|grants|compensation|packages)|(?:eligible|eligibility).{0,65}equity|(?:receive|include|offers?).{0,65}equity', content, re.I):
        labels.append('Equity')
    if re.search(r'(?:eligible|eligibility|receive|include|offers?|potential|annual|performance|sign.on|incentive).{0,65}\bbonus(?:es)?\b|\bbonus (?:potential|eligibility|plan|program|incentive|opportunit)', content, re.I):
        labels.append('Bonus')
    if re.search(r'(?:eligible for|receive|earn).{0,25}commissions?\b|commission (?:plan|rate|target)\s*[:\d]', content, re.I):
        labels.append('Commission')
    if re.search(r'bonus\s+or\s+commission', content, re.I):
        labels = [x for x in labels if x not in ['Bonus','Commission']] + ['Bonus or commission']
    return labels or ['Not stated']


COUNTRY = {'US':'United States', 'USA':'United States', 'us':'United States', 'IL':'Israel', 'GB':'United Kingdom', 'UK':'United Kingdom', 'CA':'Canada', 'DE':'Germany', 'FR':'France', 'NL':'Netherlands', 'IN':'India', 'IE':'Ireland', 'United States of America':'United States'}


def locations(value):
    value = decoded(value)
    if isinstance(value, list):
        return unique([s for v in value for s in locations(v)])
    if isinstance(value, dict):
        if 'address' in value and isinstance(value['address'], dict):
            return locations(value['address'])
        city = value.get('city') or value.get('addressLocality')
        region = value.get('state') or value.get('region') or value.get('addressRegion')
        country = value.get('country') or value.get('addressCountry')
        if isinstance(country, dict):
            country = country.get('name') or country.get('value')
        parts = unique([text(city), text(region) if not city else '', COUNTRY.get(text(country), text(country))])
        return [', '.join(parts)] if parts else locations(value.get('fullLocation') or value.get('name') or value.get('location'))
    content = text(value)
    if not content or content.lower() in ['unknown', 'not disclosed', 'none', 'null', 'not provided'] or re.fullmatch(r'\d+\s+locations?', content, re.I):
        return []
    # Some legacy fields contain a Python list after a primary location.
    if '[' in content:
        head, tail = content.split('[', 1)
        try:
            return unique(locations(head.rstrip('; ')) + locations(ast.literal_eval('['+tail)))
        except (ValueError, SyntaxError):
            pass
    result = []
    for part in re.split(r'\s*;\s*|\s*\|\s*|\n', content):
        part = re.sub(r'^(?:Office\s*-\s*|Remote\s*[-–]\s*|Hybrid\s*[-–]\s*)', '', part, flags=re.I)
        part = re.sub(r'\bUnited States of America\b', 'United States', part)
        part = re.sub(r'\b(?:USA|U\.S\.|us)\b', 'United States', part)
        part = re.sub(r'\s+', ' ', part).strip(' ,;-')
        if part.lower() in ['remote', 'hybrid', 'on-site', 'onsite']:
            continue
        if part:
            result.append(part)
    return unique(result)


def availability(value):
    value = text(value).lower()
    return 'Open' if value.startswith('open') else 'Closed' if value.startswith('closed') else 'Unknown'


def description_status(value):
    value = text(value).lower()
    if 'current' in value and any(x in value for x in ['verified', 'captured', 'retrieved']):
        return 'Current'
    if any(x in value for x in ['missing', 'not captured', 'not retrieved', 'must retrieve', 'gap']):
        return 'Missing'
    if value in ['retrieved', 'captured'] or 'full official description captured' in value:
        return 'Captured'
    if 'historical' in value or 'provenance' in value:
        return 'Historical'
    return 'Unavailable' if 'unavailable' in value else 'Missing'
