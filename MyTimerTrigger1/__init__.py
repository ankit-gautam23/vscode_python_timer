import datetime
import logging

import azure.functions as func
import okta_log_collector

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    try:
        okta_log_collector.collect_logs()
    except Exception as e:
                logging.error("error %s", str(e))
    logging.info('Python timer trigger function after changes ran at %s', utc_timestamp)
