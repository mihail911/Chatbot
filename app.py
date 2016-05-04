from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    print "hi"
    print request
    print request.data
    print request.args
    print request.form 
    return 'Hello World! asf\n'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
