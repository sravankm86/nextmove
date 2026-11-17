"""Nine workflow states; confirmations and submission attempts remain evidence."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Applied', 'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate']
END_STATES = {'Interviewing', 'Not pursuing', 'Rejected', 'Duplicate'}
