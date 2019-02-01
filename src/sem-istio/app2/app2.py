from flask import Flask
# Tracing
from jaeger_client import Config
import logging
from flask_opentracing import FlaskTracer
from opentracing_instrumentation.client_hooks import install_all_patches
# Database
from flask_pymongo import PyMongo

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
tracer = init_tracer('backend') 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/mybackend"
mongo = PyMongo(app)



flask_tracer = FlaskTracer(tracer, True, app, ['url','url_rule','method','path','environ.HTTP_X_REAL_IP'])

@app.route("/backend")
def backend():
    parent_span = flask_tracer.get_span()
    with flask_tracer._tracer.start_span('user-exists-check', child_of=parent_span) as span:
        span.set_tag("QUERY","mongo.db.users.find({'online': True})")
        online_users = mongo.db.users.find({"online": True})
        span.log_kv({'event': 'mongo_result', 'value': online_users})
    return 'backend'

install_all_patches()

if __name__ == "__main__":
    app.run(port=8083, debug=True)