import requests
from bs4 import BeautifulSoup
import smtplib
import time

url = ('https://www.emag.ro/aparat-foto-mirrorless-sony-alpha-a7ii-24-3-mp-full-frame-wi-fi-nfc-e-mount-iso-50-25600-'
       'negru-obiectiv-sel2870-28-70mm-negru-ilce7m2kb-cec/pd/DFFJCMBBM/')

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

def send_mail():
    print("SEND MAIL!!!!!!!!!!!!!!!!!!!")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('testproiect2023@gmail.com', 'parolatestproiect2023')

    subject = 'Price fell down!'
    body = 'Check the amazon link https://www.amazon.com/Sony-Mirrorless-Digital-Camera-28-70mm/dp/B00PX8CNCM/ref=' \
           'sr_1_2?crid=1EXWDB1U3GR0C&keywords=sony%2Ba7&qid=1687244192&sprefix=sony%2Ba7%2Caps%2C439&sr=8-2&th=1'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'testproiect2023@gmail.com',
        'sindilar.stefan@gmail.com',
        msg
    )

    print("HEY MAIL HAS BEEN SENT!")

    server.quit()

def check_price():
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    logic = True

    title_element = soup.find(class_="page-title")
    if title_element:
        title = title_element.get_text()
    else:
        logic = False
        print("Nu s-a putut găsi titlul produsului.")

    converted_price = 2000.0
    price_element = soup.find(class_="product-new-price has-deal")
    if price_element:
        price = price_element.get_text()
        converted_price = float(price[0:5].replace(".", ""))
    else:
        logic = False
        print("Nu s-a putut găsi prețul produsului.")

    if logic:
        print(title.strip())
        print(converted_price)

    if (converted_price < 1500):
        send_mail()

while(True):
    check_price()
    time.sleep(60)