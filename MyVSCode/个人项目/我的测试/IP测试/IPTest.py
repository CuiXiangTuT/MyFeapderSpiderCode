import requests
import logging
from datetime import datetime,timedelta, time
import schedule


def do_func():
    url = "https://gwgp-cekvddtwkob.n.bdcloudapi.com/ip/local/geo/v1/district?"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.139 Safari/537.36'
    }
    response = requests.get(url=url,headers=headers).json()
    logging.basicConfig(filename='./ipLog.log',level=logging.INFO)
    logging.info("---------------------------------------------------------------")
    logging.info('------------{}-------'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    logging.info(response)

def main():
    # schedule.every(10).seconds.until(datetime(2023, 4, 12, 18, 00, 00)).do(do_func)
    schedule.every().minute.at(":30").do(do_func)
    local_time = '2023-04-12 18:00:00'
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    while now < local_time:
        schedule.run_pending()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    

if __name__ == '__main__':
    # schedule.every(0.5).hours.until(datetime(2023, 4, 12, 18, 00, 00)).do(do_job)
    main()