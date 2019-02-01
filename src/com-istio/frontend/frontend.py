import sys

from flask import Flask, abort, request, render_template
import requests

app = Flask(__name__)

def getForwardHeaders(request):
    headers = {}

    incoming_headers = [ 'x-request-id',
                         'x-b3-traceid',
                         'x-b3-spanid',
                         'x-b3-parentspanid',
                         'x-b3-sampled',
                         'x-b3-flags',
                         'x-ot-span-context'
    ]

    for ihdr in incoming_headers:
        val = request.headers.get(ihdr)
        if val is not None:
            headers[ihdr] = val
            print("incoming: "+ihdr+":"+val, file=sys.stderr)
    return headers


@app.route("/")
def f1():
    tracking_headers = getForwardHeaders(request)
    backend_out = requests.get('http://backend:8083/backend', headers=tracking_headers).content
    meaning_out = requests.get('http://meaning:8084/meaning', headers=tracking_headers).content
    return render_template('index.html', backend=str(backend_out), meaning=str(meaning_out))

if __name__ == "__main__":
    print('frontend v2')
    app.run(host='0.0.0.0', port=8082, debug=True)
