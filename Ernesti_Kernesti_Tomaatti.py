import tkinter as tk
from PIL import Image, ImageTk
import random
import pygame
import math

# Äänen asetukset
pygame.mixer.init()

# Lataa ääniefekti (muunna MP3 WAV-muotoon tai käytä WAV-tiedostoa)

# Luo pääikkuna
root = tk.Tk()
root.title("Tomaatin heitto")
root.geometry("800x600")

# Asetetaan kuvien järkevä koko (leveys x korkeus)
new_width = 150
new_height = 150

# Lataa ja pienennä kuvat käyttäen Pillow-kirjastoa
kernesti_img = Image.open("MESSI.jpg")
kernesti_img = kernesti_img.resize((new_width, new_height))
kernesti_img = ImageTk.PhotoImage(kernesti_img)

ernesti_img = Image.open("Ronaldo.jpg")
ernesti_img = ernesti_img.resize((new_width, new_height))
ernesti_img = ImageTk.PhotoImage(ernesti_img)

maalitaulu_img = Image.open("Goal.jpg")
maalitaulu_img = maalitaulu_img.resize((new_width, new_height))
maalitaulu_img = ImageTk.PhotoImage(maalitaulu_img)

tomato_img = Image.open("ball.jpg")
tomato_img = tomato_img.resize((50, 50))  # Tomaatin koko
tomato_img = ImageTk.PhotoImage(tomato_img)

# Osumatiedot sanakirjaan
osumat = {'ernesti': 0, 'kernesti': 0}

# Funktio asettaa kernestiin satunnaiseen sijaintiin vasempaan reunaan
def sijoita_kernesti():
    x = random.randint(0, 100)  # Vasemmalla alueella
    y = random.randint(0, root.winfo_height() - new_height)
    kernesti_label.place(x=x, y=y)

# Funktio asettaa ernestiin satunnaiseen sijaintiin oikealle reunalle
def sijoita_ernesti():
    x = random.randint(root.winfo_width() - new_width - 100, root.winfo_width() - new_width)
    y = random.randint(0, root.winfo_height() - new_height)
    ernesti_label.place(x=x, y=y)

