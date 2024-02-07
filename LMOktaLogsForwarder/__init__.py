import datetime
import logging

import azure.functions as func
from .okta_log_collector import OktaLogCollector

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    oktaLogCollector = OktaLogCollector()
    if mytimer.past_due:
        logging.info('The timer is past due!')

    try:
        logging.info("in try block")
        oktaLogCollector.collect_logs()
    except Exception as e:
                logging.error("error %s", str(e))
    logging.info('Python timer trigger function after changes ran at %s', utc_timestamp)
