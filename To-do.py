#tuodaan ohjelmassa tarvittavat kirjastot.
import sqlite3
from tkinter import*
from tkinter.font import Font 

#luodaan funktio, joka tallentaa syötekentiin kirjatut tiedot tietokantaan
def saveNotes():
    #tallennetaan muuttujiin käyttäjän syötekenttiin syöttämät tiedot.
    numb = int(Entry.get(idField))
    thing = (Entry.get(thingField))
    dlline = (Entry.get(deadlineField))
    #avataan yhteys data.db nimiseen tietokantaan.
    connection = sqlite3.connect('data.db')
    #lisätään tietokannan tauluun TODO muuttujiin tallennetut käyttäjän syöttämät tiedot.
    #TODO taulussa on id-kenttä, jolla yksilöidään jokainen merkintä, note on merkinnälle varattu kenttä.
    #dlday on päivämääräkenttä.
    cursor = connection.execute("INSERT INTO TODO (ID,NOTE,DLDAY) VALUES (?,?,?)",(numb,thing,dlline))
    connection.commit()

#luodaan funktio, joka hakee tallennetut tiedot kannasta id-numerolla.
def loadNotes():
    connection = sqlite3.connect('data.db')
    #suoritaan sql-haku id-kenttään kirjatun numeron perusteella. valitaan tietokanansta id-nro, note-kentän merkintä
    #ja päivämäärätieto.
    cursor = connection.execute("SELECT ID,NOTE,DLDAY FROM TODO")
    #käydään tulokset läpi for silmukassa ja tulostetaan ne tekstilaatikkoon.
    for row in cursor:
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,'Note number: ',END)
        textbox.insert(INSERT,row[0],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,'To-DO: ',END)
        textbox.insert(INSERT,row[1],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,'Deadline: ',END)
        textbox.insert(INSERT,row[2],END)
        textbox.insert(INSERT,'\n',END)

#luodaan funktio, jonka avulla tietoja voidaan poistaa.
def deleteNotes():
    numb = int(Entry.get(idField))
    connection = sqlite3.connect('data.db')
    #poistetaan TODO taulusta haluttu tieto käyttäjän syöttämän id-numeron perusteella.
    cursor = connection.execute("DELETE FROM TODO WHERE ID= %s" %numb)
    connection.commit()

#luodaan funktio, jolla voidaan muokata tallennettuja tietoja. tieto haetaan id-numerolla.
def updateNotes():
    numb = int(Entry.get(idField))
    thing = (Entry.get(thingField))
    dlline = (Entry.get(deadlineField))
    connection = sqlite3.connect('data.db')
    #sql-lause, joka päivittää note-kentän tiedon
    cursor = connection.execute("UPDATE TODO SET NOTE=? WHERE ID=?",(thing,numb))
    #sql-lause, joka päivittää note-dlday kentän päivämäärän.
    cursor = connection.execute("UPDATE TODO SET DLDAY=? WHERE ID=?",(dlline,numb))
    connection.commit() 

#funktio, joka järjestää tietokannan merkinnät päivämäärän mukaan laskevaan järjestykseen.    
def dateDesc():
    connection = sqlite3.connect('data.db')
    cursor =  connection.execute("SELECT * FROM TODO ORDER BY DLDAY DESC")
    for row in cursor:
        textbox.insert(INSERT,row[0],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,row[1],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,row[2],END)

#funkio, joka järjestää tietokannan merkinnät päivämäärän mukaan nousevaan järjestykseen.
def dateAsc():
    connection = sqlite3.connect('data.db')
    cursor = connection.execute("SELECT * FROM TODO ORDER BY DLDAY ASC")
    for row in cursor:
        textbox.insert(INSERT,row[0],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,row[1],END)
        textbox.insert(INSERT,'\n',END)
        textbox.insert(INSERT,row[2],END)

#funktio, joka laskee tietokannassa olevien merkintöjen määrän.
def countNotes():
    connection = sqlite3.connect('data.db')
    #lasketaan todo-taulussa olevat id:t yhteen.
    cursor = connection.execute("SELECT COUNT (ID) FROM TODO")
    for row in cursor:
        textbox.insert(INSERT,' You have ',END)
        textbox.insert(INSERT,row[0],END)
        textbox.insert(INSERT,' notes ',END)

#funktio, joka tyhjentää tekstilaatikossa olevan sisällön.
def clear():
    textbox.delete(1.0,END)

    
    
    
#luodaan pohjakomponentti ja annetaan sille taustaväri.
root = Tk()
root.config(background = 'SteelBlue3')
root.title('TO-DO')

