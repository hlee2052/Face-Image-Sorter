from tkinter import *
import tkinter.font as tkFont
import imghdr
import PIL
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox

import face_recognition, os

from src.utility import *

TITLE_FONT = ("Courier bold", 20)

NO_FACE_WARNING = 'Please choose an image file with a face, ' \
                  'or try with another image with better face coverage'

INVALID_IMAGE_WARNING = 'Please choose an image file!'

TOO_MANY_FACE_WARNING = 'Please choose an image with at most 3 faces'
TEMPLATE_FACE_LIMIT = 3

color_map = {0: 'red', 1: 'blue', 2: 'green'}


class mainWindow:

    def sort_image(self):
        option = self.radio_response.get()

        """
        if option == 0:
            messagebox.showinfo('Error', "Please select an option to see if duplicate is allowed")
            return
        if not self.directory:
            messagebox.showinfo('Error', "Choose a directory with images")
            return

        if len(self.imageDict) == 0:
            messagebox.showinfo('Error', "Please upload a template face image, or make sure the template is a face")
            return

        """
        # do not create directory until directory can be created

        # dictionary of (username, user's folder path)
        destination_path = {}
        newly_created_folders = []

        for key in self.imageDict:
            new_folder_path = self.directory + "/" + key
            if not os.path.isdir(new_folder_path):
                os.mkdir(new_folder_path)
                destination_path.update({key: new_folder_path})
                newly_created_folders.append(key)
            else:
                destination_path.update({key: new_folder_path})

                """
                # try make new folder but do let user know
                i = 20
                for num in range(0, i):
                    new_folder_path = self.directory + "/" + key + str(num)
                    if not os.path.isdir(new_folder_path):
                        os.mkdir(new_folder_path)
                        # folder_new_dirs.append(key+str(num))
                        destination_path.update({key: new_folder_path})
                        newly_created_folders.append(key + str(num))
                        break
                    if num == i - 1:
                        messagebox.showinfo('Error', "Please re-upload face with unique folder name")
                 """

        """
        if the image has 2 or more faces:
        option = 1 --> copy image to each users fold
        option = 2 --> copy image to just 1 of them
        """

        for currPath, dirs, files in os.walk(self.directory):
            for file in files:
                filepath = os.path.join(currPath, file)
                if imghdr.what(filepath) is not None:
                    move_file(option, self.imageDict, filepath, destination_path, self.user_names_string)

        new_dirs_string = ""
        for item in newly_created_folders:
            new_dirs_string += item + ", "

        messagebox.showinfo('Info', "The following directories have been created: " + new_dirs_string)

    def select_directory(self):
        self.directory = filedialog.askdirectory()
        new_dir_label = "directory:  " + self.directory
        self.directory_label.configure(text=new_dir_label)

    def upload_face_image(self):
        filename = filedialog.askopenfilename()
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
        encodings = face_recognition.face_encodings(known_image)

        self.popUp = Toplevel()
        self.popUp.geometry('800x800+300+300')

        Label(self.popUp, text='For each person, provide name', font=TITLE_FONT).grid(row=curr_row, column=0, sticky=N)
        curr_row += 1

        width, height = self.upload_image_actual.size

        new_width, new_height = correct_img_dimension(width, height, MAX_WIDTH, MAX_HEIGHT)
        new_width, new_height = int(new_width), int(new_height)

        # input_image = self.upload_image_actual.resize(new_width, new_height)
        input_image = self.upload_image_actual

        tk_image = ImageTk.PhotoImage(input_image)

        canvas = Canvas(self.popUp, width=width, height=height)
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

        Label(self.popUp, text='Assign name for each square', font=TITLE_FONT).grid(row=2, column=0, sticky=W)
        curr_row += 1

        """ 
        generate input box
        """
        ## this is for keep track of inputs
        self.user_name_input = []

        # frame for name inputs
        frame_name_input = Frame(self.popUp)

        for i in range(len(image_locations)):
            label = Label(frame_name_input, text="box " + color_map.get(i), font=TITLE_FONT, fg=color_map.get(i))
            label.grid(row=i, column=0, sticky=W)
            entry = Entry(frame_name_input)
            entry.grid(row=i, column=1, sticky=W)
            self.user_name_input.append(entry)

        frame_name_input.grid(row=curr_row, column=0, sticky=W)
        curr_row += 1

        Button(self.popUp, text='Okay!!!!',
               command=lambda: self.submit_name(self.user_name_input, encodings)) \
            .grid(row=curr_row)

        self.popUp.grab_set()

        # for root
        self.upload_image_actual = self.upload_image_actual.resize((220, 280))
        self.upload_image_actual = ImageTk.PhotoImage(self.upload_image_actual)

        self.upload_image.configure(image=self.upload_image_actual)
        pass

    def submit_name(self, user_name_input, image_encodings):
        input_set = set()

        tmp_user_list = []
        for item in user_name_input:
            current_input = item.get()
            # print(current_input)

            if not current_input:
                messagebox.showinfo('Error', "Name should not be empty!")
                return
            if current_input in input_set:
                messagebox.showinfo('Error', "Name should be unique!!!")
                return
            tmp_user_list.append(current_input)

            self.user_names_string.append(current_input)

        for name in self.user_name_list_label:
            name.destroy()

        self.imageDict = {}
        self.user_names_string = tmp_user_list;

        # better to separate into another loop
        for i in range(len(user_name_input)):
            self.imageDict.update({user_name_input[i].get(): image_encodings[i]})

            each_entry = Label(root, text=user_name_input[i].get(), font=TITLE_FONT)
            each_entry.grid(row=3 + i, column=1, sticky=W)
            self.user_name_list_label.append(each_entry)

            pass
        self.popUp.destroy()

    def __init__(self, window):
        self.root = window
        self.popUp = None

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
        self.upload_image.grid(row=2, rowspan=15, column=0)

        # Upload Template
        upload_button = Button(root, text='Upload Face', command=self.upload_face_image)
        upload_button.grid()

        self.user_name_list_label = []
        self.user_name_input = []

        self.random = Label(root, text='List of faces:', font=TITLE_FONT)
        self.random.grid(row=2, column=1, sticky=N)

        self.sort_files = Label(root, text='Select options', font=TITLE_FONT)
        self.sort_files.grid(row=2, column=2, sticky=N)

        self.radio_response = IntVar()

        radio_allow_duplicate = Radiobutton(root, text="Copy image for each user", variable=self.radio_response,
                                            value=1)
        radio_allow_duplicate.grid(row=4 + 1, column=2, sticky=W)

        radio_by_ranking = Radiobutton(root, text="Decide which directory to save by user list",
                                       variable=self.radio_response, value=2)
        radio_by_ranking.grid(row=5 + 2, column=2, sticky=W)

        self.directory = ""
        select_directory_button = Button(root, text='Choose folder directory', command=self.select_directory)
        select_directory_button.grid(row=8, column=2, sticky=N)

        self.directory_label = Label(root, text='directory:')
        self.directory_label.grid(row=9, column=2, sticky=W)

        submit_button = Button(root, text='sort image!', command=self.sort_image)
        submit_button.grid(row=10, column=2, sticky=W)

        self.user_names_string = []


root = Tk()
root.geometry("800x600+300+300")
mainWindow(root)

root.mainloop()
