from tkinter import *
import tkinter.font as tkFont

import PIL
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox

import face_recognition

known_image = face_recognition.load_image_file("image/twoPeople.jpg")
unknown_image = face_recognition.load_image_file("image/onePerson.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
print(results)