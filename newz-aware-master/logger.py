import logging
from app import make_predictions
from datetime import datetime
from pytz import timezone
import os

import warnings
warnings.filterwarnings("ignore")


logging.basicConfig(level=logging.INFO, filename='predictions.log', filemode='a')

if __name__ == '__main__':

    list_of_articles = make_predictions()
    
    for article in list_of_articles:
        log_string = f"{datetime.now(timezone('Asia/Kolkata')).strftime('%d/%m/%Y, %H:%M:%S')} - {article[3]} - {article[0]} - {article[1]}"
        logging.info(log_string)