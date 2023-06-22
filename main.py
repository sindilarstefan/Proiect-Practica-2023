from tkinter import *
from tkinter import ttk
from Siteuri import Siteuri, Emag, Altex
from Email import SendMail
import time
import threading
import webbrowser

aux = 0

siteuri = []

url = ('https://www.emag.ro/aparat-foto-mirrorless-sony-alpha-a7ii-24-3-mp-full-frame-wi-fi-nfc-e-mount-iso-50-25600-'
       'negru-obiectiv-sel2870-28-70mm-negru-ilce7m2kb-cec/pd/DFFJCMBBM/')

url2 = ('https://altex.ro/aparat-foto-mirrorless-sony-a7-ii-24-3-mp-wi-fi-negru-obiectiv-sel-28-70mm-f-3-5-5-6-oss/cpd/'
        'MLCILCE7M2KB/')

url3= ('https://www.emag.ro/aparat-foto-mirrorless-sony-alpha-a7ii-body-24-3-mp-full-frame-wi-fi-nfc-e-mount-iso-50-'
       '25600-negru-ilce7m2b-cec/pd/D6XJCMBBM/')

def send_mail():
    print("!!!!!!")

    siteuri_sortate = sorted(siteuri, key=lambda x: x.get_pret())

    for i in siteuri_sortate:
        titlu = i.get_titlu()
        pret = i.get_pret()
        _url = i.get_url()
        if pret < 65000:
            to = "sindilar.stefan@gmail.com"
            subject = "Pretul produsului urmarit a scazut!!!"
            message = "{}\t\t\n\nPret: {}\t\t\n\nLink:\t\t\n{}".format(titlu, pret, _url)

            #t = SendMail(to, subject, message)
            #t.start()

def check_price():
    emag_obj = Emag(url)
    altex_obj = Altex(url2)
    emag_obj2 = Emag(url3)

    siteuri.append(emag_obj)
    siteuri.append(altex_obj)
    siteuri.append(emag_obj2)

    siteuri_sortate = sorted(siteuri, key=lambda x: x.get_pret())

    for i in siteuri_sortate:
        titlu = i.get_titlu()
        pret = i.get_pret()
        _url = i.get_url()
        if pret < 5000:
            update_interface(titlu.strip(), pret, _url)

            to = "sindilar.stefan@gmail.com"
            subject = "Pretul produsului urmarit a scazut!!!"
            message = "{}\t\t\n\nPret: {}\t\t\n\nLink:\t\t\n{}".format(titlu, pret, _url)

            #t = SendMail(to, subject, message)
            #t.start()
        else:
            label_n = Label(frame2, text=f"Pretul produsului cautat pe site-ul {i.get_magazin()} nu este sub pragul"
                                         f" dorit!", fg=text_color, font=("Arial", 14, "bold"),
                            bg=bg_color)
            print(f"Pretul produsului cautat pe site-ul {i.get_magazin()} nu este sub pragul dorit!")
            label_n.pack()

def open_url(_url):
    webbrowser.open(_url)

def open_url_intermediary(event, _url):
    open_url(_url)

def update_interface(title, price, _url):
    global aux
    if aux % 2:
        bgg = "gray"
    else:
        bgg = "#A9A9A9"
    aux += 1
    # Primul layout
    frame1 = Frame(frame2, padx=10, pady=10, bg=bgg)
    #frame1.pack(fill=BOTH, expand=True)
    frame1.pack(fill=BOTH)

    # Eticheta pentru titlu
    label_titlu = Label(frame1, text="Titlu:", fg=text_color, font=("Arial", 14, "bold"), wraplength=1000,
                           bg=frame1["bg"])
    label_titlu.pack()

    # Eticheta pentru preț
    label_pret = Label(frame1, text="Preț:", fg=text_color, font=("Arial", 12), bg=frame1["bg"])
    label_pret.pack()

    # Crează eticheta pentru URL ca link clicabil
    label_url = Label(frame1, text="URL: ", fg=text_color, font=("Arial", 12), wraplength=1000, bg=frame1["bg"])
    label_url.pack()

    link_label = Label(frame1, text=_url, fg=link_color, cursor="hand2", font=("Arial", 12, "underline"),
                          wraplength=1000, bg=frame1["bg"])
    link_label.pack()

    label_titlu.config(text="Titlu: " + title)
    label_pret.config(text="Preț: " + str(price) + "\n")
    label_url.config(text="URL: ")
    link_label.config(text=_url + "\n\n", cursor="hand2")
    link_label.bind("<Button-1>", lambda event, _url=_url: open_url_intermediary(event, _url))

root = Tk()
root.title("Verificare Preț")

# Setează culori personalizate
background_color = "#2F4F4F"
bg_color = "#2F4F4F"
text_color = "white"
link_color = "#0000ff"

root.configure(background=background_color)

label_info = Label(root, text="Informatii despre pret\n\n", fg=text_color, font=("Arial", 16, "bold"), bg=bg_color)
label_info.pack()

# Obține dimensiunile ecranului
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculează dimensiunile pentru cele două frame-uri
frame1_width = int(screen_width / 4)
frame2_width = screen_width - frame1_width

# Crează primul frame
frame1 = Frame(root, width=frame1_width, height=screen_height, bg="lightblue")
frame1.pack(side=LEFT, fill=BOTH)


# Creează o variabilă pentru a stoca valoarea selectată în combobox
selected_option = StringVar()

# Defineste optiunile pentru combobox
options = ["1", "2", "4", "86400"]

# Creează combobox-ul
combobox = ttk.Combobox(frame1, values=options, textvariable=selected_option)
combobox.pack()

def set_nr_mail():
    selected_value = selected_option.get()
    if selected_value:
        return selected_value
    else:
        return None


# Crează al doilea frame
frame2 = Frame(root, width=frame2_width, height=screen_height, bg=bg_color)
frame2.pack(side=LEFT, fill=BOTH, expand=True)


# Rulează interfața grafică în paralel cu verificarea prețului
def run_interface():
    check_price()
    root.update()


    while True:
        nr = set_nr_mail()
        if nr is not None:
            try:
                tmp = 86400 / int(nr)
            except ValueError:
                print("Valoarea selectată nu este un număr întreg!")
            send_mail()
            time.sleep(tmp)

# Pornirea interfeței grafice într-un thread separat
interface_thread = threading.Thread(target=run_interface)
interface_thread.start()

root.mainloop()
