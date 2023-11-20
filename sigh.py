#importing stuff
from datetime import datetime
import os
import subprocess
import pathlib
import threading
from tkinter import *
import pygame
from pygame import *
from pygame import mixer
from numpy import argmax
import time
import csv

#initialising Pygame
pygame.init()

#setting up the fonts 
title_font = pygame.font.Font("Fonts/ProductSans-Bold.ttf", 40)
msg_font = pygame.font.Font("Fonts/Gotham-Light.otf", 25)

# setting up some colors
spotify_green = (50, 150, 150)
background = (14, 15, 14)
grey = (101, 117, 105)

# initializing window 
screen = pygame.display.set_mode((1000, 650))
pygame.display.set_caption("GrooveSphere")
icon = pygame.image.load("Resources/groove.png")
pygame.display.set_icon(icon)

# The welcoming window
def welcome():

    data = open("Python_files/data.csv", "r")
    csvr = csv.reader(data)
    if csvr == '':
        data.close()

        # Welcome Screen 
        title = title_font.render("Welcome To GrooveSphere!", True, spotify_green)
        screen.blit(title, (250,250))

        msg = msg_font.render("You can close this window and continue the app in the console!!", True, grey)
        screen.blit(msg, (100, 310) )
        
        spotify_logo = pygame.image.load("Resources/groove.png")
        spotify_logo = pygame.transform.scale(spotify_logo, (100, 100))
        screen.blit(spotify_logo, (400, 100))

    else:
        data = open("Python_files/data.csv", "r")
        csvr = csv.reader(data)
        now = datetime.now()
        current_time = now.strftime("%H")
    
        name = csvr[0]

        # Welcome Screen 
        title = title_font.render(f"{greet(current_time)} {name.title()}!", True, spotify_green)
        screen.blit(title, (250,250))

        msg = msg_font.render("You can close this window and continue the app in the console!!", True, grey)
        screen.blit(msg, (100, 310) )
        
        spotify_logo = pygame.image.load("Resources/groove.png")
        spotify_logo = pygame.transform.scale(spotify_logo, (100, 100))
        screen.blit(spotify_logo, (400, 100))

        data.close()

    #keeping the window alive
    running = True
    while running:

        pygame.display.update()
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

# some handy functions

from bs4 import BeautifulSoup
import requests

def filter_name(string):
    count = 0
    for i in string:
        if i == '_':
            return True
        elif i.isalnum() == False:
            count += 1
            break
    if len(string) <= 2:
        return False 
    if count > 0:
        return False

def remove_links(string):
    for i in string:
        if i == '[':
            ind = string.index(i)
            end_ind = string.index(']')
            replace_part = string[ind:end_ind + 1:1]
            string = string.replace(replace_part, '')

        else:
            pass

    for j in string:
        if j == '\n':
            string = string.replace(j, '')

    return string

def artist_info(artist):
    temp = artist
    artist = artist.title().replace(' ', '_')
    url = f"https://en.wikipedia.org/wiki/{artist}#Artists"

    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    for i in range(1, 5):
        try:
            info = soup.select('div p')[i].get_text()
            if info.strip() == '':
                continue
            else:
                return remove_links(info)
        except (IndexError):
            print("Looks like there is no information about this artist on Wikipedia.")
            break

def get_user_info():
    data = open("data.csv", 'r')
    csvr = csv.reader()
    return csvr

def greet(time):
    time = int(time)

    for hour in range(24):
        if hour < 12:
            if time == hour:
                return "Good Morning"
            else:
                continue
        elif hour < 16:
            if time == hour:
                return "Good Afternoon"
            else:
                continue

        elif hour < 21:
            if time == hour:
                return "Good Evening"
            else:
                continue

        elif hour < 24:
            if time == hour:
                return "Good Night"
            else:
                continue

