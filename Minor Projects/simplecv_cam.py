try:
    from SimpleCV import Camera       # This module allows you to access with camera

except (ImportError, ModuleNotFoundError):
    print('Download SimpleCV from >>>   https://sourceforge.net/projects/simplecv/files/latest/download?source=files')


def capture_image(name):
    '''Capture image from your camera'''

    cam = Camera()
    pic = cam.getImage()
    pic.save(name)


if __name__ == '__main__':
    capture_image('Image.jpg')   # Don't forget to include extension either '.jpg' or 'png'
