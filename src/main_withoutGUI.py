import time  # To delete

import random
import re
from io import open
from sys import exit
import requests
import json
from threading import Thread
from bs4 import BeautifulSoup

numberOfFilm = str(250)
URL = f"https://www.imdb.com/search/title?title_type=feature&sort=num_votes,desc&count={numberOfFilm}"


def check_choice(user_entry):
    if not user_entry.isalpha():
        print("You job was to choose between y or n...")
        exit(1)

    if user_entry == 'y' or user_entry == 'yes' or user_entry == 'oui':
        return 1
    elif user_entry == 'n' or user_entry == 'no' or user_entry == 'non':
        return 2
    else:
        print("You job was to choose between y or n...")
        exit(1)


def result(Vote1, title1, Vote2, title2):
    if Vote1 > Vote2:
        print("Vote 1 has been chosen with " + str(Vote1) + " votes")
        print("You will watch " + title1)
    elif Vote2 > Vote1:
        print("Vote 2 has been chosen with " + str(Vote2) + " votes")
        print("You will watch " + title2)
    else:
        secondturn = input("Well, the choice seems complicated, vote again? (y/n) ")
        choice = check_choice(secondturn)
        if choice == 1:
            voting(title1, title2)

        elif choice == 2:
            print("Let's compare other film")
            return

    final_input = input('Are you happy with you final choice?(y/n) ')
    final_choice = check_choice(final_input)
    if final_choice == 1:
        print('Goodbye!')
        exit()
    elif final_choice == 2:  # no
        print("Well, let's all start from the beginning")


def voting(title1, title2):
    print("Voting Time:")
    while True:
        countVote1 = input("How many people want " + title1 + " ")
        countVote2 = input("How many people want " + title2 + " ")

        try:
            if countVote2 == '' or countVote1 == '':
                print("You have to enter something ...")
            countVote1 = int(countVote1)
            countVote2 = int(countVote2)
            if countVote2 == countVote1 or countVote2 > countVote1 or countVote1 > countVote2:
                break

        except ValueError:
            print("Choose only number")

    result(countVote1, title1, countVote2, title2)


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

            years = m.find("span", attrs={"class": "lister-item-year"}).text[1:-1]

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


def main():
    while True:

        with open('main_db.json', 'r') as readfile:
            rawdata = readfile.read()
            data = json.loads(rawdata)
            idx1 = random.randrange(0, int(numberOfFilm))
            idx2 = random.randrange(0, int(numberOfFilm))
            film1 = data[idx1]
            film2 = data[idx2]

        print(f"Vote1: "
              f"{film1['name']} {film1['year']}, "
              f"Genre: {film1['genre']}, "
              f"Rating: {film1['ratings']}, "
              f"Starring: {film1['actors']}")

        print(f"Vote2: "
              f"{film2['name']} {film2['year']}, "
              f"Genre: {film1['genre']}, "
              f"Rating: {film2['ratings']}, "
              f"Starring: {film2['actors']} "
              )
        user_input = ''
        while user_input != 'y' or user_input != 'n':
            user_input = input('Do you want to vote on this choice (y/n)? ')
            user_choice = check_choice(user_input)
            if user_choice == 1:
                title1 = film1['name']
                title2 = film2['name']
                voting(title1, title2)
                break
            elif user_choice == 2:
                break


if __name__ == '__main__':
    t1 = Thread(target=fetch_database())
    t2 = Thread(target=main())
    t2.start()
    t1.start()
    t2.join()
    t1.join()
