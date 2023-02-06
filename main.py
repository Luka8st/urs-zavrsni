import sqlite3
import serial
import binascii
import time
import math
from datetime import datetime, timedelta
import tkinter as tk

masterMode = False
entryCount = 0
create = False
optionsCount = 0
checkResultFalse = 0

root = tk.Tk()
root.title("My Window")
root.geometry("1000x1000")
checkResult = tk.Label(root)

employee_text = tk.StringVar()
employee_label = tk.Label(root, textvariable=employee_text)

list = tk.Label(root, text="Tablica radnika:")

addError = tk.Label(root, text="Radnik već ima podatke")


startLabel = tk.Label(root, text="Prislonite tag")
startLabel.pack()

masterLabel = tk.Label(root, text = "")
masterLabel.pack()

entry = tk.Entry(root)

nameLabel = tk.Label(root, text="Unesite ime")

nameEntry = tk.Entry(root)

surnameLabel = tk.Label(root, text="Unesite prezime")

surnameEntry = tk.Entry(root)

checkResult = tk.Label(root, text="")

#nameButton = tk.Button(root, text="Unesi podatke", command=lambda: check_name(posInList, nameButton))

secondLabel = tk.Label(root, text="Prislonite RFID tag")

deleteLabel = tk.Label(root, text="Prislonite RFID tag da biste obrisali podatke")

logLabel = tk.Label(root, text="uspjesna prijava/odjava")

employeeAdded = False

logSuccess = False


master_id = "609ee086f8f886'"

radnik_id = ["fe98fe667ee6'", "e686f8607ef8fe'", "9e66fe667e98fe'", "7e669e98e0'", "f800607e98'"]

#radnici = [[radnik_id[0], "", ""], [radnik_id[1], "", ""], [radnik_id[2], "", ""], [radnik_id[3], "", ""], [radnik_id[4], "", ""]]
#def change_text():
 #   startLabel.config(text="Novo tekst")

def resetNoArg():
    logLabel.pack_forget()
    startLabel.pack()
    startLabel.config(text="Prislonite tag")

def reset(return_button, submit_button):
    global masterMode, entryCount, create, optionsCount, masterLabel, startLabel, entry, employeeAdded, checkResult, deleteLabel
    employeeAdded = False
    masterMode = False
    entryCount = 0
    create = False
    optionsCount = 0
    """return_button.destroy()
    list.destroy()
    employee_label.destroy()
    submit_button.destroy()
    entry.destroy()
    masterLabel.destroy()"""

    return_button.pack_forget()
    list.pack_forget()
    employee_label.pack_forget()
    submit_button.pack_forget()
    entry.pack_forget()
    masterLabel.pack_forget()
    secondLabel.pack_forget()
    checkResult.pack_forget()
    deleteLabel.pack_forget()
    
    startLabel.config(text="Prislonite tag")
    startLabel.pack()


def checkEntry():
    global entry
    if(entry.get()==""):
        root.after(1000,checkEntry())

