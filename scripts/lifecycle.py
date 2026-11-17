"""Nine workflow states; confirmations and submission attempts remain evidence."""
STATUSES = ['Inventoried', 'Needs attention', 'Queued', 'Ready', 'Applied', 'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate']
END_STATES = {'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate'}
LEGACY = {'Need review': 'Needs attention', 'Needs review': 'Needs attention', 'Needs eligibility': 'Needs attention',
          'Confirmed': 'Applied', 'In process': 'Interviewing',
          'Not aligned': 'Not pursuing', 'Not a fit': 'Not pursuing',
          'Withdrawn': 'Not pursuing', 'Closed': 'Not pursuing',
          'Offer': 'Interviewing', 'Accepted': 'Interviewing'}


def normalize(value, *, review_approved=False, last_verified_stage=None):
    """Preserve original evidence before any persisted legacy-label migration."""
    if value in STATUSES:
        return value
    if value == 'Shortlisted':
        return 'Queued' if review_approved is True else 'Needs attention'
    if value == 'Submission uncertain':
        return last_verified_stage if last_verified_stage in {'Inventoried', 'Needs attention', 'Queued', 'Ready'} else 'Needs attention'
    return LEGACY.get(value)
