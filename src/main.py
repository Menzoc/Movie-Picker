import random
import re
import sys
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


def choose_in_database(genre='', rates='', runtime_min='', runtime_max='', year=''):
    # Manage to pass in int
    try:
        rates = int(rates)
    except ValueError:
        rates = 0.0
    try:
        runtime_min = int(runtime_min)
    except ValueError:
        runtime_min = 0.0
    try:
        runtime_max = int(runtime_max)
    except ValueError:
        runtime_max = 10000.0
    try:
        year = int(year)
    except ValueError:
        year = 0

    with open('main_db.json', 'r') as readfile:
        rawdata = readfile.read()
        data = json.loads(rawdata)
    correspond_film = []

    for i in range(0, numberOfFilm):
        liste_genre = data[i]['genre'].split(', ')
        runtime_db = int(data[i]['runtime'].split()[0])
        if (genre in liste_genre or genre == '') and \
                (float(data[i]['ratings']) >= rates or rates == 0.0) and \
                (runtime_min <= runtime_db <= runtime_max) and \
                (year == int(data[i]['year']) or year == 0):
            correspond_film.append(i)
    return correspond_film


def nb_votes():
    nb_votes.list_film_possible = 0

    # RESTART ##################################

    def restart():
        root.destroy()
        gui()

    # ENTRY BUTTON ##################################

    def count():

        count.year = entry_year.get()
        count.min_t = min_time.get()
        count.max_t = max_time.get()
        count.rates = rates_c.get()
        count.watcher = entry.get()

        if int(count.watcher) != 0 and \
                (count.year == '' or int(count.year) != 0) and \
                (count.rates == '' or 0 < int(count.rates) <= 10):
            root.destroy()

    # GET VALUE ##################################

    def get_watcher():
        return int(count.watcher)

    # START PAGE ##################################
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    a_b = screen_width / 3200
    b_b = screen_height / 1800
    geo1_b = str(int(1400 * a_b))
    geo2_b = str(int(1200 * b_b))
    root.geometry(geo1_b + "x" + geo2_b)
    root.title('MOVIE PICKER')
    canvas_1 = tk.Canvas(root, bg="black", bd=0, relief='ridge')
    canvas_1.pack(expand=True, fill=tk.BOTH)
    canvas_1.configure(highlightthickness=0)
    canvas_2 = tk.Canvas(root, bg="black", bd=0, relief='ridge')
    canvas_2.pack(expand=True, fill=tk.BOTH)
    canvas_2.configure(highlightthickness=0)

    # ORGANIZE TEXT - genre ##################################
    def disabled():
        R1['state'] = 'disabled'
        R2['state'] = 'disabled'
        R3['state'] = 'disabled'
        R4['state'] = 'disabled'
        R5['state'] = 'disabled'
        R6['state'] = 'disabled'
        R7['state'] = 'disabled'
        R8['state'] = 'disabled'
        R9['state'] = 'disabled'
        R10['state'] = 'disabled'

    genre = tk.StringVar()
    R1 = tk.Radiobutton(canvas_1, text="Comedy", variable=genre, value='Comedy', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R2 = tk.Radiobutton(canvas_1, text="Adventure", variable=genre, value='Adventure', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R3 = tk.Radiobutton(canvas_1, text="Action", variable=genre, value='Action', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R4 = tk.Radiobutton(canvas_1, text="Crime", variable=genre, value='Crime', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R5 = tk.Radiobutton(canvas_1, text="Horror", variable=genre, value='Horror', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R6 = tk.Radiobutton(canvas_1, text="Fantasy", variable=genre, value='Fantasy', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R7 = tk.Radiobutton(canvas_1, text="Science-Fiction", variable=genre, value='Sci-Fi', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R8 = tk.Radiobutton(canvas_1, text="Thriller", variable=genre, value='Thriller', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R9 = tk.Radiobutton(canvas_1, text="Drama", variable=genre, value='Drama', command=disabled,
                        bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)
    R10 = tk.Radiobutton(canvas_1, text="Romance", variable=genre, value='Romance', command=disabled,
                         bg='black', fg='white', font=fnt.Font(size=15), highlightthickness=0)

    R1.grid(row=0, column=0)
    R2.grid(row=0, column=1)
    R3.grid(row=0, column=2)
    R4.grid(row=0, column=3)
    R5.grid(row=0, column=4)
    R6.grid(row=1, column=0)
    R7.grid(row=1, column=1)
    R8.grid(row=1, column=2)
    R9.grid(row=1, column=3)
    R10.grid(row=1, column=4)

    # ORGANIZE TEXT - rates ##################################
    tk.Label(canvas_2, text=" ", bg='black', fg='white', font=fnt.Font(size=15)).pack()
    rates_lbl = tk.Label(canvas_2, text="What is the minimum rates for your film: ",
                         bg='black', fg='white', font=fnt.Font(size=15))
    details_rates_lbl = tk.Label(canvas_2, text="He has to be between 0(bad) and 10(excellent)",
                                 bg='black', fg='white', font=fnt.Font(size=10))
    rates_c = tk.Entry(canvas_2, font=('TKDefaul', 20, 'bold'))
    rates_lbl.pack()
    details_rates_lbl.pack()
    rates_c.pack()
    tk.Label(canvas_2, text=" ", bg='black', fg='white', font=fnt.Font(size=15)).pack()

    # ORGANIZE TEXT - timer ##################################
    uptime_lbl = tk.Label(canvas_2, text="How many time do you have to watch the film: ",
                          bg='black', fg='white', font=fnt.Font(size=15))
    uptime_lbl.pack()
    min_lbl = tk.Label(canvas_2, text="Time minimum in minutes ",
                       bg='black', fg='white', font=fnt.Font(size=15))
    max_lbl = tk.Label(canvas_2, text="Time maximum in minutes",
                       bg='black', fg='white', font=fnt.Font(size=15))
    min_time = tk.Entry(canvas_2, font=('TKDefaul', 20, 'bold'))
    max_time = tk.Entry(canvas_2, font=('TKDefaul', 20, 'bold'))
    min_lbl.pack()
    min_time.pack()
    max_lbl.pack()
    max_time.pack()
    tk.Label(canvas_2, text=" ", bg='black', fg='white', font=fnt.Font(size=15)).pack()

    # ORGANIZE TEXT - year ##################################
    year_lbl = tk.Label(canvas_2, text="You can write the released date on the films",
                        bg='black', fg='white', font=fnt.Font(size=15))
    year_lbl.pack()
    entry_year = tk.Entry(canvas_2, font=('TKDefaul', 20, 'bold'))
    entry_year.pack()

    # ORGANIZE TEXT - watcher ##################################
    bienvenu1_lbl = tk.Label(canvas_2, text='Please, enter the numbers of participants',
                             bg='black', fg='white', font=fnt.Font(size=15))
    bienvenu1_lbl.pack()

    entry = tk.Entry(canvas_2, font=('TKDefaul', 20, 'bold'))
    entry.pack(padx=20)

    # GESTION BUTTON ##################################
    canvas_3 = tk.Canvas(canvas_2, bg="black", bd=0, relief='ridge')
    canvas_3.pack(expand=True, fill=tk.Y)
    canvas_3.configure(highlightthickness=0)
    login_btn = tk.Button(canvas_3, bd=0, text='Enter', bg='black', fg='white', font=fnt.Font(size=20),
                          highlightthickness=0, activebackground="grey", activeforeground="white", command=count)
    restart_btn = tk.Button(canvas_3, bd=0, text='Restart', bg='black', fg='white', font=fnt.Font(size=20),
                            highlightthickness=0, activebackground="grey", activeforeground="white", command=restart)
    # END FIRST PAGE ##################################
    login_btn.grid(row=0, column=0, sticky=tk.W)
    restart_btn.grid(row=0, column=1, sticky=tk.W)
    root.mainloop()

    # GET POSSIBILITY ##################################

    if count.watcher != 0:
        nb_votes.list_film_possible = choose_in_database(genre=genre.get(),
                                                         year=count.year,
                                                         runtime_min=count.min_t,
                                                         runtime_max=count.max_t,
                                                         rates=count.rates)
    print(nb_votes.list_film_possible)
    print(len(nb_votes.list_film_possible))

    return get_watcher(), nb_votes.list_film_possible


def gui():
    while True:
        watcher, list_film = nb_votes()
        print(watcher)
        flag_One_film = 0
        gui.scr_A = 0
        gui.scr_B = 0

        if len(list_film) == 1:
            flag_One_film = 1
        with open('main_db.json', 'r') as readfile:
            rawdata = readfile.read()
            data = json.loads(rawdata)
            if len(list_film) == 1:
                film1 = data[list_film[0]]
                film2 = data[list_film[0]]
            elif len(list_film) != 0:
                idx1 = random.randrange(0, int(len(list_film)))
                film1 = data[list_film[idx1]]
                list_film.remove(list_film[idx1])
                idx2 = random.randrange(0, int(len(list_film)))
                film2 = data[list_film[idx2]]
            else:
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
            screen_width_res = rootfinal.winfo_screenwidth()
            screen_height_res = rootfinal.winfo_screenheight()
            a_r = screen_width_res / 3200
            b_r = screen_height_res / 1800
            geo1_r = str(int(1000 * a_r))
            geo2_r = str(int(1300 * b_r))
            rootfinal.geometry(geo1_r+'x'+geo2_r)
            rootfinal.title('MOVIE PICKER')
            canvas_f = tk.Canvas(rootfinal, bg="black", bd=0, relief='ridge')
            canvas_f.pack(expand=True, fill=tk.BOTH)
            canvas_f.configure(highlightthickness=0)
            if film == 'N':
                restart()

            response = requests.get(film['Image Link'])
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img = img.resize((int(a * 500), int(b * 800)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            canvas_f.create_image(int(a * 270), int(b * 200), anchor='nw', image=img)

            winner_name = tk.Label(canvas_f, text=f"The winner is: ",
                                   bg='black', fg='white', font=fnt.Font(size=15))

            winner_name2 = tk.Label(canvas_f, text=f"{film['name']}", wraplength=600,
                                    bg='black', fg='white', font=fnt.Font(size=20))
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
            quit_fbt.pack(side='bottom', pady=int(a_r * 40))
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
                if sys.platform == 'linux':
                    Plus_info_f1.configure(height=int(a * 10), width=int(b * 55), justify='left')
                    Plus_info_f1.place(x=int(a * 5), y=int(b * 140))
                else:
                    Plus_info_f1.configure(height=int(a * 20), width=int(b * 150), justify='left')
                    Plus_info_f1.place(x=int(a * 25), y=int(b * 140))
            else:
                Plus_info_f1['text'] = "+ d'info"
                if sys.platform == 'linux':
                    Plus_info_f1.configure(height=int(a * 1), width=int(b * 8))
                    Plus_info_f1.place(x=int(a * 370), y=int(b * 140))
                else:
                    Plus_info_f1.configure(height=int(a * 1), width=int(b * 15))
                    Plus_info_f1.place(x=int(a * 370), y=int(b * 140))

        def toggle_textf2():
            if Plus_info_f2['text'] == "+ d'info":
                Plus_info_f2['text'] = f"Date: {film1['year']}, " \
                                       f"Genre: {film1['genre']},\n" \
                                       f"Rating: {film1['ratings']},\n" \
                                       f"Starring: {film1['actors']} \n" \
                                       f"Resume: {film1['resume']} \n\n" \
                                       f"limit age: {film1['certificate']}, runtime: {film1['runtime']}"
                if sys.platform == 'linux':
                    Plus_info_f2.configure(height=int(a * 10), width=int(b * 55), justify='left')
                    Plus_info_f2.place(x=int(a * 1000), y=int(b * 140))
                else:
                    Plus_info_f2.configure(height=int(a * 20), width=int(b * 150), justify='left')
                    Plus_info_f2.place(x=int(a * 1000), y=int(b * 140))
            else:
                Plus_info_f2['text'] = "+ d'info"
                if sys.platform == 'linux':
                    Plus_info_f2.configure(height=int(a * 1), width=int(b * 8))
                    Plus_info_f2.place(x=int(a * 1500), y=int(b * 140))
                else:
                    Plus_info_f2.configure(height=int(a * 1), width=int(b * 15))
                    Plus_info_f2.place(x=int(a * 1500), y=int(b * 140))

        def vote_a():
            gui.scr_A += 1
            Nb_Vote_A = tk.Label(canvas_1, text='Votes: ' + str(gui.scr_A),
                                 bg='black', fg='white', font=fnt.Font(size=20))
            Nb_Vote_A.place(x=int(a * 1450), y=int(b * 1140))
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
            Nb_Vote_B.place(x=int(a * 335), y=int(b * 1140))
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

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        a = screen_width / 3200
        b = screen_height / 1800
        geo1 = str(int(2000 * a))
        geo2 = str(int(1400 * b))
        root.title("MOVIE PICKER: Help you to choose the best film for your party")
        root.geometry(geo1 + "x" + geo2)

        canvas_1 = tk.Canvas(root, bg="black", bd=0, relief='ridge')
        canvas_1.pack(expand=True, fill=tk.BOTH)
        canvas_1.configure(highlightthickness=0)

        if flag_One_film == 1:
            error_lbl = tk.Label(canvas_1, text="Your criteria are too restrictive, 1 match only. You can see it:",
                                 bg='black', fg='red', font=fnt.Font(size=10))
            error_lbl.pack()
        elif len(list_film) == 0:
            error_lbl = tk.Label(canvas_1, text="Your criteria are too restrictive. They have not been aaplied",
                                 bg='black', fg='red', font=fnt.Font(size=10))
            error_lbl.pack()

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
        img1 = img1.resize((int(a * 500), int(b * 800)), Image.ANTIALIAS)
        img1 = ImageTk.PhotoImage(img1)
        vote_A = tk.Button(canvas_1, bd=0, highlightthickness=0, text="", image=img1,
                           bg="black", activebackground="black",
                           command=vote_a)
        vote_A.place(x=int(1300 * a), y=int(b * 220))

        response2 = requests.get(film2['Image Link'])
        img_data2 = response2.content
        img2 = Image.open(BytesIO(img_data2))
        img2 = img2.resize((int(500 * a), int(800 * b)), Image.ANTIALIAS)
        img2 = ImageTk.PhotoImage(img2)
        vote_B = tk.Button(canvas_1, bd=0, highlightthickness=0, text="", image=img2,
                           activebackground="black", bg="black",
                           command=vote_b)

        vote_B.place(x=int(a * 200), y=int(b * 220))

        if sys.platform == 'linux':
            wrapvar = 900
        else:
            wrapvar = 400

        Plus_info_f1 = tk.Button(canvas_1, text="+ d'info",
                                 bd=0, highlightthickness=0, activebackground="grey", wraplength=wrapvar,
                                 activeforeground="white", bg="black", fg="white",
                                 command=toggle_textf1)

        Plus_info_f2 = tk.Button(canvas_1, text="+ d'info",
                                 bd=0, highlightthickness=0, activebackground="grey", wraplength=wrapvar,
                                 activeforeground="white", bg="black", fg="white",
                                 command=toggle_textf2)

        quit_bt = tk.Button(canvas_1, text="quit", bd=0, highlightthickness=0, activebackground="#ad1f42",
                            activeforeground="white", bg="red", fg="white", font=fnt.Font(size=15), relief='groove',
                            command=exit)

        Plus_info_f2.place(x=int(1500 * a), y=int(140 * b))
        Plus_info_f1.place(x=int(a * 370), y=int(b * 140))
        quit_bt.pack(side='bottom', pady=int(b * 40))
        root.mainloop()
        exit()


if __name__ == '__main__':
    t1 = Thread(target=fetch_database())
    t2 = Thread(target=gui())
    t2.start()
    t1.start()
    t2.join()
    t1.join()
