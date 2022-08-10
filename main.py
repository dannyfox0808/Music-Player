from tkinter import *
from tkinter import ttk
import tkinter as tk
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
#####################################################################



root = Tk()
root.title("iPlayX")
root.geometry("1000x600")
root.config(bg="black")

pygame.mixer.init()

# Grab Song Length Time Info
def play_time():
	# Check for double timing
	if stopped:
		return 
	# Grab Current Song Elapsed Time
	current_time = pygame.mixer.music.get_pos() / 1000

	# throw up temp label to get data
	#slider_label.config(text=f'Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}')
	# convert to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Get Currently Playing Song
	#current_song = song_box.curselection()
	#Grab song title from playlist
	song = song_box.get(ACTIVE)
	# add directory structure and mp3 to song title
	song = f'C:/Users/danny/Music{song}.mp3'
	# Load Song with Mutagen
	song_mut = MP3(song)
	# Get song Length
	global song_length
	song_length = song_mut.info.length
	# Convert to Time Format
	converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

	# Increase current time by 1 second
	current_time +=1
	
	if int(my_slider.get()) == int(song_length):
		status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
	elif paused:
		pass
	elif int(my_slider.get()) == int(current_time):
		# Update Slider To position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(current_time))

	else:
		# Update Slider To position
		slider_position = int(song_length)
		my_slider.config(to=slider_position, value=int(my_slider.get()))
		
		# convert to time format
		converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))

		# Output time to status bar
		status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

		# Move this thing along by one second
		next_time = int(my_slider.get()) + 1
		my_slider.config(value=next_time)






	# Output time to status bar
	#status_bar.config(text=f'Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

	# Update slider position value to current song position...
	#my_slider.config(value=int(current_time))
	
	
	# update time
	status_bar.after(1000, play_time)


#Add Song Function
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	#strip out the directory info and .mp3 extension from the song name
	song = song.replace("C:/Users/danny/Music", "")
	song = song.replace(".mp3", "")

	# Add song to listbox
	song_box.insert(END, song)

# Add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))	

	# Loop thru song list and replace directory info and mp3
	for song in songs:
		song = song.replace("C:/Users/danny/Music", "")
		song = song.replace(".mp3", "")
		# Insert into playlist
		song_box.insert(END, song)

# Play selected song
def play():
	# Set Stopped Variable To False So Song Can Play
	global stopped
	stopped = False
	song = song_box.get(ACTIVE)
	song = f'C:/Users/danny/Music{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Call the play_time function to get song length
	play_time()

	# Update Slider To position
	#slider_position = int(song_length)
	#my_slider.config(to=slider_position, value=0)


# Stop playing current song
global stopped
stopped = False
def stop():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Stop Song From Playing
	pygame.mixer.music.stop()
	song_box.selection_clear(ACTIVE)

	# Clear The Status Bar
	status_bar.config(text='')

	# Set Stop Variable To True
	global stopped
	stopped = True 

# Play The Next Song in the playlist
def next_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)

	# Get the current song tuple number
	next_one = song_box.curselection() 
	# Add one to the current song number
	next_one = next_one[0]+1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'C:/Users/danny/Music{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Play Previous Song In Playlist
def previous_song():
	# Reset Slider and Status Bar
	status_bar.config(text='')
	my_slider.config(value=0)
	# Get the current song tuple number
	next_one = song_box.curselection() 
	# Add one to the current song number
	next_one = next_one[0]-1
	#Grab song title from playlist
	song = song_box.get(next_one)
	# add directory structure and mp3 to song title
	song = f'C:/Users/danny/Music{song}.mp3'
	# Load and play song
	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist listbox
	song_box.selection_clear(0, END)

	# Activate new song bar
	song_box.activate(next_one)

	# Set Active Bar to Next Song
	song_box.selection_set(next_one, last=None)

# Delete A Song
def delete_song():
	stop()
	# Delete Currently Selected Song
	song_box.delete(ANCHOR)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Delete All Songs from Playlist
def delete_all_songs():
	stop()
	# Delete All Songs
	song_box.delete(0, END)
	# Stop Music if it's playing
	pygame.mixer.music.stop()

# Create Global Pause Variable
global paused
paused = False

# Pause and Unpause The Current Song
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		# Pause
		pygame.mixer.music.pause()
		paused = True
	
