import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def search(keyword):
    url = 'https://www.costco.com/CatalogSearch?dept=All&keyword=' + keyword
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    content = page.text
    print(page.status_code)

    # Find item
    items_text = re.findall('<input type="hidden" id="product_name_.*', content)
    item_names = []

    # Extract item name
    for item_text in items_text:
        item_name = re.search('value=".*"', item_text).group(0).replace('value="', '').replace('"', '')
        item_names.append(item_name)

    return item_names

def sendEmail(mail_msg, gmail_password):
    sender = 'hujunwei0614@gmail.com'
    receivers = ['smiletan0115@outlook.com', 'jasonhu0614@outlook.com']

    gmail_user = 'hujunwei0614@gmail.com'

    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header("Costco刷包", 'utf-8')
    message['To'] =  Header("剁手", 'utf-8')
    message['Subject'] = Header('找到包了！！', 'utf-8')
     
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sender, receivers, message.as_string())
        server.close()

        print ("Mail sent")
    except smtplib.SMTPException as e:
        print (e)
        print ("Error: Unable to send email")

def constructEmailBody(items, item_match_str):
    email_body = '<h4>Found bags in costco</h4>'

    for item in items:
        if item_match_str in item:
            email_body += '<p><span style="color:red">' + item + '</span></p>'
        else:
            email_body += '<p>' + item + '</p>'

    return email_body


gmail_pwd = input('Input gmail password:\n')
while 1 == 1:
    print('****** start round ******')

    # REPLACE HERE FOR SEARCH BOX IN COSTCO PAGE
    search_str = 'ysl+niki'

    # REPLACE HERE FOR TARGET ITEM FOUND
    item_match_str = 'niki'

    items = search(search_str)
    print(items)

    if len(items) > 0: 
        if True: 
            sendEmail(constructEmailBody(items, item_match_str), gmail_pwd)
            print('Found' + item_match_str)
        else:
            print('Found items but no ' + item_match_str + ' found in search results')
    else:
        print('No items found')
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print('****** end round at ' + current_time + '******\n\n' )
    time.sleep(300)
    