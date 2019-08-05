import os
from flask import Flask,jsonify,make_response
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app import db
mongo = db.init_db()
from app.scheduler import auto_fetch,heist_associated_fetch


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping()
    CORS(app)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(400)
    def not_found(error):
        return make_response(jsonify(error='Not found'), 400)

    @app.errorhandler(500)
    def error_500(error):
        return make_response({}, 500)

    db.get_db(mongo=mongo, app=app)

    from app.api import fetch
    
    app.register_blueprint(fetch.bp)
    

    auto_fetch_scheduler = BackgroundScheduler()
    auto_fetch_scheduler.add_job(auto_fetch, trigger='cron', day_of_week='mon-sat', hour=18,minute=21)
    auto_fetch_scheduler.start()
        

    heist_associated_fetch_scheduler = BackgroundScheduler()
    heist_associated_fetch_scheduler.add_job(heist_associated_fetch, trigger='cron', day_of_week='mon-sat', hour=17,minute=19)
    heist_associated_fetch_scheduler.start()


    try:
        return app
    except:
        auto_fetch_scheduler.shutdown()
        heist_associated_fetch_scheduler.shutdown()


       
