
import sqlite3

import pandas as pd


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, "rb") as file:
        blobData = file.read()
    return blobData


def insertBLOB(name, date, time, sleeplevel, city, temperature, wheater, photo):
    try:
        sqliteConnection = sqlite3.connect("CadastroHUB.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite_insert_blob_query = """ INSERT INTO employee
                                  (name, date, time, sleep_level, city, temperature, wheater, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

        empPhoto = convertToBinaryData(photo)
        # Convert data into tuple format
        data_tuple = (
            name,
            date,
            time,
            sleeplevel,
            city,
            temperature,
            wheater,
            empPhoto,
        )
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqliteConnection.commit()
        print("Image inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("the sqlite connection is closed")


##########################################################################################
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, "wb") as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def readBlobData(empId):
    try:
        sqliteConnection = sqlite3.connect("CadastroHUB.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from employee where id = ?"""
        cursor.execute(sql_fetch_blob_query, (empId,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            date = row[2]
            time = row[3]
            sleeplevel = row[4]
            city = row[5]
            temperature = row[6]
            wheater = row[7]
            photo = row[8]

            print("Storing employee image and resume on disk \n")
            photoPath = "FotoConsultada/" + name + date + " " + str(sleeplevel) + ".jpg"
            writeTofile(photo, photoPath)

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")



def ReadInfo():
    try:
        # variables
        dataID = []
        name = []
        date = []
        time = []
        sleeplevel = []
        city = []
        temperature = []
        wheater = []

        sqliteConnection = sqlite3.connect("CadastroHUB.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT * from employee"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            dataID.append(row[0])
            name.append(row[1])
            date.append(row[2])
            time.append(row[3])
            sleeplevel.append(row[4])
            city.append(row[5])
            temperature.append(row[6])
            wheater.append(row[7])

        cursor.close()

        df_cadastro = pd.DataFrame(
            {
                "Id": dataID,
                "Name": name,
                "Date": date,
                "Time": time,
                "Sleep Level": sleeplevel,
                "City": city,
                "Temperature": temperature,
                "Wheater": wheater,
            },
            columns=[
                "Id",
                "Name",
                "Date",
                "Time",
                "Sleep Level",
                "City",
                "Temperature",
                "Wheater",
            ],
        )
        return df_cadastro

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")



def ReadName():
    try:
        # variables
        name = []

        sqliteConnection = sqlite3.connect("CadastroHUB.db")
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sql_fetch_blob_query = """SELECT DISTINCT name from employee"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            name.append(row)

        cursor.close()

        return name

    except sqlite3.Error as error:
        print("Failed to read blob data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")
