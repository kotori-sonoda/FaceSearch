# coding:utf8

from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys, os
import os.path
import urllib2
import urllib
import constants
import identify as i

def query_twitter(kwd, count):
    session = OAuth1Session(
        constants.TW_CONSUMER_KEY,
        constants.TW_CONSUMER_SEC,
        constants.TW_ACCESS_TOKEN,
        constants.TW_ACCESS_TOKEN_SEC
    )

    url = 'https://api.twitter.com/1.1/search/tweets.json'

    print('Querying Twitter...')
    res = json.loads(session.get(url, params = {'q':'%s filter:images' % kwd, 'count':count, 'result_type':'recent', 'include_entities':'true'}).text)
    
    links = []
    for tw in res['statuses']:
        if 'extended_entities' in tw:
            for media in tw['extended_entities']['media']:
                links.append(media['media_url'])
        else:
            if 'media' in tw['entities']:
                for media in tw['entities']['media']:
                    links.append(media['media_url'])
    return links

def identify(links, person_group):
    personmap = {}
    for k, v in constants.PEOPLE[person_group].items():
        personmap[v] = []
    for link in links:
        people_found = i.identify_person(False, link, person_group)
        if len(people_found) > 0:
            for p in people_found:
                personmap[p].append(link)
        time.sleep(7)

    for k, v in personmap.items():
        out_dir = os.path.join('result', k)
        if len(v) > 0 and not os.path.exists(out_dir):
            os.mkdir(out_dir)
        for url in v:
            filename = os.path.basename(url)
            urllib.urlretrieve(url, os.path.join(out_dir, filename))

if __name__ == '__main__':
    kwd = sys.argv[1].decode('cp932').encode('utf8')
    count = int(sys.argv[2])

    links = query_twitter(kwd, count)
    print('%d images to be processed.' % len(links))
    identify(links, 'aqours')
    print('done.')
