import requests
from bs4 import BeautifulSoup
import smtplib
import time
import tkinter as tk
import threading
import webbrowser


url = ('https://www.emag.ro/aparat-foto-mirrorless-sony-alpha-a7ii-24-3-mp-full-frame-wi-fi-nfc-e-mount-iso-50-25600-'
       'negru-obiectiv-sel2870-28-70mm-negru-ilce7m2kb-cec/pd/DFFJCMBBM/')

url2 = ('https://altex.ro/aparat-foto-mirrorless-sony-a7-ii-24-3-mp-wi-fi-negru-obiectiv-sel-28-70mm-f-3-5-5-6-oss/cpd/'
        'MLCILCE7M2KB/')

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

    if converted_price < 8500:
        #send_mail()
        update_interface(title.strip(), converted_price)
    else:
        label_n = tk.Label(root, text="Pretul produsului cautat nu este sub pragul dorit!", fg=text_color,
                           font=("Arial", 14, "bold"))
        label_n.pack()


def open_url(event):
    webbrowser.open(url)

def update_interface(title, price):
    # Eticheta pentru titlu
    label_titlu = tk.Label(root, text="Titlu:", fg=text_color, font=("Arial", 14, "bold"))
    label_titlu.pack()

    # Eticheta pentru preț
    label_pret = tk.Label(root, text="Preț:", fg=text_color, font=("Arial", 12))
    label_pret.pack()

    # Crează eticheta pentru URL ca link clicabil
    label_url = tk.Label(root, text="URL: ", fg=text_color, font=("Arial", 12))
    label_url.pack()

    link_label = tk.Label(root, text=url, fg=link_color, cursor="hand2", font=("Arial", 12, "underline"))
    link_label.pack()

    label_titlu.config(text="Titlu: " + title)
    label_pret.config(text="Preț: " + str(price) + "\n")
    label_url.config(text="URL: ")
    link_label.config(text=url, cursor="hand2")
    link_label.bind("<Button-1>", open_url)


# Crează fereastra principală
root = tk.Tk()
root.title("Verificare Preț")

# Setează culori personalizate
background_color = "#f2f2f2"
bg_color = "gray"
text_color = "#333333"
link_color = "#0000ff"

root.configure(background=background_color)

label_info = tk.Label(root, text="Informatii despre pret\n\n", fg=text_color, font=("Arial", 16, "bold"))
label_info.pack()


# Rulează interfața grafică în paralel cu verificarea prețului
def run_interface():
    while True:
        check_price()
        root.update()
        time.sleep(60)

# Pornirea interfeței grafice într-un thread separat
interface_thread = threading.Thread(target=run_interface)
interface_thread.start()

# Rulează interfața grafică principală
root.mainloop()
