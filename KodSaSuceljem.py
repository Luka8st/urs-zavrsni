import sqlite3
import serial
import binascii
import time
from datetime import datetime, timedelta
import tkinter as tk

masterMode = False
entryCount = 0
create = False
optionsCount = 0

master_id = "609ee086f8f886'"

radnik_id = ["fe98fe667ee6'", "e686f8607ef8fe'", "9e66fe667e98fe'", "7e669e98e0'", "f800607e98'"]

#radnici = [[radnik_id[0], "", ""], [radnik_id[1], "", ""], [radnik_id[2], "", ""], [radnik_id[3], "", ""], [radnik_id[4], "", ""]]
#def change_text():
 #   startLabel.config(text="Novo tekst")

def reset(return_button, employee_label, list, submit_button, entry, masterLabel, startLabel):
    global masterMode, entryCount, create, optionsCount
    masterMode = False
    entryCount = 0
    create = False
    optionsCount = 0
    return_button.destroy()
    list.destroy()
    employee_label.destroy()
    submit_button.destroy()
    entry.destroy()
    masterLabel.destroy()
    #startLabel.destroy()
    startLabel.config(text="Prislonite tag")
    startLabel.pack()


def checkEntry(entry):
    if(entry.get()==""):
        root.after(1000,checkEntry(entry))

def change_starttext():
    global entryCount
    #print(data[6:22])
    data = str(binascii.hexlify(ser.read(17)))
    print(data[6:22] == master_id)
    #if(data[6:22]!=""):
    global masterMode
    print("-----------")
    print(masterMode)
    if(data[6:22] == master_id or masterMode==True):
        masterMode = True

        global optionsCount
        optionsCount = optionsCount + 1

        print(f'optioncount={optionsCount}')
        if(optionsCount == 1):
            startLabel.config(text="Master")
            startLabel.pack()
            masterLabel.config(text="Odaberite opciju: 1-dodavanje, 2-brisanje, 3-popis")
            masterLabel.pack()

        entryCount = entryCount + 1
        if(entryCount == 1):
            entry = tk.Entry(root)
            entry.pack()
            #checkEntry(entry)
            #while(entry.get()==""):
                
            submit_button = tk.Button(root, text="Submit", command=lambda: submit(entry, submit_button, masterLabel, startLabel))
            submit_button.pack()
            
                
    else:
        startLabel.config(text="Prislonite tag")
    root.after(1000, change_starttext)

def submit(entry, submit_button, masterLabel, startLabel):
    #global entry
    text = entry.get()
    # Obra??ivanje teksta unesenog u Entry widget
    print("Unesen tekst:", text)

    if(text == "1"):
        entry.destroy()
        submit_button.destroy()
        masterLabel.destroy()
        startLabel = tk.Label(root, text="Prislonite RFID tag")
        startLabel.pack()
        root.after(1000, addEmployee)
    
    if (text == "3"):
        list = tk.Label(root, text="Tablica korisnika:")
        list.pack()
        
        employee = ""
        for radnik in radnici:
            employee = employee + "ID: {0} Ime: {1} Prezime: {2} RFID: {3} Vrijeme: {4}\n".format(radnik[0], radnik[1], radnik[2], radnik[3], radnik[4])
        employee_label = tk.Label(root, text=employee)
        employee_label.pack()

    return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, employee_label, list, submit_button, entry, masterLabel, startLabel))
    return_button.pack()


def addEmployee():
    global create
    print("a")

    root.after(1000, addEmployee)


def change():
    root.after(1000, change_starttext)

