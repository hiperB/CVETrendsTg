import requests
import telethon
import json
import datetime

#debug settings
log_level = 2  # 0 | 1 | 2
dir_logs = '/var/log/scripts'
log_file = 'main_cvet_tg.log'

def logging(ll, text_log):
    if log_level > ll:
        lf.write(datetime.datetime.now().strftime("%c") + ' | '+ text_log +' \n')

lf = open(dir_logs+'/'+log_file, 'at')

#start
logging(0, "/-------------------------------------")
logging(0, "Started scripts")


#todo request to apu cvet

try:
    response1 = requests.get('https://cvetrends.com/api/cves/24hrs')
    logging(0, "Try requsts to API CVET")

except requests.exceptions.HTTPError as errh:
    logging(0, "Http Error: " + format(errh))
except requests.exceptions.ConnectionError as errc:
    logging(0, "Error Connecting: " + format(errc))
except requests.exceptions.Timeout as errt:
    logging(0, "Timeout Error: " + format(errt))
except requests.exceptions.RequestException as err:
    logging(0, "OOps: Something Else: " + format(err))

if (response1):
    print(json.dumps(response1.json(), indent=4, sort_keys=True))
#




#finish
logging(0, "Finished script")
logging(0, "/-------------------------------------")
lf.close()