# song player function
def song_player():
    root = Tk()
    root.title("GrooveSphere")
    root.geometry("500x600")
    root.config(bg = "black")
    photo = PhotoImage(file='Resources/groove.png')
    root.iconphoto(False, photo)

    mixer.init()
    rootpath = "Resources/songs"

    song = Label(root, fg = "grey", bg = "black", font=("", 10))
    song.pack(padx = 10)

    def select():
        song.config(text = "Now Playing: " + menu.get("anchor"))
        mixer.music.load(rootpath + "//" + menu.get("anchor") + '.mp3')
        mixer.music.play()
    def pause():
        mixer.music.pause()
        song.config(text='')

    def next():
        next_song = menu.curselection()
        
        try:
            next_song = next_song[0] + 1
            next_song_name = menu.get(next_song)
            song.config(text=next_song_name)

        except IndexError:
            song.config(text=next_song_name)

        mixer.music.load(rootpath + "//" + next_song_name + '.mp3')
        mixer.music.set_volume(0.7)
        mixer.music.play()

        menu.select_clear(0, 'end')
        menu.activate(next_song)
        menu.select_set(next_song)

    def prev():
        prev_song = menu.curselection()
        try:
            prev_song = prev_song[0] - 1
            prev_song_name = menu.get(prev_song)
            song.config(text=prev_song_name)
            
        except IndexError:
            song.config(text=prev_song_name)

        mixer.music.load(rootpath + "//" + prev_song_name + '.mp3')
        mixer.music.play()

        menu.select_clear(0, 'end')
        menu.activate(prev_song)
        menu.select_set(prev_song)  

    menu = Listbox(root, fg = "purple", bg = "black", font=( "productsans-regular", 15), width = 50)
    menu.pack(pady = 50)

    # getting names
    names = os.listdir("Resources/songs")

    for name in names:
        i = 0
        name = name.replace('.mp3', '')
        menu.insert(i, name)
        i+=1

    top = Frame(root, bg= "black")
    top.pack(padx = 10, pady=5, anchor="center")

    prev_button = Button(root, text='Prev.', bg="black", fg="grey", command= prev)
    prev_button.pack(pady = 10, in_=top, side="left")

    play_button = Button(root, text='Play', bg="black", fg="grey", command= select)
    play_button.pack(pady = 10, in_=top, side="left")

    stop_button = Button(root, text='Stop', bg="black", fg="grey", command = pause)
    stop_button.pack(pady = 10, in_=top, side="left")

    next_button = Button(root, text='Next', bg="black", fg="grey", command = next)
    next_button.pack(pady = 10, in_=top, side="left")

    root.mainloop()

#displaying the welcome window
welcome()

#instructions
instructions = '''Instructions:
            [help] - "Shows the instructions panel."
            [artist info] - "Gives info about the Artist."
            [player] - "Opens the song player."
            [profile] - "Shows the profile."
            [change profile] - "Changes the details of the Profile."
            [add song] - "Lets you add songs to the player."
            [end] - "Closes the app."
            [uninstall] - "Uninstalls the app including all the info." 
        '''

