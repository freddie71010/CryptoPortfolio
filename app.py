from flask import Flask
app = Flask(__name__)


@app.route('/hello')
def hello_world():
	return "hello World"


@app.route('/')
def index():
	return "index page"


if __name__ == '__main__':
	app.run(port=5000, debug=True)
