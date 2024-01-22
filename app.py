from flask import Flask
from flask_restful import Api

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

api = Api(app)

# api 작성


if __name__ == '__main__':
    app.run()
