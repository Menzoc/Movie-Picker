import time  # To delete

import random
import re
from io import open, BytesIO
from sys import exit
import requests
import json
from threading import Thread
from bs4 import BeautifulSoup

import tkinter as tk
import tkinter.font as fnt
from PIL import ImageTk, Image

numberOfFilm = 250
URL = f"https://www.imdb.com/search/title?title_type=feature&sort=num_votes,desc&count={str(numberOfFilm)}"


def fetch_database():
    start_time = time.time()
    response = requests.get(URL).text
    soup = BeautifulSoup(response, 'html.parser')
    with open("main_db.json", "w", encoding="utf-8") as write_file:
        dataFinal = ()
        for m in soup.findAll("div", class_="lister-item mode-advanced"):

            certificate = str(m.find("span", attrs={"class", "certificate"}).text)

            resume = str(m.findAll("p", attrs={"class", "text-muted"})[1])
            resume = re.sub('<p class="text-muted">\n', '', resume)
            resume = re.sub('</p>', '', resume)
            resume = re.sub('<a href=".*">', '', resume)
            resume = re.sub('</a>', '', resume)

            years = m.find("span", attrs={"class": "lister-item-year"}).text[1:-1]
            years = re.findall(r'\d+', years)[0]

            actors_list = ""
            rawActor = str(m.findAll("p", attrs={"class": ""}))
            rawActor = re.findall('<a href=".*/">.*</a>', rawActor)
            for actor in rawActor:
                actor = re.sub(r'<a href=".*/">', '', actor)
                actor = re.sub(r'</a>', '', actor)
                actors_list = actors_list + actor + ', '

            titles = m.h3.a.text

            ratings = m.strong.text

            genre = m.find("span", attrs={"class": "genre"}).text.strip()

            runtime = m.find("span", attrs={"class": "runtime"}).text

            link = f"https://www.imbd.com{m.a.get('href')}"

            linkimage = str(m.find("img", attrs={"class", "loadlate"}))
            linkimage = str(
                re.sub(r'<img alt=".*" class="loadlate" data-tconst=".*" height="98" loadlate="', '', linkimage))
            linkimage = str(re.sub(r'" src=".*" width=".."/>', '', linkimage))
            linkimage = str(re.sub(r'\.[0-9a-zA-Z_,]*\.jpg', '.jpg', linkimage))

            data = {
                       "name": titles,
                       "year": years,
                       "resume": resume,
                       "actors": actors_list,
                       "ratings": ratings,
                       "genre": genre,
                       "certificate": certificate,
                       "runtime": runtime,
                       "Image Link": linkimage,
                       "IMBD link": link
                   },
            dataFinal = dataFinal + data

        json.dump(dataFinal, write_file, ensure_ascii=False, indent=4)

        interval = time.time() - start_time
        print('Total time in seconds:', interval)


def nb_votes():
    def count():
        count.watcher = entry.get()
        count.watcher = int(count.watcher)
        if count.watcher != 0:
            canvas_1.destroy()
            root.destroy()

    def get_watcher():
        return count.watcher

    root = tk.Tk()
    root.geometry('1400x400')
    root.title('MOVIE PICKER')
    canvas_1 = tk.Canvas(root, bg="black", bd=0, relief='ridge')
    canvas_1.pack(expand=True, fill=tk.BOTH)
    canvas_1.configure(highlightthickness=0)

    bienvenu1_lbl = tk.Label(canvas_1, text='Please, enter the numbers of participants',
                             bg='black', fg='white', font=fnt.Font(size=15))
    bienvenu1_lbl.pack()

    entry = tk.Entry(canvas_1, font=('TKDefaul', 20, 'bold'))
    entry.pack()

    login_btn = tk.Button(canvas_1, bd=0, text='Enter', bg='black', fg='white', font=fnt.Font(size=15),
                          highlightthickness=0, activebackground="grey", activeforeground="white", command=count)
    login_btn.pack()

    root.mainloop()

    return get_watcher()


