import os
import pickle
import tkinter as tk
import numpy as np
import random
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image,ImageTk
from pygame import mixer
import mutagen
from mutagen.mp3 import MP3
import time

class Player(tk.Frame):
        def __init__(self, master=None):
                super().__init__(master)
                self.master = master
                self.pack()
                mixer.init()

                if os.path.exists('songs.pickle'):
                        with open('songs.pickle', 'rb') as f:
                                self.playlist = pickle.load(f)
                else:
                        self.playlist=[]

                self.current = 0
                self.paused = True
                self.played = False

                self.create_frames()
                self.track_widgets()
                self.control_widgets()
                self.tracklist_widgets()

        def create_frames(self):
                self.track = tk.LabelFrame(self, text='Song Track',font=("times new roman",16,"bold"),bg="grey20",fg="white",bd=5,relief=tk.GROOVE)
                self.track.config(width=100,height=100)
                self.track.grid(row=0, column=1, padx=10)

                self.tracklist = tk.LabelFrame(self, text=f'PlayList',font=("times new roman",15,"bold"),bg="grey20",fg="white",bd=5,relief=tk.GROOVE)
                self.tracklist.config(width=100,height=100)
                self.tracklist.grid(row=0, column=0, rowspan=3 ,pady=5)
                
                self.controls = tk.LabelFrame(self,font=("Lucida Console",15,"bold"),bg="grey20",fg="white",bd=4,relief=tk.GROOVE)
                self.controls.config(width=100,height=100)
                self.controls.grid(row=1, column=1, pady=3, padx=15)

        def track_widgets(self):
                self.canvas = tk.Label(self.track, image=img)
                self.canvas.configure(width=400, height=240)
                self.canvas.grid(row=0,column=0)

                self.songtrack = tk.Label(self.track, font=("Lucida Console",10,"bold"),bg="grey20",fg="white")
                self.songtrack['text'] = 'Music bee MP3 Player'
                self.songtrack.config(width=30, height=2,borderwidth=1, relief="solid")
                self.songtrack.grid(row=1,column=0,padx=10)

                self.duration = tk.Label(self.track, font=("times",10,"bold"),bg="grey20",fg="white")
                self.duration['text'] = 'Hear it…See it…LIVE it'
                self.duration.config(width=30, height=2,borderwidth=1, relief="solid")
                self.duration.grid(row=2,column=0,padx=10)

        def control_widgets(self):
                self.loadSongs = tk.Button(self.controls, bg='grey20', fg='white', font=("times new roman",12))
                self.loadSongs['text'] = 'Load Playlist'
                self.loadSongs['command'] = self.retrieve_songs
                self.loadSongs.grid(row=0, column=5, padx=10)

                self.prev = tk.Button(self.controls, image=prev)
                self.prev['command'] = self.prev_song
                self.prev.grid(row=0, column=1)

                self.pause = tk.Button(self.controls, image=pause)
                self.pause['command'] = self.pause_song
                self.pause.grid(row=0, column=2)

                self.next = tk.Button(self.controls, image=next_)
                self.next['command'] = self.next_song
                self.next.grid(row=0, column=3)

                self.next = tk.Button(self.controls, image=newshuffle_image)
                self.next['command'] = self.shuffle_songs
                self.next.grid(row=0, column=4)
                

                self.volume = tk.DoubleVar(self)
                self.slider = tk.Scale(self.controls, from_ = 0, to = 10, orient = tk.HORIZONTAL,bg = "grey20",fg ="grey99")
                self.slider['variable'] = self.volume
                self.slider.set(8)
                mixer.music.set_volume(0.8)
                self.slider['command'] = self.change_volume
                self.slider.grid(row=0, column=0, padx=5)
                
        def tracklist_widgets(self):
                self.scrollbar = tk.Scrollbar(self.tracklist, orient=tk.VERTICAL)
                self.scrollbar.grid(row=0,column=1, rowspan=5, sticky='ns')

                self.list = tk.Listbox(self.tracklist, selectmode=tk.SINGLE,yscrollcommand=self.scrollbar.set, selectbackground='sky blue')
                self.enumerate_songs()
                self.list.config(height=22)
                self.list.bind('<Double-1>', self.play_song) 

                self.scrollbar.config(command=self.list.yview)
                self.list.grid(row=0, column=0, rowspan=5)

        def retrieve_songs(self):
                self.songlist = []
                directory = filedialog.askdirectory()
                for root_, dirs, files in os.walk(directory):
                                for file in files:
                                        if os.path.splitext(file)[1] == '.mp3':
                                                path = (root_ + '/' + file).replace('\\','/')
                                                self.songlist.append(path)

                with open('songs.pickle', 'wb') as f:
                        pickle.dump(self.songlist, f)
                self.playlist = self.songlist
                self.tracklist['text'] = f'PlayList - {str(len(self.playlist))}'
                self.list.delete(0, tk.END)
                self.enumerate_songs()

        def enumerate_songs(self):
                for index, song in enumerate(self.playlist):
                        self.list.insert(index, os.path.basename(song))

        def play_song(self, event=None):
                if event is not None:
                        self.current = self.list.curselection()[0]
                        for i in range(len(self.playlist)):
                                self.list.itemconfigure(i, bg="white")

                print(self.playlist[self.current])
                mixer.music.load(self.playlist[self.current])
                self.songtrack['anchor'] = 'w' 
                self.songtrack['text'] = os.path.basename(self.playlist[self.current])
                audio = MP3(self.playlist[self.current])
                audio_info = audio.info
                length = int(audio_info.length)
                hours, mins, seconds = self.audio_duration(length)
                self.duration['text'] =f'Total Duration: {mins}:{seconds}'
                sec = (mins*60)+seconds
                self.pause['image'] = play
                self.paused = False
                self.played = True
                self.list.activate(self.current) 
                self.list.itemconfigure(self.current, bg='sky blue')
                mixer.music.play()
                    

        def pause_song(self):
                if not self.paused:
                        self.paused = True
                        mixer.music.pause()
                        self.pause['image'] = pause
                else:
                        if self.played == False:
                                self.play_song()
                        self.paused = False
                        mixer.music.unpause()
                        self.pause['image'] = play

        def prev_song(self):
                if self.current > 0:
                        self.current -= 1
                else:
                        self.current = 0
                self.list.itemconfigure(self.current + 1, bg='white')
                self.play_song()

        def next_song(self):
                if self.current < len(self.playlist) - 1:   
                        self.current += 1
                else:
                        self.current = 0
                self.list.itemconfigure(self.current - 1, bg='white')
                self.play_song()

        def change_volume(self, event=None):
                self.v = self.volume.get()
                mixer.music.set_volume(self.v / 10)

        def shuffle_songs(self):
                random.shuffle(self.playlist)
                self.list.delete(0, tk.END)
                self.enumerate_songs()
                print(self.playlist)
                mixer.music.load(self.playlist[0])
                self.songtrack['anchor'] = 'w' 
                self.songtrack['text'] = os.path.basename(self.playlist[0])
                audio = MP3(self.playlist[0])
                audio_info = audio.info
                length = int(audio_info.length)
                hours, mins, seconds = self.audio_duration(length)
                self.duration['text'] =f'Total Duration: {mins}:{seconds}'
                self.pause['image'] = play
                self.paused = False
                self.played = True
                self.current = 0
                mixer.music.play()

        def audio_duration(self,length):
                hours = length // 3600
                length %= 3600
                mins = length // 60
                length %= 60
                seconds = length

                return hours, mins, seconds

                
                

root = tk.Tk()
root.geometry('650x400')
root.wm_title('Music Player')
root.configure(bg='grey20')
root.resizable(0,0)

img = PhotoImage(file='images/ffff.gif')

newNext_image = Image.open("images/nex.jpg")
next_image= newNext_image.resize((35,40), Image.ANTIALIAS)
next_= ImageTk.PhotoImage(next_image)

newPrev_image = Image.open("images/prev.png")
prev_image= newPrev_image.resize((35,40), Image.ANTIALIAS)
prev= ImageTk.PhotoImage(prev_image)

newPlay_image = Image.open("images/plaaa.jpg")
play_image= newPlay_image.resize((35,40), Image.ANTIALIAS)
play= ImageTk.PhotoImage(play_image)

newPause_image = Image.open("images/paus.jpg")
pause_image= newPause_image.resize((35,40), Image.ANTIALIAS)
pause= ImageTk.PhotoImage(pause_image)

shuffle = Image.open("images/shuff.jpg")
shuffle_image= shuffle.resize((35,40), Image.ANTIALIAS)
newshuffle_image= ImageTk.PhotoImage(shuffle_image)

app = Player(master=root)
app.configure(bg='grey20')
app.mainloop()

