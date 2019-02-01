from flask import Flask
from jaeger_client import Config
import logging
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
from opentracing_instrumentation.request_context import RequestContextManager
import requests

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={ # usually read from some yaml config
            'sampler': {'type': 'const', 'param': 1, },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
    )
    return config.initialize_tracer()

app = Flask(__name__)
tracer = init_tracer('frontend') 
flask_tracer = FlaskTracer(tracer, True, app, ['url','url_rule','method','path','environ.HTTP_X_REAL_IP'])

@app.route("/")
def frontend():
    with RequestContextManager(span=flask_tracer.get_span()):
        requests.get('http://127.0.0.1:8083/backend')
        requests.get('http://127.0.0.1:8084/meaning')
        return 'frontend'

install_all_patches()
if __name__ == "__main__":
    app.run(port=8082, debug=True)