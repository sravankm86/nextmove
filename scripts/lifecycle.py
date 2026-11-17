"""Ten workflow states; confirmations and submission attempts remain evidence."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Needs answer', 'Applied', 'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate']
END_STATES = {'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate'}
