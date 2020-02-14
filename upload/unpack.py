import base64
import json
import sys
import os

for i, line in enumerate(sys.stdin):
    e = json.loads(line)
    dirname = 'photos/' + e['category']
    os.makedirs(dirname, exist_ok=True)
    for j, image in enumerate(e['images']):
        filename = f'{e["title"]}-{i}-{j}.jpg'
        with open(dirname + '/' + filename, 'wb') as f:
            b64_bytes = image['url'].replace('data:image/jpeg;base64,', '').encode('ascii')
            f.write(base64.decodestring(b64_bytes))