# Luo maalitaulun vakioitu sijainti
def sijoita_maalitaulu():
    maalitaulu_x = (root.winfo_width() // 2) - (new_width // 2)
    maalitaulu_y = (root.winfo_height() // 2) - (new_height // 2)
    maalitaulu_label.place(x=maalitaulu_x, y=maalitaulu_y)
    # Päivitä osumatiedot näytölle
    päivitä_osumatiedot()

# Päivitä osumatiedot näyttöruudulle
def päivitä_osumatiedot():
    osumat_text = f"ernesti: {osumat['ernesti']}  Kernesti: {osumat['kernesti']}"
    osumat_label.config(text=osumat_text)

# Tarkista, osuiko tomaatti maalitauluun
def tarkista_osuma():
    tomato_x, tomato_y = tomato_label.winfo_x(), tomato_label.winfo_y()
    tomato_width, tomato_height = tomato_img.width(), tomato_img.height()

    maalitaulu_x, maalitaulu_y = maalitaulu_label.winfo_x(), maalitaulu_label.winfo_y()
    maalitaulu_width, maalitaulu_height = maalitaulu_img.width(), maalitaulu_img.height()

    # Tarkista, onko tomaatti maalitaulun alueella
    if (tomato_x + tomato_width > maalitaulu_x and
        tomato_x < maalitaulu_x + maalitaulu_width and
        tomato_y + tomato_height > maalitaulu_y and
        tomato_y < maalitaulu_y + maalitaulu_height):
        return True
    return False

# Tomaatin lentämisen funktio (suoraviivainen tai kaareva liike)
def heita_tomaatti(start_x, start_y, kentta):
    # Alustetaan tomaatti lähtöpisteeseen
    tomato_label.place(x=start_x, y=start_y)
    
    # Soita ääniefekti

    maalitaulu_x, maalitaulu_y = maalitaulu_label.winfo_x(), maalitaulu_label.winfo_y()

    # Tomaatin lentoradan kaaren asettaminen
    distance_x = maalitaulu_x - start_x
    distance_y = maalitaulu_y - start_y
    steps = 50  # Kuinka monessa askeleessa tomaatti liikkuu

    for step in range(steps):
        # Lasketaan tomaatin x- ja y-koordinaatit jokaisessa vaiheessa
        t = step / steps
        current_x = int(start_x + t * distance_x)
        # Kaariliike (y = ax^2 - muokkaa tarvittaessa kaaren muotoa)
        current_y = int(start_y + t * distance_y - 100 * math.sin(t * math.pi))  # 100 määrää kaaren korkeuden

        # Siirretään tomaatti uuteen sijaintiin ja päivitetään graafinen näkymä
        tomato_label.place(x=current_x, y=current_y)
        root.update()
        root.after(20)  # Viive jokaisen askeleen välillä

    # Tarkista osuma maalitauluun
    if tarkista_osuma():
        osumat[kentta] += 1
    # Päivitä osumatiedot näytölle
    päivitä_osumatiedot()

# Tomaatin heittämisen funktio ernestiin kohdalta
def heita_tomaatti_ernesti():
    ernesti_x, ernesti_y = ernesti_label.winfo_x(), ernesti_label.winfo_y()
    heita_tomaatti(ernesti_x, ernesti_y, 'ernesti')

# Tomaatin heittämisen funktio Kernestiin kohdalta
def heita_tomaatti_kernesti():
    kernesti_x, kernesti_y = kernesti_label.winfo_x(), kernesti_label.winfo_y()
    heita_tomaatti(kernesti_x, kernesti_y, 'kernesti')

# Nollaa osumatiedot
def nollaa_osumat():
    osumat['ernesti'] = 0
    osumat['kernesti'] = 0
    päivitä_osumatiedot()

# Luo tkinter Label-widgetit kuvien sijoittamiseksi
kernesti_label = tk.Label(root, image=kernesti_img)
kernesti_label.place(x=0, y=0)  # Aluksi sijoitetaan jonnekin

ernesti_label = tk.Label(root, image=ernesti_img)
ernesti_label.place(x=0, y=0)  # Aluksi piilotettu

maalitaulu_label = tk.Label(root, image=maalitaulu_img)
maalitaulu_label.place(x=0, y=0)  # Maalitaulu keskittyy myöhemmin

# Luo tomaatti, mutta piilota se aluksi
tomato_label = tk.Label(root, image=tomato_img)
tomato_label.place_forget()

# Näyttöruutu osumatiedoille
osumat_label = tk.Label(root, text="", font=("Arial", 16), bg="white")
osumat_label.place(x=(root.winfo_width() // 2) - 100, y=20)  # Sijoitetaan maalitaulun ylle

# Luo painike, joka sijoittaa ernestiin satunnaiseen paikkaan oikealle reunalle
painike_ernesti = tk.Button(root, text="Sijoita ernesti", command=sijoita_ernesti)
painike_ernesti.pack(side=tk.BOTTOM)

# Luo painike, joka heittää tomaatin ernestiin kohdalta
painike_tomaatti_ernesti = tk.Button(root, text="Heitä tomaatti ernestiin kohdalta", command=heita_tomaatti_ernesti)
painike_tomaatti_ernesti.pack(side=tk.BOTTOM)

# Luo painike, joka heittää tomaatin Kernestiiin kohdalta
painike_tomaatti_kernesti = tk.Button(root, text="Heitä tomaatti Kernestiin kohdalta", command=heita_tomaatti_kernesti)
painike_tomaatti_kernesti.pack(side=tk.BOTTOM)

# Luo painike, joka nollaa osumatiedot
painike_reset = tk.Button(root, text="Reset", command=nollaa_osumat)
painike_reset.pack(side=tk.BOTTOM)

# Sijoitetaan kuvat aluksi
root.after(100, sijoita_kernesti)
root.after(100, sijoita_ernesti)
root.after(100, sijoita_maalitaulu)

# Käynnistä pääsilmukka
root.mainloop()