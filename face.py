# -*- coding: cp932 -*-
import httplib
import json
import sys
import os
import os.path
import constants

def _request(method, host, path, header, body):
    conn = httplib.HTTPSConnection(host)
    conn.request(method, path, body, header)
    response = conn.getresponse()
    return response.read()

def get_face_id_by_file(file_path):
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    data = _request('POST', constants.COGNITIVE_HOST, '/face/v1.0/detect?', header, open(file_path, 'rb'))

    result = json.loads(data)
    face_ids = []
    if 'error' in result:
        print(result)
        return
    for face in result:
        face_ids.append(face['faceId'])
    return face_ids

def get_face_id_by_url(url):
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    body = {
        'url': url
    }

    data = _request('POST', constants.COGNITIVE_HOST, '/face/v1.0/detect?', header, json.dumps(body))

    result = json.loads(data)
    face_ids = []
    if 'error' in result:
        print(result)
        return
    for face in result:
        face_ids.append(face['faceId'])
    return face_ids

def create_person_group(person_group_name):
    print('creating person group...')
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    body = {
        'name': person_group_name
    }

    data = _request('PUT', constants.COGNITIVE_HOST, '/face/v1.0/persongroups/%s' % person_group_name, header, json.dumps(body))

    if len(data) > 0:
        print(data)
        return

    print('person group %s successfully created.' % person_group_name)

def create_person(person_group, person_name):
    print('Creating person...')
    header = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    body = {
        'name': person_name
    }

    data = json.loads(_request('POST', constants.COGNITIVE_HOST, '/face/v1.0/persongroups/%s/persons' % person_group, header, json.dumps(body)))

    try:
        if 'personId' in data:
            print('person %s successfully created.' % person_name)
            return data['personId']
        else:
            print(data)
            return ''
    except KeyError:
        print(data)
        return ''

def add_person_face(person_group, person, file_path):
    print('Adding person face...')
    header = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    data = json.loads(_request('POST', constants.COGNITIVE_HOST, '/face/v1.0/persongroups/%s/persons/%s/persistedFaces' % (person_group, person), header, open(file_path, 'rb')))

    try:
        if 'persistedFaceId' in data:
            return data['persistedFaceId']
        else:
            print(data)
            return ''
    except KeyError:
        print(data)
        return ''

def train_person_group(person_group):
    header = {
        'Ocp-Apim-Subscription-Key': constants.COGNITIVE_KEY
    }

    data = _request('POST', constants.COGNITIVE_HOST, '/face/v1.0/persongroups/%s/train' % person_group, header, {})

    if len(data) > 0:
        print(data)

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage: python face.py (-cg | -cp | -af | -tr) parameters')
        print('-cg: Create person group')
        print('-cp: Create person')
        print('-af: Add face data into person')
        print('-tr: Train person group')
        sys.exit()

    mode = sys.argv[1]
    if mode == '-cg':
        if len(sys.argv) != 3:
            print('Usage: python face.py -cg person_group_name')
            print('Create person group.')
            sys.exit()
        create_person_group(sys.argv[2])
    elif mode == '-cp':
        if len(sys.argv) != 4:
            print('Usage: python face.py -cp person_name person_group')
            print('Create person.')
            sys.exit()
        person_name = sys.argv[2]
        group = sys.argv[3]
        print(create_person(group, person_name))
    elif mode == '-af':
        if len(sys.argv) != 5:
            print('Usage: python face.py -af file_path person_id person_group')
            print('Add face data into person.')
            sys.exit()
        file_path = sys.argv[2]
        person_id = sys.argv[3]
        group = sys.argv[4]
        for f in os.listdir(file_path):
            face_id = add_person_face(group, person_id, os.path.join(file_path, f))
    elif mode == '-tr':
        if len(sys.argv) != 3:
            print('Usage: python face.py -tr person_group')
            print('Train person group')
            sys.exit()
        group = sys.argv[2]
        train_person_group(group)
