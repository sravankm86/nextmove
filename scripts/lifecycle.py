"""Seven workflow states; reasons, confirmations and attempts are separate facts."""
STATUSES = ['Inventoried', 'Queued', 'Ready', 'Applied', 'Interviewing', 'Not pursuing', 'Rejected']
END_STATES = {'Interviewing', 'Not pursuing', 'Rejected'}
LEGACY = {'Needs review': 'Inventoried', 'Needs eligibility': 'Inventoried',
          'Confirmed': 'Applied', 'In process': 'Interviewing',
          'Not aligned': 'Not pursuing', 'Not a fit': 'Not pursuing',
          'Withdrawn': 'Not pursuing', 'Closed': 'Not pursuing', 'Duplicate': 'Not pursuing',
          'Offer': 'Interviewing', 'Accepted': 'Interviewing'}


def normalize(value, *, review_approved=False, last_verified_stage=None):
    """Read legacy labels without manufacturing acceptance or submission success.

    Callers preserve original values and evidence before any persisted migration.
    Uncertainty always requires durable attempt reconciliation, regardless of label.
    """
    if value in STATUSES:
        return value
    if value == 'Shortlisted':
        return 'Queued' if review_approved is True else 'Inventoried'
    if value == 'Submission uncertain':
        return last_verified_stage if last_verified_stage in {'Inventoried', 'Queued', 'Ready'} else 'Inventoried'
    return LEGACY.get(value)
