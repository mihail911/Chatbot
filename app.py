from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello World! asf\n'

if __name__ == '__main__':
    app.run(host="127.0.0.1")
