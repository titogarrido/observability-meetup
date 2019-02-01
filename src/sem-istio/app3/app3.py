from flask import Flask
# Tracing
from jaeger_client import Config
import logging
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
import random, time

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

tracer = init_tracer('meaning') 
flask_tracer = FlaskTracer(tracer, True, app, ['url','url_rule','method','path','environ.HTTP_X_REAL_IP'])

@app.route("/meaning")
def meaning():
    parent_span = flask_tracer.get_span()
    with flask_tracer._tracer.start_span('calculate-meaning-of-life', child_of=parent_span) as span:
        span.set_tag("ANSWER","42")
        rand_time = 0.01*random.randint(0,150)
        time.sleep(rand_time)
        span.set_tag("DURATION", rand_time)
        return '42'

install_all_patches()

if __name__ == "__main__":
    app.run(port=8084, debug=True)