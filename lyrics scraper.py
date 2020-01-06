#website lyrics scraper by Robert Nimmo

import urllib.request
from bs4 import BeautifulSoup
from tkinter import *
from tkinter.filedialog import askdirectory
import re

top = Tk()
artistnameTk = StringVar('')
songnameTk = StringVar('')
top.title("Lyrics Scraper")
top.geometry("500x630")

def lyrics():
        url = 'https://lyrics.fandom.com/wiki/'

        artistnameOrig = artistnameTk.get().lower()
        songnameOrig = songnameTk.get().lower()

        artistname = artistnameOrig.replace(' ', '_')
        songname = songnameOrig.replace("&","%26").replace(' ', '_')

        url = '{}{}:{}'.format(url, artistname, songname)
        try:
                page = urllib.request.urlopen(url)

                soup = BeautifulSoup(page, 'html.parser')
                title= soup.find(
                        'h1', attrs={'class':"page-header__title"})
                title =[i for i in title.get_text().replace('Lyrics','').split(':')]
                div = soup.find(
                        'div', attrs={'class': 'lyricbox'})

                for br in div.find_all("br"):
                        br.replace_with("\n")

                lyrics = div.get_text()

                texts = "{}\n{}\n\n{}".format(title[0], title[1], lyrics)

                if radio.get()==1:
                        fileName = askdirectory()
                        with open(fileName+'/lyrics.txt', 'w') as f:
                                f.write(texts)

                texts=texts.split('\n')
                messageLabel.delete(0, END)
                for i in texts:
                        messageLabel.insert(END, str(i))


        except:
                messageLabel.delete(0, END)
                messageLabel.insert(END, "Sorry the song can't be found")

radio=IntVar()

scrollbar=Scrollbar(top)
scrollbar.pack(side=RIGHT, fill=Y)

artistLabel=Label(top, text="Artist:", width=8)
artistLabel.pack()

artistEntry=Entry(top, textvariable=artistnameTk, width=20)
artistEntry.pack()

songLabel=Label(top, text="Song:", width=8)
songLabel.pack()

songEntry=Entry(top, textvariable=songnameTk, width=20)
songEntry.pack()

breaklabel1=Label(top)
breaklabel1.pack()

fileLabel=Label(top,text="Would you like lyrics to be \n loaded into a text file?",width=25)
fileLabel.pack()
fileYbutton=Radiobutton(top,text="Yes",variable=radio,value=1)
fileYbutton.pack()
fileNbutton=Radiobutton(top,text="No",variable=radio,value=2)
fileNbutton.pack()
fileNbutton.select()

breaklabel2=Label(top)
breaklabel2.pack()

lyricsButton = Button(top,text="Get lyrics",command=lyrics)
lyricsButton.pack()


breaklabel3=Label(top)
breaklabel3.pack()

messageLabel=Listbox(top, width=70,height=20,justify=CENTER)

messageLabel.pack()
messageLabel.insert(END, 'Lyrics Scraper by Robert Nimmo')

breaklabel4=Label(top)
breaklabel4.pack()

quitButton=Button(top, text="Quit", command=top.destroy)
quitButton.pack()


messageLabel.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=messageLabel.yview)

mainloop()