import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    FLASK_APP = 'app.py'
    # 基本配置
    SECRET_KEY = os.urandom(24)  # 生成一个随机的密钥
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭对模型修改的监控

    # 数据库配置
    WIN = sys.platform.startswith('win')
    prefix = '///' if WIN else '////'
    DATABASE_FILE = os.getenv('DATABASE_FILE', 'data.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:{prefix}{os.path.join(os.path.dirname(os.path.abspath(__file__)), DATABASE_FILE)}'

