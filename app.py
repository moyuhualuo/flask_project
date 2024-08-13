from flask import Flask, render_template, url_for
from markupsafe import escape
app = Flask(__name__)


@app.route('/')
def index_page():  # put application's code here
    return render_template('index.html')
@app.route('/life')
def life_page():
    return render_template('life.html')
@app.route('/self_learn')
def self_learn_page():
    return render_template('self_learn.html')
@app.route('/commit')
def commit_page():
    return render_template('commit.html')
@app.route('/tools')
def tools_page():
    return render_template('tools.html')
@app.route('/serect')
def serect_page():
    return render_template('serect.html')


if __name__ == '__main__':
    app.run()