def gui():
    while True:
        watcher = nb_votes()

        print(watcher, )
        gui.scr_A = 0
        gui.scr_B = 0

        with open('main_db.json', 'r') as readfile:
            rawdata = readfile.read()
            data = json.loads(rawdata)
            idx1 = random.randrange(0, int(numberOfFilm))
            idx2 = random.randrange(0, int(numberOfFilm))
            film1 = data[idx1]
            film2 = data[idx2]

        def result(film):

            def restart():
                rootfinal.destroy()
                gui()
                exit()

            rootfinal = tk.Tk()
            rootfinal.geometry('1000x1200')
            rootfinal.title('MOVIE PICKER')
            canvas_f = tk.Canvas(rootfinal, bg="black", bd=0, relief='ridge')
            canvas_f.pack(expand=True, fill=tk.BOTH)
            canvas_f.configure(highlightthickness=0)
            if film == 'N':
                restart()

            response = requests.get(film['Image Link'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((500, 800), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas_f.create_image(270, 150, anchor='nw', image=img)

            winner_name = tk.Label(canvas_f, text=f"The winner is: ",
                                   bg='black', fg='white', font=fnt.Font(size=15))

            winner_name2 = tk.Label(canvas_f, text=f"{film['name']}",
                                    bg='black', fg='white', font=fnt.Font(size=20), wraplength=600)
            quit_fbt = tk.Button(canvas_f, text="Click to quit", bd=0, highlightthickness=0,
                                 activebackground="grey", activeforeground="white", bg="black", fg="white",
                                 font=fnt.Font(size=15),
                                 command=exit)

            replay_fbt = tk.Button(canvas_f, text="Click to restart", bd=0, highlightthickness=0,
                                   activebackground="#ad1f42", activeforeground="white", bg="red", fg="white",
                                   font=fnt.Font(size=15),
                                   command=restart)
            winner_name.pack()
            winner_name2.pack()
            quit_fbt.pack(side='bottom', pady=40)
            replay_fbt.pack(side='bottom')

            rootfinal.mainloop()
            exit()

        def toggle_textf1():
            if Plus_info_f1['text'] == "+ d'info":
                Plus_info_f1['text'] = f"Date: {film2['year']}, " \
                                       f"Genre: {film2['genre']},\n" \
                                       f"Rating: {film2['ratings']},\n" \
                                       f"Starring: {film2['actors']} \n" \
                                       f"Resume: {film2['resume']} \n\n" \
                                       f"limit age: {film2['certificate']}, runtime: {film2['runtime']}"
                Plus_info_f1.configure(height=10, width=55, justify='left')
                Plus_info_f1.place(x=0, y=140)
            else:
                Plus_info_f1['text'] = "+ d'info"
                Plus_info_f1.configure(height=1, width=8)
                Plus_info_f1.place(x=370, y=140)

        def toggle_textf2():
            if Plus_info_f2['text'] == "+ d'info":
                Plus_info_f2['text'] = f"Date: {film1['year']}, " \
                                       f"Genre: {film1['genre']},\n" \
                                       f"Rating: {film1['ratings']},\n" \
                                       f"Starring: {film1['actors']} \n" \
                                       f"Resume: {film1['resume']} \n\n" \
                                       f"limit age: {film1['certificate']}, runtime: {film1['runtime']}"
                Plus_info_f2.configure(height=10, width=55, justify='left')
                Plus_info_f2.place(x=960, y=140)
            else:
                Plus_info_f2['text'] = "+ d'info"
                Plus_info_f2.configure(height=1, width=8)
                Plus_info_f2.place(x=1500, y=140)

        def vote_a():
            gui.scr_A += 1
            Nb_Vote_A = tk.Label(canvas_1, text='Votes: ' + str(gui.scr_A),
                                 bg='black', fg='white', font=fnt.Font(size=20))
            Nb_Vote_A.place(x=1450, y=1140)
            if gui.scr_A + gui.scr_B > watcher:
                exit(1)
            if gui.scr_A + gui.scr_B == watcher:
                canvas_1.destroy()
                root.destroy()
                if gui.scr_A > gui.scr_B:
                    result(film1)
                elif gui.scr_A < gui.scr_B:
                    result(film2)
                else:
                    result('N')

        def vote_b():
            gui.scr_B += 1
            Nb_Vote_B = tk.Label(canvas_1, text='Votes: ' + str(gui.scr_B),
                                 bg='black', fg='white', font=fnt.Font(size=20))
            Nb_Vote_B.place(x=335, y=1140)
            if gui.scr_A + gui.scr_B > watcher:
                exit(1)
            if gui.scr_A + gui.scr_B == watcher:
                canvas_1.destroy()
                root.destroy()
                if gui.scr_A > gui.scr_B:
                    result(film1)
                elif gui.scr_A < gui.scr_B:
                    result(film2)
                else:
                    result('N')

        root = tk.Tk()

        root.title("MOVIE PICKER: Help you to choose the best film for your party")
        root.geometry("2000x1400+400+000")

        canvas_1 = tk.Canvas(root, bg="black", bd=0, relief='ridge')
        canvas_1.pack(expand=True, fill=tk.BOTH)
        canvas_1.configure(highlightthickness=0)

        bienvenu1_lbl = tk.Label(canvas_1, text='Welcome To MOVIE Picker',
                                 bg='black', fg='white', font=fnt.Font(size=20))
        bienvenu1_lbl.pack()

        bienvenu2_lbl = tk.Label(canvas_1,
                                 text='Participants: '
                                      + str(watcher) +
                                      '. In order to vote, please click on Film pictures',
                                 bg='black', fg='white', font=fnt.Font(size=15))
        bienvenu2_lbl.pack()

        response1 = requests.get(film1['Image Link'])
        img_data1 = response1.content
        img1 = Image.open(BytesIO(img_data1))
        img1 = img1.resize((500, 800), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        # canvas_1.create_image(1300, 200, anchor='nw', image=img1)
        vote_A = tk.Button(canvas_1, bd=0, highlightthickness=0, text="", image=img1,
                           bg="black", activebackground="black",
                           command=vote_a)
        vote_A.place(x=1300, y=220)

        response2 = requests.get(film2['Image Link'])
        img_data2 = response2.content
        img2 = Image.open(BytesIO(img_data2))
        img2 = img2.resize((500, 800), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)
        # canvas_1.create_image(200, 200, anchor='nw', image=img2)
        vote_B = tk.Button(canvas_1, bd=0, highlightthickness=0, text="", image=img2,
                           activebackground="black", bg="black",
                           command=vote_b)

        vote_B.place(x=200, y=220)

        Plus_info_f1 = tk.Button(canvas_1, text="+ d'info",
                                 bd=0, highlightthickness=0, activebackground="grey", wraplength=900,
                                 activeforeground="white", bg="black", fg="white",
                                 command=toggle_textf1)

        Plus_info_f2 = tk.Button(canvas_1, text="+ d'info",
                                 bd=0, highlightthickness=0, activebackground="grey", wraplength=900,
                                 activeforeground="white", bg="black", fg="white",
                                 command=toggle_textf2)

        quit_bt = tk.Button(canvas_1, text="quit", bd=0, highlightthickness=0, activebackground="#ad1f42",
                            activeforeground="white", bg="red", fg="white", font=fnt.Font(size=15), relief='groove',
                            command=exit)

        Plus_info_f2.place(x=1500, y=140)
        Plus_info_f1.place(x=370, y=140)
        quit_bt.pack(side='bottom', pady=40)
        root.mainloop()
        exit()


if __name__ == '__main__':
    t1 = Thread(target=fetch_database())
    t2 = Thread(target=gui())
    t2.start()
    t1.start()