def change_starttext():
    global entryCount, logLabel, startLabel
    #print(data[6:22])
    data = str(binascii.hexlify(ser.read(17)))
    print(data[6:22] == master_id)
    #if(data[6:22]!=""):
    global masterMode
    print("-----------")
    print(masterMode)
    if(data[6:22] == master_id or masterMode==True):
        masterMode = True

        global optionsCount, logSuccess
        optionsCount = optionsCount + 1

        print(f'optioncount={optionsCount}')
        if(optionsCount == 1):
            startLabel.config(text="Master")
            startLabel.pack()
            masterLabel.config(text="Odaberite opciju: 1-dodavanje, 2-brisanje, 3-popis")
            masterLabel.pack()

        entryCount = entryCount + 1
        if(entryCount == 1):
            #entry = tk.Entry(root)
            entry.config(text="")
            entry.delete(0, 20)
            entry.pack()
            #checkEntry(entry)
            #while(entry.get()==""):
                
            submit_button = tk.Button(root, text="Submit", command=lambda: submit(submit_button))
            submit_button.pack()
    else:
        if(data[6:22] in radnik_id):
            print("radnik u bazi")   

            logPos = -1
            for i in range(5):
                if(radnik_id[i] == data[6:22]):
                    logPos = i 
            print(logPos)    

            if(radnici[logPos][1] != ""):
                print("radnik ima podatke")

                cursor.execute("""
                    SELECT * FROM vrijeme WHERE id_radnik = ? AND kraj IS NULL
                """, (radnici[logPos][0],)
                )
                otvoreno = cursor.fetchall()

                print("otvoreno:")
                print(len(otvoreno))

                if(len(otvoreno) == 1):
                    print("postoji otvorena smjena")

                    cursor.execute("""
                        UPDATE vrijeme SET kraj=? 
                        WHERE id_radnik = ? AND kraj IS NULL
                    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),radnici[logPos][0])
                    )
                    conn.commit()
                    print("unesen kraj")

                    cursor.execute("""
                        UPDATE vrijeme SET 
                        trajanje = strftime('%s', kraj) - strftime('%s', pocetak)
                        WHERE id_radnik = ? AND trajanje IS NULL
                    """,(radnici[logPos][0],))
                    conn.commit()

                    cursor.execute("""
                        SELECT trajanje FROM vrijeme WHERE trajanje !="" ORDER BY id DESC LIMIT 1
                    """)
                    conn.commit()
                    fetch = cursor.fetchone()[0]

                    print("fetch type")
                    print(type(fetch))
                    trajanje = int(fetch)
                    print("izracunato trajanje")
                    print(trajanje)

                    trajanjeH = math.floor(trajanje/3600)
                    trajanjeM = math.floor((trajanje - 3600*trajanjeH)/60)
                    trajanjeS = trajanje - 60*trajanjeM - 3600*trajanjeH

                    startLabel.config(text=f'Uspješna odjava - {radnici[logPos][1]} {radnici[logPos][2]}\nKraj: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nTrajanje: {trajanjeH} h {trajanjeM} m {trajanjeS} s')
                    startLabel.pack()
                    logSuccess = True
                    #root.after(5000, resetNoArg())
                else:
                    cursor.execute("""
                        INSERT INTO vrijeme (id_radnik,pocetak) VALUES (?,?)
                        """, (radnici[logPos][0],datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)
                    )
                    conn.commit()

                    print("uneseni podaci")

                    logSuccess = True

                    #startLabel.pack_forget()
                    startLabel.config(text=f'Uspješna prijava - {radnici[logPos][1]} {radnici[logPos][2]}\nPočetak: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
                    #startLabel.pack()

            else:
                print("radnik nema podatke")
                
        #else:
            #startLabel.config(text="Prislonite tag")
    if(logSuccess):
        root.after(5000, resetNoArg)
        logSuccess = False
        
    root.after(1000, change_starttext)

def submit(submit_button):
    global masterLabel, startLabel, entry
    #global entry
    text = entry.get()
    # Obrađivanje teksta unesenog u Entry widget
    print("Unesen tekst:", text)

    if(text == "1"):
        """entry.destroy()
        submit_button.destroy()
        masterLabel.destroy()"""
        return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))

        submit_button.pack_forget()
        entry.pack_forget()
        masterLabel.pack_forget()
        #startLabel = tk.Label(root, text="Prislonite RFID tag")
        secondLabel.pack()
        root.after(1000, lambda: addEmployee(submit_button))

        """print("employee added:")
        print(employeeAdded)
        if(employeeAdded):
            return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
            return_button.pack()"""


        #return_button.pack()


        #ovo bi mozda trebalo maknut
        #list = tk.Label(root, text="")
        #employee_label = tk.Label(root, text="")

        
        #return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, list, submit_button, entry, masterLabel, startLabel))

    if (text == "2"):
        root.after(500, lambda: deleteEmployee(submit_button))
    
    if (text == "3"):
        global employee_label, list
        submit_button.pack_forget()
        entry.pack_forget()
        masterLabel.pack_forget()

        #list = tk.Label(root, text="Tablica korisnika:")
        list.pack()
        
        employee = ""
        for radnik in radnici:
            employee = employee + "ID: {0} Ime: {1} Prezime: {2} RFID: {3} Vrijeme: {4}\n".format(radnik[0], radnik[1], radnik[2], radnik[3], radnik[4])
        #employee_label = tk.Label(root, text=employee)
        #employee_label.config(text=employee)
        #employee_text.set("Unesite tekst ovdje")
        employee_text.set(employee)
        employee_label.pack()

        return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
        return_button.pack()


def deleteEmployee(submit_button):
    global radnici, entry, deleteLabel
    print("delete")

    entry.pack_forget()
    submit_button.pack_forget()
    masterLabel.pack_forget()
    deleteLabel.pack()
    

    dataEmployee = str(binascii.hexlify(ser.read(17)))

    posInList = -1
    for i in range(5):
        if(dataEmployee[6:22] == radnici[i][3]):
            posInList = i
    
    if(posInList != -1):
        print("pos!=-1")
        cursor.execute("""
            UPDATE radnici 
            SET name = ?, surname = ?, time_stamp = ? 
            WHERE rfid_id = ?
            """, ("", "", "", radnici[posInList][3])
        )
        conn.commit()

        cursor.execute("""
            SELECT * FROM radnici
        """)
        radnici = cursor.fetchall()
        print("radnici:")
        print(radnici)
        conn.commit()

        return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
        return_button.pack()
    else:
        print("pos=-1")
        root.after(100, lambda: deleteEmployee(submit_button))


def addEmployee(submit_button):
    
    checkResultFalse = 0
    global create, addError
    print("a")
    dataEmployee = str(binascii.hexlify(ser.read(17)))
    
    posInList = -1
    for i in range(5):
        if(dataEmployee[6:22] == radnici[i][3]):
            posInList = i

    if(posInList == -1):
        print(f'pos=-1, data={dataEmployee[6:22]}')

        root.after(100, addEmployee(submit_button))
    else:
        if(radnici[posInList][1] != ""):
            print("ovaj radnik vec ima podatke")

            addError.pack()

            test = tk.Label(root, text="test")
            test.pack()

            print("test")

            return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
            return_button.pack()

            root.after(100, addEmployee(submit_button))

        else:
            print("radnik je u bazi i nema ime")

            #nameLabel = tk.Label(root, text="Unesite ime")
            nameLabel.pack()

            #nameEntry = tk.Entry(root)
            nameEntry.delete(0, 20)
            nameEntry.pack()

            #surnameLabel = tk.Label(root, text="Unesite prezime")
            surnameEntry.delete(0, 20)
            surnameLabel.pack()

            #surnameEntry = tk.Entry(root)
            surnameEntry.pack()

            nameButton = tk.Button(root, text="Unesi podatke", command=lambda: check_name(posInList, nameButton, submit_button))
            nameButton.pack()
            #return_button.pack()

    

def check_name(posInList, nameButton, submit_button):
    global radnici, checkResultFalse, startLabel, nameEntry, surnameEntry, nameLabel, surnameLabel, employeeAdded
    
    
    if(nameEntry.get() != "" and surnameEntry.get() != ""):
        print("dobri podaci")
        cursor.execute("""
            UPDATE radnici 
            SET name = ?, surname = ?, time_stamp = ? 
            WHERE rfid_id = ?
            """, (nameEntry.get(), surnameEntry.get(), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), radnici[posInList][3])
        )
        conn.commit()

        cursor.execute("""
            SELECT * FROM radnici
        """)
        radnici = cursor.fetchall()
        print("radnici:")
        print(radnici)
        conn.commit()

        employeeAdded = True
        secondLabel.pack_forget()
        nameLabel.pack_forget()
        nameEntry.pack_forget()
        surnameLabel.pack_forget()
        surnameEntry.pack_forget()
        nameButton.pack_forget()
        checkResult.pack_forget()
        checkResult.config(text="Podaci su uspjesno uneseni")
        checkResult.pack()

        return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
        return_button.pack()
    else:
        if(checkResultFalse == 0):
            checkResult.config(text="Podaci nisu ispravni, pokušajte ponovno")
            checkResult.pack()
            checkResultFalse = 1


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
    print("izvršen insert")
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

data = ""

root.after(1000, change_starttext)

root.mainloop()

conn.close()