#luodaan framekomponentit ja annetaan taustavärit. framekomponenteillä asemoidaan muut komponentit.
frame1 = Frame()
frame1.config(background = 'SteelBlue3')
frame2 = Frame()
frame2.config(background = 'SteelBlue3')
frame3 = Frame()
frame3.config(background = 'SteelBlue3')
frame4 = Frame()
frame4.config(background = 'SteelBlue3')
frame5 = Frame()
frame5.config(background = 'SteelBlue3')
frame6 = Frame()
frame6.config(background = 'SteelBlue3')

#luodaan rullauspalkki, sijoitetaan se oikealle ja asetetaan rullaussuunta Y-akselille.
#rullauspalkki sijoitetaan frame6 komponenttiin.
scrollbar = Scrollbar(frame6)
scrollbar.pack(side = RIGHT, fill = Y)

#luodaan alasvetovalikko.
menubar = Menu(root)
funcmenu = Menu(menubar)
#annetaan alasvetovalikolle otsikkoteksti.
menubar.add_cascade(label = 'More Functions', menu = funcmenu)
#lisätään rullauspalkkiin toiminnot, command komennolla kerrotaan funktio, joka suoritetaan
#jos toimintoa painetaan hiirellä.
funcmenu.add_command(label = 'Order by date desc', command = dateDesc)
funcmenu.add_command(label = 'Order by date asc', command = dateAsc)
funcmenu.add_command(label = 'Count notes', command = countNotes)
funcmenu.add_command(label = 'Clear textbox', command = clear) 
root.config(menu=menubar)

#tallenetaan muuttujiin segoe print fontti.
titlefont = Font (family = 'Segoe Print')
labelfont = Font (family = 'Segoe Print', size = 9)

#tuodaan ohjelmaan kuvakkeet, joita käytetään painikkeissa.
updateicon = PhotoImage(file = 'updated.png')
updatefinal = updateicon.subsample(4,4 )

deleteicon = PhotoImage(file = 'delete.png')
deletefinal = deleteicon.subsample(4,4)

loadicon = PhotoImage(file = 'loadfile.png')
loadfinal = loadicon.subsample(4,4)

saveicon = PhotoImage(file = 'savefile.png')
savefinal = saveicon.subsample(4,4)


#luodaan syötekentät.
idField = Entry(frame1,width=8)
thingField = Entry(frame2)
deadlineField = Entry(frame3,width=10)

#luodaan tekstiä sisältävät komponentit, font komennolla kerrotaan tekstissä
#käytettävä fontti ja bg komennolla komponentissa käytettävä taustaväri.
name = Label(root, text = 'TO-DO-APP',font = titlefont, bg = 'SteelBlue3')
idLabel = Label(frame1, text = 'Note number:', font = labelfont, bg = 'SteelBlue3')
thingLabel = Label(frame2, text = 'TO-DO', font = labelfont, bg = 'SteelBlue3')
deadlineLabel = Label(frame3, text = 'Deadline', font = labelfont, bg = 'SteelBlue3')

#luodaan tekstilaatikko, annetaan sille korkeus ja leveys, sekä liitetään siihen
#aiemmin luotu rullauspalkki.
textbox = Text(frame6, width = 25, height = 8, yscrollcommand = scrollbar.set)

#luodaan painikekomponentit, command komennolla kerrotaan suoritettava funktio jos nappia
#painetaan, image komennolla kerrotaan kuvake joka liitetään painikkeeseen, compound komennolla
#kerrotaan kuvakkeen sijoitussuunta.

savebtn = Button(frame4, text = 'Save', command = saveNotes, image = savefinal, compound = RIGHT)
loadbtn = Button(frame4, text = 'Load', command = loadNotes, image = loadfinal, compound = RIGHT)
delbtn = Button(frame5, text = 'Delete', command = deleteNotes, image = deletefinal, compound = RIGHT)
updatebtn = Button(frame5, text = 'Edit', command = updateNotes, image = updatefinal, compound = RIGHT)

#pakataan komponentit, side komennolla sijoitetaan komponentti, pady ja padx komennoilla lisätään
#tyhjää tilaa komponenttien ympärille.
name.pack()
frame1.pack()
idLabel.pack(side=LEFT,pady = 4,padx = 4)
idField.pack(side=RIGHT,pady = 4, padx = 4)
frame2.pack()
thingLabel.pack(side=LEFT,pady = 4,padx = 4)
thingField.pack(side=RIGHT,pady=4, padx = 4)
frame3.pack()
deadlineLabel.pack(side=LEFT, pady = 4, padx = 4)
deadlineField.pack(side=RIGHT, pady = 4, padx = 4)
frame6.pack()
textbox.pack(pady=4,padx=4, side= LEFT, fill = BOTH)
scrollbar.config(command = textbox.yview)
frame4.pack()
savebtn.pack(side=LEFT,padx=4,pady=4)
loadbtn.pack(side=RIGHT)
frame5.pack()
delbtn.pack(side=LEFT,padx=4, pady = 4)
updatebtn.pack(side=RIGHT)