#keeping program alive
alive = True
while alive:

    now = datetime.now()
    current_time = now.strftime("%H")
    greetings = greet(current_time)

    #checking whether the user is already logged in
    data = open("Python_files/data.csv", 'r')
    csvr = csv.reader(data)
    if csvr == '':
        data.close()
        Not_logged = True

    else:
        data = open("Python_files/data.csv", 'r')
        details = csv.reader(data)
        name = details[0]
        Not_logged = False
        print(f"{greetings} {name.title()}!")
        data.close()
        data = open("Python_files/data.csv", "r")
        details = data.read().split(",")

        try:
            username = details[0]
        except IndexError:
            username='not entered'

        try:
            age_value = details[1]
        except IndexError:
            age_value='not entered'
        
        try:
            gender_identity = details[2]
        except IndexError:
            gender_identity='not entered'
        
        try:
            language = details[3]
        except IndexError:
            language='not entered'
        
        global profile

        profile = f'''
            [name] : {username.title()}
            [age] : {age_value}
            [gender] : {gender_identity.title()}
            [language] : {language.title()}
        '''
        data.close()

    if Not_logged:
        # greeting the new user
        print("Welcome to GrooveSphere. Create a profile for yourself to access songs offline!")

        #bringing in the file to write
        data= open("Python_files/data.csv", 'w+')
        writer = csv.writer(data)
        obj = []

        #name
        n = False
        while n == False:
            
            name = input("Enter name: ")
            if filter_name(name) == False:
                print("Name must not contain any special characters and should contain more than or equal to 3 characters.")
                input()
            else:
                username = name
                obj.append(username)
                n = True
        
        #age
        var = False
        while var == False:

            try:
                age = int(input("Enter your age: "))
                if age <= 0 or age > 122:
                    print("Age cannot be negative, zero or more than 122...")
                    continue
                else:
                    age_value = age
                    obj.append(str(age_value))
                    break
            except ValueError:
                print("Bruh age should be an integer...")
                continue
        
        #gender :
        print("Enter your gender down below.")
        time.sleep(1)
        print("Options are : 'Male', 'Female', 'Rather not say'")
        time.sleep(1.3)
        print("Press 'w' to know why we ask gender identity or press 'Enter' to pass.")
        inp = input()
        
        if inp == 'w':
            print('We use your gender to make GrooveSphere services more personal. When you specify your gender, you help us to:')
            print('Personalize messages and other text that refer to you. For example, people who can see your gender will see text like “Send him a message” or “In her circles.”')
        
        N = False
        while N == False:
            gender = input('Gender >>>')
            gender = gender.lower()
            if gender == "male" or gender == "female" or gender == "rather not say":
                gender_identity = gender
                obj.append(gender_identity)
                N = True
            else:
                print("Enter any of the above listed options!")
                continue
        
        #language preference:
        print("Enter the language you are comfortable with (Does not affect the songs).")
        time.sleep(1)
        print("Options are : 1. English, 2. Hindi")
        time.sleep(1.3)
        
        lan = False
        while lan == False:
            lang = input("Language >>>")
            lang = lang.lower()
            if lang == "english" or lang == "hindi":
                language = lang
                obj.append(language)
                writer.writerow(obj)
                data.close()
                lan = True
            else:
                print("Enter any of the above listed options!")
                continue

        profile = f'''
                [name] : {username.title()}
                [age] : {age_value}
                [gender] : {gender_identity.title()}
                [language] : {language.title()}'''

        print("Great! You are good to go!")
        time.sleep(0.5)
        input("Press 'Enter' to continue...")

        # rules and instructions:
        input("Now before we move on let us look at some instructions which might be helpful.")
        print(instructions)    

    # keeping the interface alive
    running = True
    while running:
        command = input(">>>")
        command = command.strip()
    
        def run(choice, info):
            #help command
            if choice == "help":
                
                time.sleep(0.5)
                print(".", end='')
                time.sleep(0.5)
                print(".", end='')
                time.sleep(0.5)
                print(".")
                time.sleep(0.5)

                print(instructions)              

            #info command
            elif choice == "artist info":
                
                artist = input("Enter artist_name>>>")
                print(artist_info(artist))


            elif choice == "profile":
                
                time.sleep(0.5)
                print(".", end='')
                time.sleep(0.5)
                print(".", end='')
                time.sleep(0.5)
                print(".")
                time.sleep(0.5)
                print(info)


            #running the player
            elif choice == "player":
                song_player()

            #changing the profile
            

            elif choice == "add song":

                def add_song():
                    subprocess.Popen('explorer "C:/"') 

                def show_window():
                    root = Tk()
                    root.title("Message")
                    root.geometry("300x50")
                    root.config(bg = "black")
                    photo = PhotoImage(file='Resources/groove.png')
                    root.iconphoto(False, photo)
                    
                    msg = Label(root,text='Add songs here', fg = "grey", bg = "black", font=("", 20))
                    msg.pack(padx = 10, pady=10)

                    root.mainloop()

                threading.Thread(target=add_song).start()
                threading.Thread(target=show_window).start()

                print("Add songs into the resources directory and they will show up in the player next time!")

        options = ['help', 'artist info', 'player', 'profile', 'add song']

        if command in options:
            run(choice=command, info=profile)

        elif command == "change profile":
            data_rewrite = open("Python_files/data.csv", "w")
            print("Enter the new details below. If you do not wish to change a specific detail, then press 'ENTER' to pass.")

            time.sleep(0.5)
            print(".", end='')
            time.sleep(0.5)
            print(".", end='\n')

            nam = True 
            while nam:
                new_name = input("Enter new name>>>")
                if new_name == '':
                    data_rewrite.write(username + ",")
                    break
                else:
                    if filter_name(new_name) == False:
                        print("Name must not contain any special characters and should contain more than or equal to 3 characters.")
                        input()
                    else:
                        nam = False
                        username = new_name
                        data_rewrite.write(username + ',')

            ag = True
            while ag:
                new_age = input("Enter new age>>>")
                if new_age == '':
                    data_rewrite.write(str(age_value)+',')
                    ag = False
                else:
                    try:
                        int(new_age)
                        age_value = new_age
                        data_rewrite.write(age_value+',')
                        ag = False
                    except ValueError:
                        print("Bruh age should be an integer...")
                    
            N = False
            while N == False:
                new_gender = input("Enter new gender>>>")
                new_gender = new_gender.lower()

                if new_gender == "male" or new_gender == "female" or new_gender == "rather not say":
                    gender_identity = new_gender
                    data_rewrite.write(gender_identity+',')
                    N = True
                
                elif new_gender == '':
                    data_rewrite.write(gender_identity+',')
                    break
                
                else:
                    print("Enter any of the above listed options!")
                    continue           
            
            lan = False
            while lan == False:
                new_lang = input("Enter new language>>>")
                new_lang = new_lang.lower()

                if new_lang == '':
                    data_rewrite.write(language+',')
                    break

                elif new_lang == "english" or new_lang == "hindi":
                    language = new_lang
                    data_rewrite.write(language)
                    data_rewrite.close()
                    lan = True
                
                else:
                    print("Enter any of the above listed options!")
                    continue

            profile = f'''
            [name] : {username.title()}
            [age] : {age_value}
            [gender] : {gender_identity.title()}
            [language] : {language.title()}
            '''

        elif command == 'end':
            running = False

        elif command == 'uninstall':
            data = open('Python_files/data.csv', 'w+')
            data.close()
            running = False

        else:
        
            def approx(arg:str, opt:list):
                similarities = []
                
                for j in opt:
                    n_i = 0
                    for i in arg:
                        if i in j:
                            n_i += 1
                    similarities += [n_i]

                return (similarities, argmax(similarities), opt[argmax(similarities)])

            options = ['help', 'artist info', 'player', 'profile', 'add song']
            scores = approx(command, options)

            if scores[0][scores[1]] < len(scores[2])/2:
                print('Invalid choice.')
            else:
                print(f"I think you wanted to type {scores[2]}. So, lemme do it for you.")
                run(choice=scores[2], info=profile)

    alive = False