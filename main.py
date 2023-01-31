import sqlite3
import serial
import binascii
import time
from datetime import datetime, timedelta

master_id = "609ee086f8f886'"

radnik_id = ["fe98fe667ee6'", "e686f8607ef8fe'", "9e66fe667e98fe'", "7e669e98e0'", "f800607e98'"]

#radnici = [[radnik_id[0], "", ""], [radnik_id[1], "", ""], [radnik_id[2], "", ""], [radnik_id[3], "", ""], [radnik_id[4], "", ""]]



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
                                print("Za taj id već je postavljeno ime radnika - da biste ga promijenili, prvo morate izbrisati postojeće ime")
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
