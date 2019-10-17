import os
from flask import Flask,jsonify,make_response
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app import db

mongo = db.init_db()


#---------calling schedulers run time from config.py----------
from app.scheduler import auto_fetch
from app.notification_scheduler import tx_notification
from app.pgpverification_scheduler import pgp_verification
from app.invoice_scheduler import invoice_notification
from app.riskscore_scheduler import risk_score,profile_risk_score
from app.heist_riskscore_scheduler import risk_score_by_heist
from app.riskscore_safename_scheduler import risk_score_by_safename
from app.riskscore_oldtx_scheduler import tx_two_yearold
from app.heist_associated_scheduler import heist_associated_fetch
from app.top_users_scheduler import Top_user_percentage


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
    from app.api import balance

    app.register_blueprint(fetch.bp)
    app.register_blueprint(balance.bp)
    



#--------Schedulers timing and days functionality------------

    auto_fetch_scheduler = BackgroundScheduler()
    auto_fetch_scheduler.add_job(auto_fetch, trigger='cron', day_of_week='mon-sat', hour=11,minute=41)
    auto_fetch_scheduler.start()
    '''
    pgp_verification_scheduler = BackgroundScheduler()
    pgp_verification_scheduler.add_job(pgp_verification, trigger='cron', day_of_week='mon-sat', hour=13,minute=7)
    pgp_verification_scheduler.start()
    '''
    '''
    heist_associated_fetch_scheduler = BackgroundScheduler()
    heist_associated_fetch_scheduler.add_job(heist_associated_fetch, trigger='cron', day_of_week='mon-sat', hour=12,minute=28)
    heist_associated_fetch_scheduler.start()
    '''
    tx_two_yearold_scheduler = BackgroundScheduler()
    tx_two_yearold_scheduler.add_job(tx_two_yearold, trigger='cron', day_of_week='sat', hour=14,minute=2)
    tx_two_yearold_scheduler.start()
    
    risk_score_by_safename_scheduler = BackgroundScheduler()
    risk_score_by_safename_scheduler.add_job(risk_score_by_safename, trigger='cron', day_of_week='mon-sat', hour=14,minute=38)
    risk_score_by_safename_scheduler.start()
    
    risk_score_by_heist_scheduler = BackgroundScheduler()
    risk_score_by_heist_scheduler.add_job(risk_score_by_heist, trigger='cron', day_of_week='sat', hour=12,minute=59)
    risk_score_by_heist_scheduler.start()
    
    tx_notification_scheduler = BackgroundScheduler()
    #tx_notification_scheduler.add_job(tx_notification, trigger='cron', day_of_week='mon-sat', hour=10, minute=50)
    tx_notification_scheduler.add_job(tx_notification, trigger='interval', minutes=7)
    tx_notification_scheduler.start()
    #tx_notification_scheduler.add_job(tx_notification, trigger='interval', minutes=tx_notification_scheduler_minute)
    #tx_notification_scheduler.add_job(tx_notification, trigger='interval', hours=20)
    #tx_notification_scheduler.add_job(tx_notification, trigger='interval', seconds=60)
    
    risk_score_scheduler = BackgroundScheduler()
    risk_score_scheduler.add_job(risk_score, trigger='cron', day_of_week='mon', hour=12,minute=9)
    risk_score_scheduler.start()

    profile_risk_score_scheduler = BackgroundScheduler()
    profile_risk_score_scheduler.add_job(profile_risk_score, trigger='cron', day_of_week='fri', hour=15,minute=17)
    profile_risk_score_scheduler.start()
    
    invoice_notification_scheduler = BackgroundScheduler()
    #invoice_notification_scheduler.add_job(invoice_notification, trigger='cron', day_of_week='mon-sat', hour=9,minute=30)
    invoice_notification_scheduler.add_job(invoice_notification, trigger='interval', minutes=30)
    invoice_notification_scheduler.start()
    
    Top_user_percentage_scheduler = BackgroundScheduler()
    Top_user_percentage_scheduler.add_job(Top_user_percentage, trigger='cron', day_of_week='mon-sat', hour=11,minute=00)
    Top_user_percentage_scheduler.start()



    try:
        return app
    except:
        auto_fetch_scheduler.shutdown()
       # pgp_verification_scheduler.shutdown()
       # heist_associated_fetch_scheduler.shutdown()
        tx_two_yearold_scheduler.shutdown()
        risk_score_by_safename_scheduler.shutdown()
        risk_score_by_heist_scheduler.shutdown()
        tx_notification_scheduler.shutdown()
        risk_score_scheduler.shutdown()
        invoice_notification_scheduler.shutdown()
        profile_risk_score_scheduler.shutdown()
        Top_user_percentage_scheduler.shutdown()

'''

to = 0x94d0b8ccd2141a6969018be0bc25adc7ef91068c
from =0xbcbf6ac5f9d4d5d35bac4029b73aa4b9ed5e8c0b
1.005
'''
