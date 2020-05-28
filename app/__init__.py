import os
from flask import Flask,jsonify,make_response
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from app import db

mongo = db.init_db()


#---------calling schedulers run time from config.py----------

from app.heist_fetch_scheduler import auto_fetch
from app.notification_scheduler import tx_notification
from app.pgpverification_scheduler import pgp_verification
from app.invoice_scheduler import invoice_moving,invoice_notification_interval, safename_verification
from app.riskscore_scheduler import risk_score,profile_risk_score
from app.heist_riskscore_scheduler import risk_score_by_heist
from app.riskscore_safename_scheduler import risk_score_by_safename
from app.riskscore_oldtx_scheduler import tx_two_yearold
from app.heist_associated_scheduler import heist_associated_fetch
from app.top_users_scheduler import Top_user_percentage
from app.ethersync import EthSync,EthTimeSync,EthTimeSync1,EthTimeSync2,EthTimeSync3,EthIntSync1,EthIntSync2,EthIntSync3,EthIntSync4
from app.btc import btc_data_sync
from app.gpl import GplDataSync


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


#---------register api files in blueprint----------

    from app.api import fetch
    from app.api import balance
    from app.api import unknown_riskscore

    app.register_blueprint(fetch.bp)
    app.register_blueprint(balance.bp)
    app.register_blueprint(unknown_riskscore.bp)
    

    EthSync_scheduler = BackgroundScheduler()
    EthSync_scheduler.add_job(EthSync,trigger='interval',hours=3)
    EthSync_scheduler.add_job(EthSync, trigger='cron', day_of_week='mon-sun', hour=21,minute=10)
    EthSync_scheduler.add_job(EthSync,trigger='interval',hours=5)
    EthSync_scheduler.add_job(EthSync,trigger='interval',hours=2)
    #EthSync_scheduler.add_job(EthSync,trigger='interval',minutes=20)
    EthSync_scheduler.start()


    EthTimeSync_scheduler = BackgroundScheduler()
    EthTimeSync_scheduler.add_job(EthTimeSync,trigger='interval',hours=5000)
    #EthTimeSync_scheduler.add_job(EthTimeSync1,trigger='interval',minutes=30)
    #EthTimeSync_scheduler.add_job(EthTimeSync2,trigger='interval',minutes=40)
    #EthTimeSync_scheduler.add_job(EthTimeSync3,trigger='interval',minutes=6000)
    EthTimeSync_scheduler.start()


    EthIntSync_scheduler = BackgroundScheduler()
    EthIntSync_scheduler.add_job(EthIntSync1,trigger='interval',hours=2)
    EthIntSync_scheduler.add_job(EthIntSync1,trigger='interval',hours=3)
    EthIntSync_scheduler.add_job(EthIntSync1,trigger='interval',hours=5)
    #EthIntSync_scheduler.add_job(EthIntSync4,trigger='interval',minutes=30)
    EthIntSync_scheduler.add_job(EthIntSync1, trigger='cron', day_of_week='mon-sun', hour=21,minute=3)
    #EthSync_scheduler.add_job(EthSync,trigger='interval',minutes=30)
    #EthSync_scheduler.add_job(EthSync,trigger='interval',minutes=60)
    EthIntSync_scheduler.start()

    GplDataSync_scheduler = BackgroundScheduler()
    GplDataSync_scheduler.add_job(GplDataSync,trigger='interval',hours=22222)
    GplDataSync_scheduler.add_job(GplDataSync,trigger='interval',hours=33333)
    GplDataSync_scheduler.add_job(GplDataSync,trigger='interval',minutes=555555)
    #EthIntSync_scheduler.add_job(GplDataSync,trigger='interval',minutes=30)
    GplDataSync_scheduler.add_job(GplDataSync, trigger='cron', day_of_week='sun', hour=13,minute=30)
    #EthSync_scheduler.add_job(GplDataSync,trigger='interval',minutes=30)
    #EthSync_scheduler.add_job(GplDataSync,trigger='interval',minutes=60)
    GplDataSync_scheduler.start()


    btc_data_sync_scheduler = BackgroundScheduler()
    #btc_data_sync_scheduler.add_job(btc_data_sync,trigger='interval',minutes=10)
    btc_data_sync_scheduler.add_job(btc_data_sync,trigger='interval',minutes=30)
    #btc_data_sync_scheduler.add_job(btc_data_sync, trigger='cron', day_of_week='mon-sat', hour=9,minute=21)
    btc_data_sync_scheduler.start()


#--------Schedulers timing and days functionality------------

    safename_verification_scheduler = BackgroundScheduler()
    #safename_verification_scheduler.add_job(safename_verification, trigger='cron', day_of_week='mon-sun', hour=13,minute=4)
    safename_verification_scheduler.add_job(safename_verification, trigger='interval', minutes=20)
    safename_verification_scheduler.start()
    

    auto_fetch_scheduler = BackgroundScheduler()
    auto_fetch_scheduler.add_job(auto_fetch, trigger='cron', day_of_week='sun', hour=11,minute=41)
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
    tx_two_yearold_scheduler.add_job(tx_two_yearold, trigger='cron', day_of_week='mon-sat', hour=12,minute=00)
    tx_two_yearold_scheduler.start()
    
    risk_score_by_safename_scheduler = BackgroundScheduler()
    risk_score_by_safename_scheduler.add_job(risk_score_by_safename, trigger='cron', day_of_week='mon-sat', hour=11,minute=30)
    risk_score_by_safename_scheduler.start()
    
    '''
    risk_score_by_heist_scheduler = BackgroundScheduler()
    risk_score_by_heist_scheduler.add_job(risk_score_by_heist, trigger='cron', day_of_week='mon-sat', hour=15,minute=00)
    risk_score_by_heist_scheduler.start()
    '''

    tx_notification_scheduler = BackgroundScheduler()
    tx_notification_scheduler.add_job(tx_notification, trigger='interval', minutes=7000)
    #tx_notification_scheduler.add_job(tx_notification, trigger='cron', day_of_week='mon-sat', hour=13,minute=24)
    tx_notification_scheduler.start()
    
    risk_score_scheduler = BackgroundScheduler()
    risk_score_scheduler.add_job(risk_score, trigger='cron', day_of_week='mon-sat', hour=15,minute=13)
    risk_score_scheduler.start()

    profile_risk_score_scheduler = BackgroundScheduler()
    profile_risk_score_scheduler.add_job(profile_risk_score, trigger='cron', day_of_week='mon-sat', hour=15,minute=17)
    profile_risk_score_scheduler.start()
    
    # invoice_moving_scheduler = BackgroundScheduler()
    # invoice_moving_scheduler.add_job(invoice_moving, trigger='interval', minutes=60)
    # invoice_moving_scheduler.start()




    invoice_notification_interval_scheduler = BackgroundScheduler()
    invoice_notification_interval_scheduler.add_job(invoice_notification_interval, trigger='cron', day_of_week='mon-sun', hour=13,minute=12)
    #invoice_notification_interval_scheduler.add_job(invoice_notification_interval, trigger='interval', minutes=1)
    invoice_notification_interval_scheduler.start()

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
       # risk_score_by_heist_scheduler.shutdown()
        tx_notification_scheduler.shutdown()
        risk_score_scheduler.shutdown()
        #invoice_moving_scheduler.shutdown()
        profile_risk_score_scheduler.shutdown()
        Top_user_percentage_scheduler.shutdown()
        invoice_notification_interval_scheduler.shutdown()
        EthSync_scheduler.shutdown()
        EthTimeSync_scheduler.shutdown()
        GplDataSync_scheduler.shutdown()

