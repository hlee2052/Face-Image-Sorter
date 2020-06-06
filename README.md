# Face Image Sorter

A python program to sort images to different folder based on face-features, without having to manually go through each images in person.
Example: You have 1000s of images of politicians. If you want to categorize images by certain feature(eg, Trump), then this program will allow you to copy all Trump images to a folder.

- GUI created with tkinter
- face_recognition library used to extract and compare facial features

![gifmovie](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo-face-image.gif)


## Instruction

Run the script with:
```bash
python main.py
```

## Usage

1. Upload the template face (can contain at most 3 faces on image, but recommended to best face image for template).
2. Label the each face on template with name, which is the directory which image is going to be saved.
3. Select the folder which contains the images to be sorted.
4. Select the option to see if images are to be only saved to 1 folder. For example, if a single template image has face of Trump and Biden, and if the target image(s) has both Trump and Biden, then choose whether save this image to BOTH Trump and Biden directory, or only save to one of them.
5. Press sort image to sort images.
 
## ScreenShots

![demo1](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo1.png)
![demo2](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo2.png)
![demo3](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo3.png)
![demo4](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo4.png)
![demo5](https://github.com/hlee2052/Face-Image-Sorter/blob/master/screenshot/demo5.png)



