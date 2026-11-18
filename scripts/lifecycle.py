"""Active lifecycle ends at a verified resume; later legacy outcomes are read-only."""
STATUSES = ['Inventoried', 'Need review', 'Queued', 'Ready', 'Not pursuing', 'Duplicate']
END_STATES = {'Ready', 'Not pursuing', 'Duplicate'}
LEGACY_READ_ONLY = {'Needs answer', 'Applied', 'Interviewing', 'Rejected'}
