from flask_pymongo import PyMongo
from app.config import MongoUri

def init_db():
    mongo = PyMongo()
    return mongo


#----------Setup MongoUri----------

def get_db(app, mongo):
    app.config["MONGO_URI"] = MongoUri#"mongodb://localhost:27017/crypto_app"
    mongo.init_app(app)