# Create slider function
def slide(x):
	#slider_label.config(text=f'{int(my_slider.get())} of {int(song_length)}')
	song = song_box.get(ACTIVE)
	song = f'C:/Users/danny/Music{song}.mp3'

	pygame.mixer.music.load(song)
	pygame.mixer.music.play(loops=0, start=int(my_slider.get()))



###################################################################################################

# COLOR FRAME


canvas = Canvas(root, bg="blue", width=910,height=250)
canvas.pack(pady=50)

# FRAME IN THE COLOR FRAME

frame_2 = Frame(canvas)
canvas2 = Canvas(frame_2, bg="gray22", width=900,height=445)
canvas2.pack()
frame_2.config(bg="gray22", width=500)
frame_2.pack(pady=10,padx=10)

song_box = Listbox(frame_2, bg="black", fg="green", width=110, height=18, selectbackground="gray", selectforeground="white")
song_box.place(x=135,y=75)

lf = LabelFrame(frame_2, text="")
lf.config(bg="gray22")
lf.place(x=240,y=390)

# Logo
logo = Label(root, text="iPlayX", font=("Halvetica", 24, 'bold'), fg="white", bg="black")
logo.place(x=25, y=3)

# Title
title = Label(root, text="Welcome To iPlayX", font=("Halvetica", 16, 'bold'), bg="black", fg="white")
title.place(x=408,y=12)

# Version
title = Label(root, text="Version 1.0.0", font=("Halvetica", 10, 'bold'), bg="black", fg="white")
title.place(x=30, y=575)

b1 = Button(lf, text="Go Back", fg="white", bg="gray22", borderwidth=0, command = previous_song).grid(row=0,column=0, padx=20)
b1a = Label(lf,text="").grid(row=0,column=1)
b2 = Button(lf, text="Go Forward", fg="white", bg="gray22", borderwidth=0, command = next_song).grid(row=0,column=3, padx=20)
b2a = Label(lf,text="").grid(row=0,column=4)
b3 = Button(lf, text="Play", fg="white", bg="gray22", borderwidth=0, command = play).grid(row=0,column=5, padx=20)
b3a = Label(lf,text="").grid(row=0,column=6)
b4 = Button(lf, text="Pause", fg="white", bg="gray22", borderwidth=0, command = lambda: pause(paused)).grid(row=0,column=7, padx=20)
b4a = Label(lf,text="").grid(row=0,column=8)
b5 = Button(lf, text="Stop", fg="white", bg="gray22", borderwidth=0, command = stop).grid(row=0,column=9, padx=20)

my_slider = ttk.Scale(frame_2, from_=0, to=100, orient = HORIZONTAL, value = 0, command = slide, length=360)
my_slider.place(x=285,y=25)

# Menu

my_menu = Menu(frame_2)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command = add_song)

add_song_menu.add_command(label="Add Many Songs To Playlist", command = add_many_songs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu= remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command = delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist", command = delete_all_songs)


# Status bar
status_bar = Label(root, text = "", bd=1, relief=GROOVE, anchor = E)
status_bar.pack(fill=X,side = BOTTOM, ipady=2)

####################################THEMES###############################################################

# Themes
options = [
	"Select A Theme",
	"Blue",
	"Red",
	"Green",
	"Purple",
	"Light",

]

def comboclicked():

	if clicked.get() == "Select A Theme":
		pass
	if clicked.get() == "Red":
		pass
	elif clicked.get() == "Purple":
		pass
	elif clicked.get() == "Green":
		pass
	elif clicked.get() == "Blue":
		pass
	elif clicked.get() == "Light":
		pass

def show(e):

	if clicked.get() == "Red":
		canvas.config(bg="red")

	elif clicked.get() == "Purple":
		canvas.config(bg="purple")
	elif clicked.get() == "Green":
		canvas.config(bg="lightgreen")
	elif clicked.get() == "Blue":
		canvas.config(bg="blue")
	elif clicked.get() == "Light":
		canvas.config(bg="white")


clicked = StringVar()
clicked.set(options[4])

# Theme selection
drop1 = ttk.OptionMenu(root,clicked, *options,command=show)
drop = ttk.Combobox(root,value= comboclicked)
drop.current(0)
drop.bind("<<ComboboxSelected>>", show)
drop1.place(x=800,y=15)
drop1.config(width=20)



root.mainloop()
