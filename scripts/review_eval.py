"""Score Review predictions against the Review eval answer key (DATA.md "Review eval")."""

VERDICTS = ('Pursue', 'Not pursuing')
REASON_TYPES = ('Pay', 'Location', 'Seniority', 'Company', 'Work type', 'Domain', 'Specialist gap',
                'Technical background', 'Consumer', 'Internal tools', 'Language', 'Excluded company',
                'Strong match', 'Other')
SPLITS = ('Train', 'Holdout')
PREDICTIONS = ('Queued', 'Need review', 'Not pursuing')

# Need review is a deferral: it neither agrees nor disagrees with the answer key.
_AGREE = {('Pursue', 'Queued'), ('Not pursuing', 'Not pursuing')}


def outcome(verdict, prediction):
    if verdict not in VERDICTS:
        raise ValueError(f'unknown verdict: {verdict!r}')
    if prediction not in PREDICTIONS:
        raise ValueError(f'unknown prediction: {prediction!r}')
    if prediction == 'Need review':
        return 'deferred'
    if (verdict, prediction) in _AGREE:
        return 'agree'
    return 'false_queue' if prediction == 'Queued' else 'missed'


def score(rows, split=None):
    """rows: dicts with verdict, prediction, split, active. Returns counts and status-match rate."""
    picked = [r for r in rows if r.get('active', True) and (split is None or r.get('split') == split)]
    counts = {'agree': 0, 'false_queue': 0, 'missed': 0, 'deferred': 0}
    for r in picked:
        counts[outcome(r['verdict'], r['prediction'])] += 1
    total = len(picked)
    return {'total': total, **counts, 'status_match': (counts['agree'] / total) if total else None}
