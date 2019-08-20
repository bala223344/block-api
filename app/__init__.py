import os
from flask import Flask,jsonify,make_response
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app import db
mongo = db.init_db()
from app.scheduler import auto_fetch,heist_associated_fetch,tx_two_yearold,risk_score_by_safename,risk_score_by_heist,tx_notification#,risk_score


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
    auto_fetch_scheduler.add_job(auto_fetch, trigger='cron', day_of_week='mon', hour=16,minute=31)
    auto_fetch_scheduler.start()
        
    heist_associated_fetch_scheduler = BackgroundScheduler()
    heist_associated_fetch_scheduler.add_job(heist_associated_fetch, trigger='cron', day_of_week='mon', hour=16,minute=41)
    heist_associated_fetch_scheduler.start()

    '''
    tx_two_yearold_scheduler = BackgroundScheduler()
    tx_two_yearold_scheduler.add_job(tx_two_yearold, trigger='cron', day_of_week='mon-sat', hour=19,minute=2)
    tx_two_yearold_scheduler.start()
    
    risk_score_by_safename_scheduler = BackgroundScheduler()
    risk_score_by_safename_scheduler.add_job(risk_score_by_safename, trigger='cron', day_of_week='mon-sat', hour=15,minute=21)
    risk_score_by_safename_scheduler.start()
    
    risk_score_by_heist_scheduler = BackgroundScheduler()
    risk_score_by_heist_scheduler.add_job(risk_score_by_heist, trigger='cron', day_of_week='mon-sat', hour=19,minute=38)
    risk_score_by_heist_scheduler.start()
    '''

    tx_notification_scheduler = BackgroundScheduler()
    #tx_notification_scheduler.add_job(tx_notification, trigger='cron', day_of_week='mon-sat', hour=11,minute=24)
    tx_notification_scheduler.add_job(tx_notification, trigger='interval', seconds=300)
    tx_notification_scheduler.start()


    '''
    risk_score_scheduler = BackgroundScheduler()
    risk_score_scheduler.add_job(risk_score, trigger='cron', day_of_week='mon-sat', hour=16,minute=00)
    risk_score_scheduler.start()
    '''

    try:
        return app
    except:
        auto_fetch_scheduler.shutdown()
        heist_associated_fetch_scheduler.shutdown()
        #tx_two_yearold_scheduler.shutdown()
        #risk_score_by_safename_scheduler.shutdown()
        #risk_score_by_heist_scheduler.shutdown()
        tx_notification_scheduler.shutdown()
        # risk_score_scheduler.shutdown()
