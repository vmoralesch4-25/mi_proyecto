import base64, json, sys, urllib.request

with open(sys.argv[1], 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

payload = json.dumps({'image': 'data:image/jpeg;base64,' + b64}).encode()
req = urllib.request.Request(
    'http://127.0.0.1:8000/predict',
    data=payload,
    headers={'Content-Type': 'application/json'},
)
try:
    print(urllib.request.urlopen(req).read().decode())
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode())