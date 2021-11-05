from SimpleCV import Camera


class SimpleCVCam:
    def __init__(self, name):
        self.name = 'Image.jpg'
        self.download_link = 'https://sourceforge.net/projects/simplecv/files/latest/download?source=files'

    def capture(self):
        '''Capture image from your camera'''

        cam = Camera
        cap = cam.getImage()
        cap.save(self.name)


if __name__ == '__main__':
    simple_cv = SimpleCVCam('Image.jpg')
    simple_cv.capture()
