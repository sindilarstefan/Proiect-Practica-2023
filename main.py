from tkinter import *
from tkinter import ttk
from Siteuri import Siteuri, Emag, Altex
from Email import SendMail
import time
import threading
import webbrowser
import re
import Factory
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.scrolledtext import ScrolledText


urls = []

file_path_prod = "produse.txt"


def extract_products_links(_file_path):
    with open(_file_path, "r") as file:
        lines = file.readlines()
    for line in lines:
        link = line.strip()  # Eliminăm caracterele de newline ("\n") de la sfârșitul fiecărei linii
        urls.append(link)


extract_products_links(file_path_prod)


def extract_emails_from_file(_file_path):
    emails = []
    with open(_file_path, "r") as file:
        for line in file:
            # Utilizăm expresia regulată pentru a căuta adresele de e-mail
            email_matches = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
            if email_matches:
                # Adăugăm adresele de e-mail găsite în listă
                emails.extend(email_matches)
    return emails


# Exemplu de utilizare
file_path_adr = "adrese_email.txt"
email_list = extract_emails_from_file(file_path_adr)

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
            label_n = Label(scrollable_frame, text=f"Pretul produsului cautat pe site-ul {i.get_magazin()} nu este sub "
                                                   f"pragul dorit!", fg=text_color, font=("Arial", 14, "bold"),
                            bg=bg_color)
            print(f"Pretul produsului cautat pe site-ul {i.get_magazin()} nu este sub pragul dorit!")
            label_n.pack()
    #frame2.update()
    #scrollable_frame.update()

def open_url(_url):
    webbrowser.open(_url)


def open_url_intermediary(_url):
    open_url(_url)


def update_interface(title, price, _url):
    global aux
    if aux % 2:
        bgg = "gray"
    else:
        bgg = "#A9A9A9"
    aux += 1
    # Primul layout
    frame1 = Frame(scrollable_frame, padx=10, pady=10, bg=bgg)
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
    link_label.bind("<Button-1>", lambda event, _url=_url: open_url_intermediary(_url))


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


label_info = Label(frame1, text="\n\nAlege numarul de mailuri trimise pe zi:", fg="black", font=("Arial", 14, "bold"),
                   wraplength=1000, bg=frame1["bg"])
label_info.pack()

# Creează o variabilă pentru a stoca valoarea selectată în combobox
selected_option = StringVar()

# Defineste optiunile pentru combobox
options = ["1", "2", "4", "86400"]

# Creează combobox-ul
combobox = ttk.Combobox(frame1, values=options, textvariable=selected_option)
combobox.pack()


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

    # global frame2
    # frame2.destroy()
    # frame2 = Frame(root, width=frame2_width, height=screen_height, bg=bg_color)
    # frame2.pack(side=LEFT, fill=BOTH, expand=True)
    for child in scrollable_frame.winfo_children():
        child.destroy()


def set_nr_mail():
    selected_value = selected_option.get()
    if selected_value:
        return selected_value
    else:
        return 0


# Crează al doilea frame
frame2 = Frame(root, width=frame2_width, height=screen_height, bg=bg_color)
frame2.pack(side=LEFT, fill=BOTH, expand=True)


######
# Funcția pentru a face scrolul pe cadru
def on_frame_configure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


# Configurarea scrollbara
canvas = Canvas(frame2, width=200, height=300)
scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Plasarea canvas-ului și scrollbar-ului în cadru
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


def onclick(event, _url, ax):
    # Obține coordonatele clicului
    x = event.xdata

    # Lista coordonatelor limitelor coloanelor
    coloane_limita = [bar.get_x() + bar.get_width() / 2 for bar in ax.containers[0]]

    # Caută coloana în care se află clicul
    for i, limita in enumerate(coloane_limita):
        if x < limita:
            # Clic în coloana i
            print(f"A fost apăsată coloana {i + 1}")

            # Deschide linkul corespunzător titlului găsit
            webbrowser.open(_url[i])
            break


def create_price_chart():
    global price
    pret_limita = int(price)

    # Lista produselor cu prețurile sub pragul dorit
    produse_sub_pret = []
    #################################################################
    for i, site in enumerate(siteuri):
        if site.get_pret() < pret_limita:
            produse_sub_pret.append((site.get_titlu(), site.get_pret(), site.get_magazin(), site.get_url()))

    if produse_sub_pret:
        produse_sub_pret = sorted(produse_sub_pret, key=lambda x: x[1])  # Sortăm produsele după preț

        titluri = [p[0] for p in produse_sub_pret]
        preturi = [p[1] for p in produse_sub_pret]
        magazine = [p[2] for p in produse_sub_pret]
        _url = [p[3] for p in produse_sub_pret]

        # Creăm figura și axa pentru graficul de bare
        fig, ax = plt.subplots()

        # Creăm graficul de bare
        ax.bar(titluri, preturi)

        # Adăugăm etichetele pe axa x
        ax.set_xticks(range(len(magazine)))
        ax.set_xticklabels(magazine, rotation=45, ha='right')

        # Adăugăm titlul și etichetele de axă
        ax.set_title('Produse cu prețuri sub pragul dorit')
        ax.set_xlabel('Produse')
        ax.set_ylabel('Preț (lei)')

        # Adăugăm numele magazinului pe fiecare bară
        for i, rect in enumerate(ax.patches):
            ax.text(rect.get_x() + rect.get_width() / 2, rect.get_height(), magazine[i],
                    ha='center', va='bottom')

        # Creăm obiectul de afișare a figurii în Tkinter
        canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas.draw()

        # Plasăm obiectul de afișare în frame2
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
        canvas.mpl_connect('button_press_event', lambda event: onclick(event, _url, ax))

        # Actualizăm interfața grafică
        scrollable_frame.update()
    else:
        # Dacă nu există produse sub pragul dorit, ștergem graficul anterior (dacă există)
        for child in scrollable_frame.winfo_children():
            child.destroy()

        # Afisăm un mesaj de informare în locul graficului
        label_n = Label(scrollable_frame, text="Nu există produse cu prețuri sub pragul dorit.", fg="white",
                        font=("Arial", 14), bg="black")
        label_n.pack()


label_grafic = Label(frame1, text="\n\nCrează grafic.", fg="black", font=("Arial", 14, "bold"), wraplength=1000,
                     bg=frame1["bg"])
label_grafic.pack()

# Adăugăm un buton în frame1 pentru a crea graficul
button_chart = Button(frame1, text="Crează grafic", command=create_price_chart)
button_chart.pack()


label_rst = Label(frame1, text="\n\nReseteaza datele introduse.", fg="black", font=("Arial", 14, "bold"),
                  wraplength=1000, bg=frame1["bg"])
label_rst.pack()

reset_button = Button(frame1, text="Resetare", command=reset_data)
reset_button.pack()


# Rulează interfața grafică în paralel cu verificarea prețului
def run_interface():
    while True:
        global reset
        global price
        logic_pret = True
        while logic_pret:
            if price != 0:
                logic_pret = False
            root.update()

        check_price()
        root.update()
        #frame2.update()

        run = True
        while run:
            if reset:
                run = False
                reset = False
            nr = set_nr_mail()
            tmp = 1
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


try:
    root.mainloop()
except KeyboardInterrupt:
    pass
