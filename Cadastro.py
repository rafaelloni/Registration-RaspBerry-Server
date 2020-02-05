#################################
## Registration Project V.1.0  ##
## Author: Rafael Loni Martins ##
##         Vitor Hugo Bezerra  ##
## 05/02/2020                  ##
#################################


import json
import os

# XMLRPC for communication with raspberry server
import xmlrpc.client
from datetime import date, datetime

import cv2

# Face recognition
import face_recognition

# BASICS IMPORTS
import numpy as np
import pandas as pd

# API to get temperature and wheater
import requests

# Streamlit to create app interface
import streamlit as st
from PIL import Image

# DataBaseHUB.py for SQL database
import DataBaseHUB

############################ PROXY #################################
# Proxy to communicate with raspberry server
raspberryIP = "PUT THE RASPBERRY IP HERE"
proxy = xmlrpc.client.ServerProxy(raspberryIP)
# Optional localhost proxy
# proxy = xmlrpc.client.ServerProxy("http://localhost:8000")


# Meno to choose registration or admin
menu_registration = st.sidebar.radio("", ("Registration", "Admin"))


######################## REGISTRATION ##############################
if menu_registration == "Registration":
    st.title("Registration")
    # Take a picture and show the result
    if st.button("Take a picture"):
        try:
            with open("imagem01.jpg", "wb") as handle:
                handle.write(proxy.TakePicture().data)
        except:
            st.title("There are no connection to the server.")

    try:
        imagem001 = Image.open("imagem01.jpg")
    except:
        st.write("The picture cannot be loaded.")

    ################# READ FILE FUNCTION #################
    # Read the name of all files in a specific path
    def TakeTheFilesNames(path):
        # List to take the name of all files
        AllFiles = []
        try:
            # Search for files
            for i in os.listdir(path):
                try:
                    # Append the name of the files
                    AllFiles.append(open(path + i))
                except:
                    print("The file cannot be appended.")
            # Return a list with file's names
            return AllFiles
        except:
            print("The path does not exist.")

    ################ END OF FUNCTION #####################

    ############## FACE ENCODING AND NAMES ###############
    # Load a sample picture and learn how to recognize it.
    def LoadNRecognize(pictures, path):
        known_face_encoding = []
        known_face_names = []
        try:
            for picture in pictures:
                load_image = face_recognition.load_image_file(picture.name)
                known_face_encoding.append(
                    face_recognition.face_encodings(load_image)[0]
                )
                known_face_names.append(
                    picture.name.replace(path, "").replace(".jpeg", "")
                )
            return (known_face_encoding, known_face_names)
        except:
            st.write("Failed.")

    ######################################################

    # Folder with registered photos
    folder_path = "Cadastrados/"
    pessoas_cadastradas = TakeTheFilesNames(folder_path)
    faces_N_names = LoadNRecognize(pessoas_cadastradas, folder_path)
    name = ""
    try:
        face_image = face_recognition.load_image_file("imagem01.jpg")
        face_encoding = face_recognition.face_encodings(face_image)[0]
        matches = face_recognition.compare_faces(faces_N_names[0], face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(faces_N_names[0], face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces_N_names[1][best_match_index]
    except:
        st.write("Process failed.")

    try:
        st.image(imagem001, caption="{}".format(name), use_column_width=True)
    except:
        st.write("The picture cannot be showed.")

    sono = st.slider("What is your slepness level?", min_value=1, max_value=5, step=1)

    # Take the current date and time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    today = date.today()

    try:
        # Enter your API key here
        api_key = "ENTER YOUR API KEY HERE"

        # base_url variable to store url
        base_url = "http://api.openweathermap.org/data/2.5/weather?"

        # Give city name
        city_name = "Londrina"  # input("Enter city name : ")

        # complete_url variable to store
        # complete url address
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name

        # get method of requests module
        # return response object
        response = requests.get(complete_url)

        # json method of response object
        # convert json format data into
        # python format data
        x = response.json()

        # print(x)

        # Now x contains list of nested dictionaries
        # Check the value of "cod" key is equal to
        # "404", means city is found otherwise,
        # city is not found
        if x["cod"] != "404":

            # store the value of "main"
            # key in variable y
            y = x["main"]

            # store the value corresponding
            # to the "temp" key of y
            current_temperature = y["temp"] - 273.15  # Convert to celsius

            # store the value corresponding
            # to the "pressure" key of y
            current_pressure = y["pressure"]

            # store the value corresponding
            # to the "humidity" key of y
            current_humidiy = y["humidity"]

            # store the value of "weather"
            # key in variable z
            z = x["weather"]

            # store the value corresponding
            # to the "description" key at
            # the 0th index of z
            weather_description = z[0]["description"]

        else:
            print(" City Not Found ")
    except:
        current_temperature = 404
        weather_description = "There are no connection."

    df_cadastro = pd.DataFrame(
        {
            "Name": [name],
            "Date": [today],
            "Time": [current_time],
            "Sleepness level": [sono],
        },
        columns=["Name", "Date", "Time", "Sleepness level"],
    )
    st.write(df_cadastro)

    df_clima = pd.DataFrame(
        {
            "City": [city_name],
            "Temperature": [current_temperature],
            "Wheater": [weather_description],
        },
        columns=["City", "Temperature", "Wheater"],
    )
    st.write(df_clima)

    if name != "Unknown":
        if name != "":
            if st.button("Submit"):
                DataBaseHUB.insertBLOB(
                    name,
                    today,
                    current_time,
                    sono,
                    city_name,
                    current_temperature,
                    weather_description,
                    "imagem01.jpg",
                )
                st.success("Done")
        else:
            st.subheader("Take another picture")
    else:
        st.subheader("You are not registered. Enter your name below to continue.")
        newperson = st.text_input("Full name: ")
        try:
            lennewnome = newperson.split()
        except:
            pass
        if len(lennewnome) <= 1:
            st.subheader("Enter you full name.")
        else:
            imagem001.save("Cadastrados/{}.jpeg".format(newperson))
            if st.button("Refresh"):
                st.success("Registered")

    # cv2.destroyAllWindows()
    # video_capture.release()


########################### ADMIN ##################################
else:
    adm_password = st.sidebar.text_input("Password:", type="password")
    # st.sidebar.markdown(adm_password)

    if adm_password == "raspdomumu":

        ################################################
        st.title("Registration analysis")

        alldata = DataBaseHUB.ReadInfo()
        if st.checkbox("Show data base"):
            st.write(alldata)

        options = [str(i).strip("',)").strip("(')") for i in DataBaseHUB.ReadName()]
        people_option = st.selectbox("Choose a person", options)

        dataperson = alldata.loc[alldata["Name"] == people_option]
        st.table(dataperson)

        #################################################
        st.subheader("Enter with file name below to save.")
        saveoption = st.radio("", ("Save all database", "Save selected person"))
        file_name = st.text_input("Nome do arquivo: ")
        if st.button("Download"):
            if saveoption == "Save all database":
                try:
                    alldata.to_csv("savedfiles/{}.csv".format(file_name), index=None)
                    st.success("Done")
                except:
                    st.write("The file has no name.")
            else:
                try:
                    dataperson.to_csv("savedfiles/{}.csv".format(file_name), index=None)
                    st.success("Done")
                except:
                    st.write("The file has no name.")
