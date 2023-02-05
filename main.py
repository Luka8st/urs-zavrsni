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
checkResultFalse = 0

root = tk.Tk()
root.title("My Window")
root.geometry("1000x1000")
checkResult = tk.Label(root)

employee_text = tk.StringVar()
employee_label = tk.Label(root, textvariable=employee_text)

list = tk.Label(root, text="Tablica korisnika:")

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

employeeAdded = False


master_id = "609ee086f8f886'"

radnik_id = ["fe98fe667ee6'", "e686f8607ef8fe'", "9e66fe667e98fe'", "7e669e98e0'", "f800607e98'"]

#radnici = [[radnik_id[0], "", ""], [radnik_id[1], "", ""], [radnik_id[2], "", ""], [radnik_id[3], "", ""], [radnik_id[4], "", ""]]
#def change_text():
 #   startLabel.config(text="Novo tekst")

def reset(return_button, submit_button):
    global masterMode, entryCount, create, optionsCount, masterLabel, startLabel, entry, employeeAdded, checkResult
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
    
    startLabel.config(text="Prislonite tag")
    startLabel.pack()


def checkEntry():
    global entry
    if(entry.get()==""):
        root.after(1000,checkEntry())

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
            #entry = tk.Entry(root)
            entry.config(text="")
            entry.delete(0, 20)
            entry.pack()
            #checkEntry(entry)
            #while(entry.get()==""):
                
            submit_button = tk.Button(root, text="Submit", command=lambda: submit(submit_button))
            submit_button.pack()
            
                
    else:
        startLabel.config(text="Prislonite tag")
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
        root.after(500, lambda: deleteEmployee)
    
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


def deleteEmployee():
    global radnici
    print("delete")

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
    else:
        print("pos=-1")
        root.after(100, deleteEmployee)


def addEmployee(submit_button):
    
    checkResultFalse = 0
    global create, addError
    print("a")
    dataEmployee = str(binascii.hexlify(ser.read(17)))
    
    posInList = -1
    for i in range(5):
        if(dataEmployee[6:22] == radnici[i][3]):
            posInList = i
    
    """if(posInList == -1):
        print(f'pos=-1, data={dataEmployee[6:22]}')

    if(posInList != -1 and radnici[posInList][1] != ""):
        print("ovaj radnik vec ima podatke")
        #checkResult.pack_forget()
        #checkResult.config(text="Ovaj radnik već ima podatke u bazi")
        #checkResult.pack()

        test = tk.Label(root, text="test")
        test.pack()

        print("test")

        return_button = tk.Button(root, text="Povratak", command=lambda: reset(return_button, submit_button))
        return_button.pack()
    
    if(posInList != -1 and radnici[posInList][1] == ""):
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
        
    else:
        root.after(100, addEmployee(submit_button))"""

    if(posInList == -1):
        print(f'pos=-1, data={dataEmployee[6:22]}')

        root.after(100, addEmployee(submit_button))
    else:
        if(radnici[posInList][1] != ""):
            print("ovaj radnik vec ima podatke")
            #checkResult.pack_forget()
            #checkResult.config(text="Ovaj radnik već ima podatke u bazi")
            #checkResult.pack()

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
    port='/dev/ttyUSB1',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.close()
ser.open()

#startLabel = tk.Label(root, text="Prislonite tag")
#startLabel.pack()

#masterLabel = tk.Label(root, text = "")
#masterLabel.pack()


#masterLabel.pack(expand=False)
#masterLabel.pack_forget()

#button = tk.Button(root, text="Promijeni tekst", command=change_text)
#button.pack()
data = ""

root.after(1000, change_starttext)



root.mainloop()

conn.close()
