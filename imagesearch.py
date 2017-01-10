# -*- coding: cp932 -*-
import urllib2
import urllib
import json
import sys
import time
import os
import os.path
import constants
import identify

PAGE_SIZE = 10

def search_image(word, page):
    param = {
        'searchType': 'image',
        'key': constants.GCS_KEY,
        'cx': constants.GCS_ENGINE_ID,
        'q': word.decode('cp932').encode('utf8'),
        'start': page
    }

    request_url = constants.GCS_URI % urllib.urlencode(param)
    response = urllib2.urlopen(request_url)
    result = json.loads(response.read())
    if len(result['items']) > 0:
        return [item['link'] for item in result['items']]

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python imagesearch.py keyword page(up to 10) person_group')

    word = sys.argv[1]
    page = int(sys.argv[2])
    group = sys.argv[3]

    result = []
    start = 1
    for p in range(1, page + 1):
        result.extend(search_image(word, start))
        start = start + PAGE_SIZE

    personmap = {}
    for k, v in constants.PEOPLE[group].items():
        personmap[v] = []
    for link in result:
        people_found = identify.identify_person(False, link, group)
        if len(people_found) > 0:
            for p in people_found:
                personmap[p].append(link)
        time.sleep(7)

    for k, v in personmap.items():
        out_dir = os.path.join('result', k)
        if len(v) > 0 and not os.path.exists():
            os.mkdir(out_dir)
        for url in v:
            filename = os.path.basename(url)
            urllib.urlretrieve(url, os.path.join(out_dir, filename))

    print('done.')
