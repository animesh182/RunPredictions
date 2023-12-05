from datetime import datetime,timezone
import logging
import azure.functions as func
import pandas as pd
from PredictionFunction.meta_tables import data,location_specific_dictionary,weather_locations
async def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Timer trigger function ran at %s', utc_timestamp)







