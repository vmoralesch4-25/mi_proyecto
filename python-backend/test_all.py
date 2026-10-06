import base64, glob, json, os, urllib.request, urllib.error

for path in sorted(glob.glob('data/static/images/*')):
    with open(path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = json.dumps({'image': 'data:image/jpeg;base64,' + b64}).encode()
    req = urllib.request.Request('http://127.0.0.1:8000/predict', data=payload,
                                 headers={'Content-Type': 'application/json'})
    try:
        r = json.loads(urllib.request.urlopen(req).read())
        print(f"{os.path.basename(path):60} clase {r['prediction']:>2}  {r['confidence']:.4f}")
    except urllib.error.HTTPError as e:
        print(f"{os.path.basename(path):60} ERROR {e.code}")