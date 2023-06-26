from tkinter import *
from tkinter import ttk
from Siteuri import Siteuri, Emag, Altex
from Email import SendMail
import time
import threading
import webbrowser
import re
import Factory

urls = []

file_path_prod = "produse.txt"

def extract_products_links(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    for line in lines:
        link = line.strip()  # Eliminăm caracterele de newline ("\n") de la sfârșitul fiecărei linii
        urls.append(link)

extract_products_links(file_path_prod)

def extract_emails_from_file(file_path):
    emails = []
    with open(file_path, "r") as file:
        for line in file:
            # Utilizăm expresia regulată pentru a căuta adresele de e-mail
            email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
            if email_matches:
                # Adăugăm adresele de e-mail găsite în listă
                emails.extend(email_matches)
    return emails

# Exemplu de utilizare
file_path = "adrese_email.txt"
email_list = extract_emails_from_file(file_path)

aux = 0
price = 0

siteuri = []

def send_mail():
    print("!!!!!!")
    global price
    pret_limita = int(price)

    siteuri_sortate = sorted(siteuri, key=lambda x: x.get_pret())

    for i in siteuri_sortate:
        titlu = i.get_titlu()
        pret = i.get_pret()
        _url = i.get_url()
        if pret < pret_limita:
            subject = "Pretul produsului urmarit a scazut!!!"
            message = "{}\t\t\n\nPret: {}\t\t\n\nLink:\t\t\n{}".format(titlu, pret, _url)
            for to in email_list:
                print(to)
                #t = SendMail(to, subject, message)
                #t.start()

def check_price():
    global price
    pret_limita = int(price)

    for _url in urls:
        site = Factory.factory(_url)
        siteuri.append(site)

    siteuri_sortate = sorted(siteuri, key=lambda x: x.get_pret())

    for i in siteuri_sortate:
        titlu = i.get_titlu()
        pret = i.get_pret()
        _url = i.get_url()
        if pret < pret_limita:
            update_interface(titlu.strip(), pret, _url)
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
                          wraplength=980, bg=frame1["bg"])
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

label_info = Label(frame1, text="Alege numarul de mailuri trimise pe zi:", fg="black", font=("Arial", 14, "bold"),
                   wraplength=1000, bg=frame1["bg"])
label_info.pack()

# Creează o variabilă pentru a stoca valoarea selectată în combobox
selected_option = StringVar()

# Defineste optiunile pentru combobox
options = ["1", "2", "4", "86400"]

# Creează combobox-ul
combobox = ttk.Combobox(frame1, values=options, textvariable=selected_option)
combobox.pack()

label_inf = Label(frame1, text="\nIntrodu pretul maxim al produsului:", fg="black", font=("Arial", 14, "bold"),
                   wraplength=1000, bg=frame1["bg"])
label_inf.pack()
def validate_input(new_value):
    if new_value.isdigit() or new_value == "":
        return True
    else:
        return False

def get_entry_value():
    global price
    logic_pret = True
    while logic_pret:
        price = entry.get()
        if price != "":
            logic_pret = False
        root.update()
        print(price)

validation = frame1.register(validate_input)

entry = Entry(frame1, validate="key", validatecommand=(validation, "%P"))
entry.pack()

button = Button(frame1, text="Seteaza valoarea", command=get_entry_value)
button.pack()

reset = False
def reset_data():
    print("Reset!")
    global reset
    reset = True
    global price
    entry.delete(0, END)  # Șterge conținutul câmpului de introducere a prețului
    combobox.delete(0, END)
    price = 0  # Resetează valoarea prețului la 0
    siteuri.clear()

    global frame2
    frame2.destroy()
    frame2 = Frame(root, width=frame2_width, height=screen_height, bg=bg_color)
    frame2.pack(side=LEFT, fill=BOTH, expand=True)


label_rst = Label(frame1, text="\n\nReseteaza datele introduse.", fg="black", font=("Arial", 14, "bold"),
                   wraplength=1000, bg=frame1["bg"])
label_rst.pack()

reset_button = Button(frame1, text="Resetare", command=reset_data)
reset_button.pack()


def set_nr_mail():
    selected_value = selected_option.get()
    if selected_value:
        return selected_value
    else:
        return 0


# Crează al doilea frame
frame2 = Frame(root, width=frame2_width, height=screen_height, bg=bg_color)
frame2.pack(side=LEFT, fill=BOTH, expand=True)



# Rulează interfața grafică în paralel cu verificarea prețului
def run_interface():
    while True:
        global reset
        global price
        logic_pret = True
        while logic_pret:
            if price != 0:
                logic_pret = False

        check_price()
        root.update()

        run = True
        while run:
            if reset:
                run = False
                reset = False
            nr = set_nr_mail()
            if nr != 0:
                try:
                    tmp = 86400 / int(nr)
                except ValueError:
                    print("Valoarea selectată nu este un număr întreg!")
                send_mail()
                time.sleep(tmp)
            root.update()


# Pornirea interfeței grafice într-un thread separat
interface_thread = threading.Thread(target=run_interface)
interface_thread.start()

root.mainloop()
