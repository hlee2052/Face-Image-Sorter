#import face_recognition

"""
known_image = face_recognition.load_image_file("trump.jpg")
unknown_image = face_recognition.load_image_file("trump2.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[1]
results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
print (results)

"""



from tkinter import Tk, Label, Button

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="test")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.click)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def click(self):
        print("press!")

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()