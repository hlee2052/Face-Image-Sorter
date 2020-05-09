

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

    ratio = height/width

    if isWidthGreater:
        return (threshold_w, ratio*threshold_h)

    return (threshold_w * (1/ratio), threshold_h)

def move_file(option, imageDict, filepath, dest_dirs, user_name_list):
    """
    reads an image file (filepath) and see if it belongs to

    :param option:
        option = 1 --> copy image to any users
        option = 2 --> copy image to first user in user_name_list.
    :param imageDict:  dictionary of (userName, image_encoding)
    :param filepath: source file path
    :param dest_dirs: dictionary of (userName, destination path)
    :param user_name_list: user list priority sorted by order (if option=2)

    :return: list of users which the image file belongs
    """

    """
    1. let curr =   load image from filepath:
    2.  compare (curr with every items in imageDict's encoding)
       --> if match, then move file to destination
        (to get destination, get it from dest_dirs map)
        --> 
    
    
    """
    pass




