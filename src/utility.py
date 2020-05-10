import face_recognition, os
from shutil import copyfile, move


def correct_img_dimension(width, height, threshold_w, threshold_h):
    """
    return a new width and height that is as close as to the thresholds, while keeping
    aspect ratio same

    :param width:
    :param height:
    :param threshold_w:
    :param threshold_h:
    :return: tuple of new width and height
    """

    isWidthGreater = False
    if width > height:
        isWidthGreater = True

    ratio = height / width

    if isWidthGreater:
        return (threshold_w, ratio * threshold_h)

    return (threshold_w * (1 / ratio), threshold_h)


def move_file(option, imageDict, filepath, dest_dirs, user_name_list):
    """
    reads an image file (filepath) and see if it belongs to

    :param option:
        option = 1 --> copy image to any users
        option = 2 --> MOVE image to first user in user_name_list.
    :param imageDict:  dictionary of (userName, image_encoding)
    :param filepath: source file path
    :param dest_dirs: dictionary of (userName, destination path)
    :param user_name_list: user list priority sorted by order (if option=2)

    :return: list of users which the image file belongs
    """

    curr_image = face_recognition.load_image_file(filepath)

    # this may contain 0 or more faces
    current_encodings = face_recognition.face_encodings(curr_image)

    for i, user in enumerate(user_name_list):
        for encoding in current_encodings:
            is_same = face_recognition.compare_faces([imageDict[user]], encoding)
            if is_same[0]:
                file_name = filepath.split('\\')
                file_name = file_name[len(file_name) - 1]

                # just add to any users directory
                user_dest = dest_dirs[user]  # dest folder
                user_dest += "/" + file_name

                try:
                    copyfile(filepath, user_dest)
                except:
                    # if same file, just pass
                    pass
                if option == 2:  # if only want to copy to 1 user
                    return


def delete_file(file):
    if os.path.isfile(file):
        os.remove(file)
