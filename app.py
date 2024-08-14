from flask import Flask, render_template, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from markupsafe import escape
import click
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, default=1)
    like_count = db.Column(db.Integer, default=0)
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
@app.route('/like', methods=['POST'])
def like():
    like_record = Like.query.get(1)
    if like_record is None:
        like_record = Like(like_count=1)
        db.session.add(like_record)
    else:
        like_record.like_count += 1
    db.session.commit()
    return jsonify({'like_count': like_record.like_count})
@app.route('/get_like_count', methods=['GET'])
def get_like_count():
    like_record = Like.query.get(1)
    like_count = like_record.like_count if like_record else 0
    return jsonify({'like_count': like_count})
if __name__ == '__main__':
    app.run()
