# -*- coding: cp932 -*-
import sys
import os
import os.path
import json
import time
import constants
import face as f

def identify_person(is_local, src, person_group):
    print('Identifying person...')
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    if is_local:
        face_ids = f.get_face_id_by_file(src)
    else:
        face_ids = f.get_face_id_by_url(src)

    body = {
        'faceIds': face_ids,
        'personGroupId': person_group
    }

    data = json.loads(f.request('POST', constants.COGNITIVE_HOST, '/face/v1.0/identify', header, json.dumps(body)))
    try:
        if 'error' in data:
            print(data)
            return []
        result = []
        for face in data:
            face_id = face['faceId']
            if len(face['candidates']) == 0:
                return []
            for candidate in face['candidates']:
                result.append(constants.PEOPLE[person_group][candidate['personId']])
        return result
    except KeyError:
        print(data)
        return []

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python identify.py (-local | -dir | -url) source person_group')
        sys.exit()

    src = sys.argv[2]
    group = sys.argv[3]

    result = []
    if sys.argv[1] == '-local':
        result = identify_person(True, src, group)
    elif sys.argv[1] == '-dir':
        for file in os.listdir(src):
            result.extend(identify_person(True, os.path.join(src, file), group))
            time.sleep(7)
    else:   # -url as default
        result = identify_person(False, src, group)
    for p in result:
        print(p)
