from flask import Flask
from flask_pymongo import PyMongo
from controllers import routes

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flask_mongo'

mongo = PyMongo(app)

routes.init_app(app)

if __name__ == '__main__':
    app.run(host='localhost', port=4000, debug=True)