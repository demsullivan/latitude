from .models import Source

def seeds():
    return [
        Source(source_name='We Work Remotely - Devops', source_url='https://weworkremotely.com/categories/6-devops-sysadmin/jobs.rss', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='We Work Remotely - Programming', source_url='https://weworkremotely.com/categories/2-programming/jobs.rss', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Authentic Jobs', source_url='https://authenticjobs.com/rss/custom.php?remote=1', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Stack Overflow Jobs', source_url='http://stackoverflow.com/jobs/feed', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='wfh.io Devops', source_url='https://www.wfh.io/categories/6-remote-devops/jobs.atom', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='wfh.io Software Dev', source_url='https://www.wfh.io/categories/1-remote-software-development/jobs.atom', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Smashing Magazine', source_url='http://jobs.smashingmagazine.com/rss/all/programming', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='remoteok.io Dev Jobs', source_url='https://remoteok.io/remote-dev-jobs.json', params='{}', parser=''),
        Source(source_name='Django Gigs', source_url='https://djangogigs.com/feeds/gigs/', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Django Jobbers', source_url='http://djangojobbers.com/rss/', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Github Jobs - Python', source_url='https://jobs.github.com/positions.atom?description=Python', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Github Jobs - Rails', source_url='https://jobs.github.com/positions.atom?description=Rails', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Github Jobs - Devops', source_url='https://jobs.github.com/positions.atom?description=Devops', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Rails Jobbers', source_url='http://railsjobbers.com/rss/', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Jobspresso Development', source_url='https://jobspresso.co/?feed=job_feed&job_types=developer', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Django Jobs', source_url='https://www.djangojobs.net/jobs/latest/feed/rss/', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Work in Startups - Programming', source_url='http://feeds.feedburner.com/workinstartups/EGLo?format=xml', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Reddit /r/forhire', source_url='https://www.reddit.com/r/forhire/search.rss?q=hiring+developer&restrict_sr=on&sort=new&t=all', params='{}', parser='parsers.rss.RSSParser'),
        Source(source_name='Craigslist Toronto - Software', source_url='cltorsof',  params='{"site": "toronto", "category": "sof", "filters": null}', parser='parsers.craigslist.CraigslistParser'),
        Source(source_name='Twitter Django', source_url='twitterdjango', params='{"search_terms": "(django OR python OR flask) AND (freelance OR freelancer OR contract OR consultant OR developer)"}', parser='parsers.twitter.TwitterParser'),
        Source(source_name='Twitter Ember.js', source_url='twitterember', params='{"search_terms": "(ember OR ember.js) AND (contract OR freelancer OR freelance OR developer)"}', parser='parsers.twitter.TwitterParser')
    ]
