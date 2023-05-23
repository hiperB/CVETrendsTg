import requests
import telethon
import telegram
#from telegram import ParseMode
import json
import datetime

#debug settings
log_level = 2  # 0 | 1 | 2
dir_logs = '/var/log/scripts'
log_file = 'main_cvet_tg.log'

#tg-chat
apiToken = '6162179055:AAE4OAoAxMHqvuZjZg7X3l1swWGZi7fND_Y'
chatID = '515382482'
channel_id = '-1001480961939'
apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

def logging(ll, text_log):
    if log_level > ll:
        lf.write(datetime.datetime.now().strftime("%c") + ' | '+ text_log +' \n')

def send_to_telegram(message):

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        logging(0, "Try Send message")
    except Exception as e:
        logging(0, "Sending is failure. Error: " + format(e))


def send_msg(text):
    token = apiToken
    chat_id = channel_id
    bot = telegram.Bot(token=token)

    #bot.sendMessage(chat_id=chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)
    bot.sendMessage(chat_id=chat_id, text=text)


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
    #print(json.dumps(response1.json(), indent=4, sort_keys=True))
    logging(0, "Prepare text for sending...")
    text_message = ''

    text_message += "TOP10 CVE by day #top10byday /n"
    text_message += "[Source](https://cvetrends.com/) /n/n"

    for item in response1.json()['data']:

        text_message += "<b>" + item['cve'] + "</b> /n"
        text_message += "<b>" + str(item['score']) + " : " + str(item['severity']) + "</b> /n"
        text_message += "<b>Published:</b> <i><u>" + str(item['publishedDate']) + "</i></u> | <b>Modified:</b> <i><u>" + str(item['publishedDate']) + "</i></u> /n"
        text_message += "[Url](" + str(item['cve_urls']) + ") /n"
        for url in item['vendor_advisories']:
            text_message += "[Vendor_url](" + url + ") /n"
        text_message += "<b>EPSS:</b> " + str(float(item['epss_score'])*100) + "% /n"
        text_message += "<b>Audience:</b> <i><u>" + str(item['audience_size']) + "</i></u> | <b>Tweets:</b> <i><u>" + str(item['num_tweets_and_retweets']) + "</i></u> /n"
        text_message += "||" + str(item['description']) + "|| /n/n/n"

    logging(0, "Try send to Tg...")
    send_msg(text_message)


#finish
logging(0, "Finished script")
logging(0, "/-------------------------------------")
lf.close()
