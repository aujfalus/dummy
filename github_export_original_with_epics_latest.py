"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""

#New

# New type of comments introduced blablabla

# blablabla whatever new comment extra comment

import csv
import requests # requests might not be installed by default, use pip for installing it (pip install requests)
import getpass

GITHUB_USER = 'aujfalus'
#GITHUB_USER = 'yahman72'
GITHUB_PASSWORD = ''
REPO = 'yahman72/ta'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?per_page=100&state=all' % REPO
#ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?state=all' % REPO
MSTONES_FOR_REPO_URL = 'https://api.github.com/repos/%s/milestones' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    print("Received %s issues" % len(r.json()))
    for issue in r.json():
        #print issue
        if issue.get("pull_request", None) is not None:
            continue
        labels = issue['labels']
        label_names = []
        prio = ''
        ctg = ''
        size = ''
        cust = 'N' # code comment
        outsrc = ''
        status = issue['state']
#        zero_effort_lbls = ['duplicate', 'invalid']
        zero_effort_lbls = ['Must have', 'Should have']
        prio_lbls = ['prio0', 'prio1', 'prio2', 'prio3']
        ctg_lbls = ['enhancement', 'bug', 'Research', 'infra', '3rd party', 'tooling','Documentation']
        size_lbls = ['S0', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']
        idle_lbls = ['idle', ]
#        outsrc_lbls = ['OS1','OS2']
        outsrc_lbls = ['epic']
        for label in labels:
            label_name = label['name']
            if label_name in prio_lbls:
                prio = label_name
            elif label_name in ctg_lbls:
                ctg = label_name
            #elif label_name in zero_effort_lbls:
            #    size = 'S0'
            elif label_name in size_lbls:
                size = label_name
            #elif label_name == "customer needs":
            #    cust = 'Y'
            elif label_name in zero_effort_lbls:
                cust = label_name
            elif label_name in outsrc_lbls:
                outsrc = label_name
            elif label_name in idle_lbls:
                status = 'idle'
        csvout.writerow([
                u'%s' % issue['number'],
                u'%s' % issue['title'].encode("ascii", "ignore"),
#                u'%s' % issue['title'],
                u'%s' % status,
                u'%s' % '' if issue['milestone'] is None else issue['milestone']['title'],
                u'%s' % prio,
                u'%s' % cust,
                u'%s' % ctg,
                u'%s' % size,
                u'%s' % outsrc,#fixed
                #comment
                u'%s' % issue['created_at'],
                u'%s' % issue['updated_at'],
                u'%s' % issue['closed_at'],
                ])
    #print("issue %s" % dict(issue).keys())

def write_mstones(response):
    "output a list of milestones to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    print("Received %s milestones" % len(r.json()))
    for mstone in r.json():
        #print mstone
        csvout.writerow([
                u'%s' % mstone['title'],
                u'%s' % mstone['description'],
                u'%s' % mstone['state'],
                u'%s' % mstone['due_on'],
                u'%s' % mstone['created_at'],
                u'%s' % mstone['updated_at'],
                ])
    #print("issue %s" % dict(issue).keys())

def get_pages(response):
    #more pages? examine the 'link' header returned
    # 'Link': '<https://api.github.com/repositories/32080817/issues?page=2>; rel="next", <https://api.github.com/repositories/32080817/issues?page=3>; rel="last"',
    # First page has these (last + next):
    #   {'last': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=5', 'next': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=2'}
    # The ones in between these (last + next + prev + first):
    #   {'prev': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=1', 'last': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=5', 'first': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=1', 'next': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=3'}
    # Last page has these (prev + first):
    #   {'prev': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=4', 'first': 'https://api.github.com/repositories/32080817/issues?per_page=100&state=all&page=1'}
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    return pages

#Also new comments here.
    
u = ''
p = ''
u = raw_input('github login [%s]: ' % GITHUB_USER)
p = getpass.getpass('github password: ')
if u == '':
    u = GITHUB_USER
if p == '':
    p = GITHUB_PASSWORD
AUTH = (u, p)
# ISSUE LIST
print("logging in to '%s' as '%s'" % (ISSUES_FOR_REPO_URL, u))
r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
print("Returned HTTP status '%s'" % r.status_code)
csvfile = 'github_export.csv'
fh = open(csvfile, 'wb')
csvout = csv.writer(fh)
csvout.writerow((u'id', u'Title', u'Status', u'Milestone', u'Prio', u'Customer Needs', u'Category', u'Size', u'Outsource', u'Created At', u'Updated At', u'Closed At'))
write_issues(r)
pages = get_pages(r)
#print pages
while 'last' in pages and 'next' in pages:
    r = requests.get(pages['next'], auth=AUTH)
    write_issues(r)
    pages = get_pages(r)
    #print pages


# MILESTONE LIST
print("logging in to '%s' as '%s'" % (MSTONES_FOR_REPO_URL, u))
r = requests.get(MSTONES_FOR_REPO_URL, auth=AUTH)
print("Returned HTTP status '%s'" % r.status_code)
csvfile = 'milestone_export.csv'
fh = open(csvfile, 'wb')
csvout = csv.writer(fh)
csvout.writerow((u'Title', u'Description', u'State', u'Due', u'Created At', u'Updated At'))
write_mstones(r)

