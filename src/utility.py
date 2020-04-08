

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









