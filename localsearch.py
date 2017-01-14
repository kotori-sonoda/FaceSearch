# -*- coding: cp932 -*-
import sys
import os
import os.path
import time
import shutil
import constants
import identify

def search(dir_path, person_group):
    personmap = {}
    group = constants.PEOPLE[person_group]

    for k, v in group.items():
        personmap[v] = []

    for f in os.listdir(dir_path):
        full_path = os.path.join(dir_path, f)
        people_found = identify.identify_person(True, full_path, person_group)
        if len(people_found) > 0:
            for p in people_found:
                personmap[p].append(full_path)
        time.sleep(7)

    for k, v in personmap.items():
        out_dir = os.path.join('result', k)
        if len(v) > 0 and not os.path.exists(out_dir):
            os.mkdir(out_dir)
        for f in v:
            shutil.copy2(f, out_dir)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python localsearch.py dir_path person_group')
        sys.exit()

    search(sys.argv[1], sys.argv[2])
    print('done.')
