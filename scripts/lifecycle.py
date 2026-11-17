"""Nine workflow states; confirmations and submission attempts remain evidence."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Applied', 'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate']
END_STATES = {'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate'}
LEGACY = {'Needs attention': 'Need review', 'Needs review': 'Need review', 'Needs eligibility': 'Need review',
          'Confirmed': 'Applied', 'In process': 'Interviewing',
          'Not aligned': 'Not pursuing', 'Not a fit': 'Not pursuing',
          'Withdrawn': 'Not pursuing', 'Closed': 'Not pursuing',
          'Offer': 'Interviewing', 'Accepted': 'Interviewing'}


def normalize(value, *, review_approved=False, last_verified_stage=None):
    """Preserve original evidence before any persisted legacy-label migration."""
    if value in STATUSES:
        return value
    if value == 'Shortlisted':
        return 'Queued' if review_approved is True else 'Need review'
    if value == 'Submission uncertain':
        return last_verified_stage if last_verified_stage in {'Inventoried', 'Need review', 'Queued', 'Ready'} else 'Need review'
    return LEGACY.get(value)
