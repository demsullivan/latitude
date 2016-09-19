from collections import namedtuple

Source = namedtuple('Source',
    [
        'source_name',
        'source_url',
        'params',
        'parser'
    ]
)

Lead = namedtuple('Lead',
    [
        'lead_url',
        'date_created',
        'source_name',
        'title',
        'description',
        'contact_name',
        'contact_email',
        'website',
        'twitter',
        'linkedin'
    ]
)
