from tkinter import *
import tkinter.font as tkFont

import PIL
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox

import face_recognition

from src.utility import *

TITLE_FONT = ("Courier bold", 20)

NO_FACE_WARNING = 'Please choose an image file with a face, ' \
                  'or try with another image with better face coverage'

INVALID_IMAGE_WARNING = 'Please choose an image file!'

TOO_MANY_FACE_WARNING = 'Please choose an image with at most 3 faces'
TEMPLATE_FACE_LIMIT = 3

color_map = {0: 'red', 1: 'blue', 2: 'green'}


class mainWindow:

    def upload_face_image(self):
        filename = filedialog.askopenfilename()
        print('Selected:', filename)

        try:
            self.upload_image_actual = Image.open(filename)
            known_image = face_recognition.load_image_file(filename)
            encoding = face_recognition.face_encodings(known_image)

            if len(encoding) == 0:
                messagebox.showinfo('Error', NO_FACE_WARNING)
                return

            if len(encoding) > TEMPLATE_FACE_LIMIT:
                messagebox.showinfo('Error', TOO_MANY_FACE_WARNING)
                return
            # print(encoding)
            # print(len(encoding))
        except PIL.UnidentifiedImageError:
            messagebox.showinfo('Error', INVALID_IMAGE_WARNING)
            return
        # default - uploaded image with 1 face
        self.upload_multiple_faces(known_image)

    def upload_multiple_faces(self, known_image):

        curr_row = 0

        MAX_WIDTH = 400
        MAX_HEIGHT = 300

        # tuple: top right bottom left
        image_locations = face_recognition.face_locations(known_image)
        print(image_locations)

        popUp = Toplevel()
        popUp.geometry('800x800+300+300')

        Label(popUp, text='For each person, provide name', font=TITLE_FONT).grid(row=curr_row, column=0, sticky=N)
        curr_row += 1

        width, height = self.upload_image_actual.size

        print(width)
        print(height)

        new_width, new_height = correct_img_dimension(width, height, MAX_WIDTH, MAX_HEIGHT)
        new_width, new_height = int(new_width), int(new_height)

        # input_image = self.upload_image_actual.resize(new_width, new_height)
        input_image = self.upload_image_actual

        tk_image = ImageTk.PhotoImage(input_image)

        canvas = Canvas(popUp, width=width, height=height)
        canvas.img = tk_image

        image_offset_x = 20
        image_offset_y = 20

        canvas.create_image(0, 0, anchor=NW, image=tk_image)
        # x1,y1,x2,y2.  left top right bottom

        for i in range(len(image_locations)):
            left = image_locations[i][3]
            right = image_locations[i][1]
            top = image_locations[i][0]
            bottom = image_locations[i][2]
            canvas.create_rectangle(left, top, right, bottom, outline=color_map.get(i))

        canvas.grid(row=curr_row, column=0, columnspan=2)
        curr_row += 1

        """
        template_image = Label(popUp, image=tk_image)
        template_image.grid(row=1, column=0)
        template_image.test = tk_image
        """

        Label(popUp, text='Assign name for each square', font=TITLE_FONT).grid(row=2, column=0, sticky=W)
        curr_row += 1

        """ 
        generate input box
        """
        ## this is for keep track of inputs
        # must make sure they are the same
        labelArr = []

        # frame for name inputs
        frame_name_input = Frame(popUp)
        for i in range(len(image_locations)):
            label = Label(frame_name_input, text="box " + color_map.get(i), font=TITLE_FONT, fg=color_map.get(i))
            label.grid(row=i, column=0, sticky=W)
            entry = Entry(frame_name_input)
            entry.grid(row=i, column=1, sticky=W)
            labelArr.append(entry)

        frame_name_input.grid(row=curr_row, column=0, sticky=W)
        curr_row += 1

        Button(popUp, text='Okay!!!!', command=lambda: self.submit_name(labelArr)).grid(row=curr_row)

        print('--------')
        print(len(labelArr))

        popUp.grab_set()

        # for root
        self.upload_image_actual = self.upload_image_actual.resize((220, 280))
        self.upload_image_actual = ImageTk.PhotoImage(self.upload_image_actual)
        self.upload_image.configure(image=self.upload_image_actual)
        pass

    def submit_name(self, arr):
        print("test")
        print(arr[0].get())

        input_set = set()
        for item in arr:
            current_input = item.get()

            if not current_input:
                messagebox.showinfo('Error', "Name should not be empty!")
                return

            if current_input in input_set:
                messagebox.showinfo('Error', "Name should be unique!!!")
                return
            input_set.add(current_input)



    def __init__(self, window):
        self.root = window

        # Title
        self.title = Label(root, text='Face Image Sorter', font=TITLE_FONT)
        self.title.grid(row=0, column=1, pady=(20, 0), sticky=W)

        # the actual template
        self.upload_image_actual = None
        self.imageDict = {}

        # label - Upload face
        self.upload_ref = Label(root, text='Upload reference face')
        self.upload_ref.grid(row=1, column=0, sticky=W)

        # Default template
        self.template_image = ImageTk.PhotoImage(file="image/upload_template.png")
        self.upload_image = Label(self.root, image=self.template_image)
        self.upload_image.template_image = self.template_image
        self.upload_image.grid(row=2, rowspan=3, column=0)

        # Upload Template
        upload_button = Button(root, text='Upload Face', command=self.upload_face_image)
        upload_button.grid()

        self.random = Label(root, text='Random assortment', font=TITLE_FONT).grid(row=2, column=1, sticky=N)
        Label(root, text='Random assortment', font=TITLE_FONT).grid(row=3, column=1, sticky=N)
        Label(root, text='Random assortment', font=TITLE_FONT).grid(row=4, column=1, sticky=N)


root = Tk()
root.geometry("800x600+300+300")
# root.grid_rowconfigure(0, minsize=50)  # Here
mainWindow(root)
# photo = ImageTk.PhotoImage(file="image/upload_template.png")
# label = Label(image=photo).grid(row=0, column=0)

root.mainloop()
