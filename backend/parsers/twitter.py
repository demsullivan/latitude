from __future__ import absolute_import
import twitter
import os
import logging
import urllib

from stores.models import Lead

logger = logging.getLogger('latitude.twitter')

class TwitterParser(object):
    def __init__(self):
        self.api = twitter.Api(consumer_key=os.environ.get('TWITTER_CONSUMER_KEY', None),
                               consumer_secret=os.environ.get('TWITTER_CONSUMER_SECRET', None),
                               access_token_key=os.environ.get('TWITTER_ACCESS_TOKEN_KEY', None),
                               access_token_secret=os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', None))

    def tweet_to_lead_for_source(self, source):

        def tweet_to_lead(status):
            tweet = status.AsDict()
            url = 'https://twitter.com/{}/status/{}'.format(tweet['user']['screen_name'], tweet['id'])
            title = u'Tweet from {}'.format(tweet['user']['name'])
            twitter = tweet['user']['screen_name']

            logger.info('Converting tweet to lead for tweet ID {}'.format(tweet['id']))

            return Lead(lead_url=url, date_created=status.created_at_in_seconds, source_name=source.source_name, title=title,
                        description=tweet['text'], contact_name=tweet['user']['name'], contact_email='n/a',
                        website='n/a', twitter=twitter, linkedin='n/a')

        return tweet_to_lead


    def get_leads(self, source, search_terms=None):
        logger.info('Doing twitter search for terms [{}]'.format(search_terms))

        result = self.api.GetSearch(raw_query='q={}&result_type=recent'.format(urllib.quote(search_terms)))
        logger.debug(urllib.quote(search_terms))
        logger.debug(result)
        return map(self.tweet_to_lead_for_source(source), result)
