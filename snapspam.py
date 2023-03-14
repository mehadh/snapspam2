import requests
import random
from imagetyperzapi4 import imagetyperzapi
import os
from re import sub
from decimal import Decimal
import threading
import time
from time import sleep
import urllib.parse
import sys
from urllib.parse import quote

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "2820",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundary53f6Ua04sQBVQ5LA",
    "origin": "https://help.snapchat.com",
    "referer": "https://help.snapchat.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"109\", \"Not)A;Brand\";v=\"99\", \"Chromium\";v=\"109\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

targets = []
emails = []
reasons = []
proxies = []
ita = None
threadNum = 1
goodReport = 0
badReport = 0
badCaptcha = 0


def report(email, reportee, reason, captcha):
    body = """
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"key\"

ts-reported-content-2
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"answers\"

5153567363039232,5743597085261824
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"g-recaptcha-response\"

"""+captcha+"""
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"field-24380496\"

none
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"field-24335325\"

"""+email+"""
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"field-25326243\"


------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"field-24380626\"

"""+reportee+"""
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"field-22808619\"

"""+reason+"""
------WebKitFormBoundary53f6Ua04sQBVQ5LA
Content-Disposition: form-data; name=\"tags\"

ts,viewed-story,cf-ts-content-story,ca-live-story,sca-safety-concern
------WebKitFormBoundary53f6Ua04sQBVQ5LA--
"""
    encoded = urllib.parse.quote(body)
    proxy = random.choice(proxies)
    proxArr = proxy.split(":")
    realStr = proxArr[-2]+":"+proxArr[-1]+"@"+proxArr[0]+":"+proxArr[1]

    username = quote(proxArr[-2])
    password = quote(proxArr[-1])
    proxy = proxArr[0]
    proxy_port = proxArr[1]

    proxy_http = 'http://' + username + ':' + password + '@' + proxy + ':' + proxy_port
    proxyes = {'all' : proxy_http}

    response = requests.post("https://wassupsnap.appspot.com/en-us/api/v2/zendesk/send", headers=headers, data=body, proxies=proxyes)
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False

def loadAll():
    global targets
    global emails
    global reasons
    global proxies
    try:
        with open("targets.txt", "r") as f:
            targets = [i.rstrip() for i in f.readlines()]
        with open("emails.txt", "r") as f:
            emails = [i.rstrip() for i in f.readlines()]
        with open("reasons.txt", "r") as f:
            reasons = [i.rstrip() for i in f.readlines()]
        with open("proxies.txt", "r") as f:
            proxies = [i.rstrip() for i in f.readlines()]
        return True
    except:
        print("There was an error when loading the required files. Check that the following files exist: targets.txt, emails.txt, reasons.txt, proxies.txt, token.txt")
        os.system('pause')
        quit()


def initCaptcha():
    try:
        tokenfile = open("./token.txt", "r")
    except:
        print("An error has occurred while opening token.txt. Please check that token.txt is created and contains a valid token key.")
        os.system('pause')
        quit()
    access_token = tokenfile.read()
    global ita
    try:
        ita = imagetyperzapi.ImageTyperzAPI(access_token)
        balance = ita.account_balance()
        print("Connected to ImageTyperz successfully! Balance: {}".format(balance))
        return True
    except:
        print("An error has occurred while connecting to ImageTyperz. Please check that token.txt is created and contains a valid token key.")
        os.system('pause')
        quit()

def getBalance():
    balance = ita.account_balance()
    value = Decimal(sub(r'[^\d.]', '', balance))
    return value

def solveCaptcha():
    try:
        proxy = random.choice(proxies)
        proxArr = proxy.split(":")
        realStr = proxArr[-2]+":"+proxArr[-1]+"@"+proxArr[0]+":"+proxArr[1]
        xhttpproxies = {
                "all":"http://" + realStr,
                #"https": "https://" + proxy
            }
        # captcha_params = {'page_url': "https://help.snapchat.com/hc/en-us/requests/new", 'sitekey': '6Ldt4CkUAAAAAJuBNvKkEcx7OcZFLfrn9cMkrXR8', "type": 2, 'proxy': xhttpproxies}
        captcha_params = {'page_url': "https://help.snapchat.com/hc/en-us/requests/new", 'sitekey': '6Ldt4CkUAAAAAJuBNvKkEcx7OcZFLfrn9cMkrXR8', "type": 2}
        captcha_id = ita.submit_recaptcha(captcha_params)
        print("Submitted captcha!")
        response = None
        while not response:
            sleep(10)
            response = ita.retrieve_response(captcha_id)
        answer = response['Response']
        print("Answer received!")
        return (True, answer)
    except Exception as e:
        global badCaptcha
        badCaptcha+=1
        print(e)
        print("An error has occurred in solveCaptcha")
        return (False, None)

def child():
    global badCaptcha
    global badReport
    global goodReport
    captchaRes = solveCaptcha()
    if captchaRes[0] == False:
        badCaptcha+=1
        print("Didn't get captcha result.")
    else:
        email = random.choice(emails)
        target = random.choice(targets)
        reason = random.choice(reasons)
        result = report(email, target, reason, captchaRes[1])
        if result == True:
            goodReport += 1
            print("REPORT SENT! {} @ {} for {}".format(email, target, reason))
        else:
            badReport +=1
            print("Report failed. {} @ {} for {}".format(email, target, reason))


def startThread():
    if (threading.active_count() < int(threadNum)):
        new_thread = threading.Thread(target=child)
        new_thread.start()
    # else:
    #     time.sleep(2)
    #     startThread()

def runner():
    while getBalance() > 2:
        if (threading.active_count() < int(threadNum)):
            updateTitle()
            startThread()

def startup():
    if loadAll() != True:
        print("Error in loadAll")
        quit()
    if initCaptcha() != True:
        print("Error in initCaptcha")
        quit()
    if getBalance() < 2:
        print("Put some money in your captcha!")
        quit()
    if promptThreads() != True:
        print("Error in promptThreads")
        quit()
    runner()

def promptThreads():
    global threadNum
    give = input("Enter the amount of threads: ")
    if len(give) < 1 or give.isnumeric() == False:
        print("Not a valid number!")
        promptThreads()
    else:
        threadNum = int(give)
    return True

def setTitle(title):
    try:
        os.system("title "+title)
    except:
        pass
    try: 
        sys.stdout.write("\x1b]2;"+title+"\x07")
    except:
        pass

def updateTitle():
    title = "[SNAPSPAM] SENT: {} FAILED: {} CAPTCHERR: {} BAL: {} THREADS: {}".format(goodReport, badReport, badCaptcha, getBalance(), threadNum)
    setTitle(title)

startup()