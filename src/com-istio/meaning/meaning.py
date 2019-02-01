from flask import Flask
import random, time

app = Flask(__name__)

@app.route("/meaning")
def meaning():
        rand_time = 0.01*random.randint(0,150)
        time.sleep(rand_time)
        return '42'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8084, debug=True, threaded=True)