conn = sqlite3.connect("rfid.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS radnici (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    rfid_id TEXT,
    time_stamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS vrijeme (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_radnik INTEGER,
    pocetak TEXT,
    kraj TEXT,
    trajanje TEXT,
    FOREIGN KEY (id_radnik) REFERENCES radnici(id)
)
""")


conn.commit()

cursor.execute("SELECT COUNT(*) FROM radnici")
count = cursor.fetchone()[0]

if count == 0:
    sql = "INSERT INTO radnici (name, surname, rfid_id, time_stamp) VALUES (?,?,?,?)"
    values = [
        ["", "", radnik_id[0], ""],
        ["", "", radnik_id[1], ""],
        ["", "", radnik_id[2], ""],
        ["", "", radnik_id[3], ""],
        ["", "", radnik_id[4], ""]
    ]
    cursor.executemany(sql, values)
    print("izvr??en insert")
    conn.commit()

cursor.execute("SELECT * FROM radnici")
radnici = cursor.fetchall()
conn.commit()
print(radnici)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.close()
ser.open()

root = tk.Tk()
root.title("My Window")
root.geometry("1000x1000")

startLabel = tk.Label(root, text="Prislonite tag")
startLabel.pack()

masterLabel = tk.Label(root, text = "")
masterLabel.pack()


#masterLabel.pack(expand=False)
#masterLabel.pack_forget()

#button = tk.Button(root, text="Promijeni tekst", command=change_text)
#button.pack()
data = ""

root.after(1000, change_starttext)



root.mainloop()

while True:
    data = str(binascii.hexlify(ser.read(17)))

    if data[6:22] == master_id:
        #root.after(1000, change_starttext)
        #masterLabel.pack(side="bottom", fill="both",expand=True)

        #label = tk.Label(root, text="Label created after mainloop")
        #label.pack()
        #root.update()
        vrijednost = input("Odaberite opciju: 1-unos, 2-brisanje, 3-popis ")
        if(vrijednost == "1"):
            print("Prislonite RFID tag")
            while 1:
                data_radnik = str(binascii.hexlify(ser.read(17)))
                if data_radnik[6:22] != "":
                    print("1 - " + data_radnik[6:22])
                    if data_radnik[6:22] in radnik_id:
                    #if data_radnik[6:22] in radnici["rfid_id"]:
                        print("Uspjesno procitan tag")

                        pos = -1
                        for i in range(5):
                            print(radnici[i][3])
                            if(data_radnik[6:22] == radnici[i][3]):
                                pos = i
                                break
                        
                        print(f'pos = {pos}')
                        if (pos == -1):
                            print("Ovaj id ne postoji u bazi")
                        else:
                            if(radnici[pos][1] != "" or radnici[pos][2] != ""):
                                print("Za taj id ve?? je postavljeno ime radnika - da biste ga promijenili, prvo morate izbrisati postoje??e ime")
                            else:
                                ime = input("Unesite ime: ").strip()
                                prezime = input("Unesite prezime: ").strip()
                                while (ime == "" or prezime == ""):
                                    print("Podaci nisu ispravno uneseni")
                                    ime = input("Unesite ime: ").strip()
                                    prezime = input("Unesite prezime: ").strip()
                                print(ime + " " + prezime + " - radnik je ispravno unesen")
                                
                                cursor.execute("""
                                    UPDATE radnici 
                                    SET name = ?, surname = ?, time_stamp = ? 
                                    WHERE rfid_id = ?
                                """, (ime, prezime, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), radnici[pos][3])
                                )

                                cursor.execute("""
                                    SELECT * FROM radnici
                                """)
                                radnici = cursor.fetchall()
                                conn.commit()
                            
                        break
                    else:
                        print("Ovaj id ne postoji u bazi")
        else:
            if(vrijednost == "2"):
                print("Prislonite RFID tag")
                while 1:
                    data_radnik = str(binascii.hexlify(ser.read(17)))
                    if(data_radnik[6:22] != ""):
                        print("2 - " + data_radnik[6:22])
                        if data_radnik[6:22] in radnik_id:
                            print("Uspjesno procitan tag")
                            for i in range(5):
                                if(data_radnik[6:22] == radnici[i][3]):
                                    
                                    rfid = data_radnik[6:22]
                                    cursor.execute("""
                                        UPDATE radnici 
                                        SET name = "", surname = "", time_stamp = "" 
                                        WHERE rfid_id = ?
                                    """, (rfid,)
                                    )
                                    print("Uspjesno izbrisani podaci")

                                    cursor.execute("""
                                        SELECT * FROM radnici
                                    """)
                                    radnici = cursor.fetchall()
                                    
                                    conn.commit()
                                    break
                            break
            else:
                
                if(vrijednost == "3"):
                    for i in range(5):
                        print(radnici[i])
                    

            vrijednost = ""


    else:
        if(data[6:22] in radnik_id):
            print("pokusaj prijave/odjave")

            pos_radnik = -1
            for i in range(5):
                if(data[6:22] == radnici[i][3]):
                    pos_radnik = i
                    break
            print(f'pos_radnik={pos_radnik}')

            cursor.execute("""
                SELECT COUNT(*) FROM vrijeme JOIN radnici ON(vrijeme.id_radnik = radnici.id)
                WHERE radnici.rfid_id = ?
            """,(data[6:22],))
            countPrijave = cursor.fetchone()[0]
            
            print(data[6:22])
            if(countPrijave > 0):
                print("postoji taj radnik i ima zapis u vrijeme")


                cursor.execute("""
                    SELECT * FROM vrijeme WHERE id_radnik = ? AND kraj IS NULL
                """, (radnici[pos_radnik][0],)
                )
                otvoreno = cursor.fetchall()

                if(len(otvoreno) == 1): #ako radnik ima otvorenu smjenu, tj smjenu bez kraja
                    cursor.execute("""
                        UPDATE vrijeme SET kraj=? 
                        WHERE id_radnik = ? AND kraj IS NULL
                    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),radnici[pos_radnik][0])
                    )
                    conn.commit()
                    print("unesen kraj")

                    cursor.execute("""
                        UPDATE vrijeme SET 
                        trajanje = strftime('%s', kraj) - strftime('%s', pocetak)
                        WHERE id_radnik = ? AND trajanje IS NULL
                    """,(radnici[pos_radnik][0],))
                    conn.commit()
                    print("izracunato trajanje")
                else:
                    print("ovaj radnik nema nijednu smjenu bez kraja")
                    cursor.execute("""
                    INSERT INTO vrijeme (id_radnik,pocetak) VALUES (?,?)
                        """, (radnici[pos_radnik][0],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                    )
                    conn.commit()

                    print("uneseni podaci")



            else:
                print("zapis sa tim id ne postoji")
                rfid = data[6:22]
                cursor.execute("""
                    SELECT COUNT(*) FROM radnici WHERE rfid_id=? AND name != ""
                    """, (rfid,)
                )
                countRadnici = len(cursor.fetchall())

                print(countRadnici)
                if(countRadnici > 0):
                    print("postoji taj radnik, ali nema zapis u vrijeme")

                    pos = -1
                    for i in range(5):
                        if(radnici[i][3] == rfid):
                            pos = i
                            break
                    
                    if(pos == -1):
                        print("taj rfid nije u bazi")
                    else:
                        print("radnik pronaden u bazi")
                    
                        cursor.execute("""
                        INSERT INTO vrijeme (id_radnik,pocetak) VALUES (?,?)
                            """, (radnici[pos][0],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                        )
                        conn.commit()

                        print("uneseni podaci")

    time.sleep(1)

conn.close()
