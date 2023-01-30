import sqlite3
import serial
import binascii
import time
from datetime import datetime, timedelta

master_id = "609ee086f8f886'"

radnik_id = ["fe98fe667ee6'", "e686f8607ef8fe'", "9e66fe667e98fe'", "7e669e98e0'", "18607e98'"]

radnici = [[radnik_id[0], "", ""], [radnik_id[1], "", ""], [radnik_id[2], "", ""], [radnik_id[3], "", ""], [radnik_id[4], "", ""]]

conn = sqlite3.connect("rfid.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS rfid_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    surname TEXT,
    rfid_id TEXT,
    time_stamp TEXT
)
""")

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

while True:
    data = str(binascii.hexlify(ser.read(17)))

    if data[6:22] == master_id:
        vrijednost = input("Odaberite opciju: 1-unos, 2-brisanje, 3-popis ")
        if(vrijednost == "1"):
            print("Prislonite RFID tag")
            while 1:
                data_radnik = str(binascii.hexlify(ser.read(17)))
                if data_radnik[6:22] != "":
                    print("1 - " + data_radnik[6:22])
                    if data_radnik[6:22] in radnik_id:
                        print("Uspjesno procitan tag")

                        pos = -1
                        for i in range(5):
                            if(data_radnik[6:22] == radnici[i][0]):
                                pos = i
                                break
                        
                        print(f'pos = {pos}')
                        if (pos == -1):
                            print("Ovaj id ne postoji u bazi")
                        else:
                            ime = input("Unesite ime: ")
                            prezime = input("Unesite prezime: ")
                            print(ime + " " + prezime)
                            radnici[i][1] = ime
                            radnici[i][2] = prezime
                            
                        break
                    else:
                        print("Ovaj id ne postoji u bazi")
        else:
            if(vrijednost == "2"):
                print("Prislonite RFID tag")
                while 1:
                    data_radnik = str(binascii.hexlify(ser.read(17)))
                    print("2 - " + data_radnik[6:22])
                    if data_radnik[6:22] in radnik_id:
                        print("Uspjesno procitan tag")
                        for i in range(5):
                            if(data_radnik[6:22] == radnici[i][0]):
                                radnici[i][1] = ""
                                radnici[i][2] = ""
                                break
                        break
            else:
                if(vrijednost == "3"):
                    for i in range(5):
                        print(radnici[i])
                    

            vrijednost = ""
    """if data[6:22] != '':
        rfid_id = data[6:22]
        cursor.execute("SELECT name, surname FROM rfid_tags WHERE rfid_id=?", (rfid_id,))
        result = cursor.fetchone()
        if result:
            name, surname = result
            print("Name: ", name)
            print("Surname: ", surname)
            print("RFID ID: ", rfid_id)
            print("Time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            cursor.execute("INSERT INTO rfid_tags (name, surname, rfid_id, time_stamp) VALUES (?,?,?,?)
            ", (name, surname, rfid_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        else:
            name = input("Enter name: ")
            surname = input("Enter surname: ")
            cursor.execute("INSERT INTO rfid_tags (name, surname, rfid_id, time_stamp) VALUES (?,?,?,?)
            ", (name, surname, rfid_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            print("Name: ", name)
            print("Surname: ", surname)
            print("RFID ID: ", rfid_id)
            print("Time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))"""
    time.sleep(1)

conn.close()
