import cv2


class Open_CV:
    '''Capture image from your camera'''

    def __init__(self, image_name):
        self.image_name = image_name
        self.download_link = 'pip install opencv-python'

    def capture(self):
        '''Capturing Image'''

        try:
            cam = cv2.VideoCapture(0)  # Setting default camera

            for _ in range(30):   # This loop prevents black image
                cam.read()

            ret, frame = cam.read()  # Reading each frame
            cv2.imwrite(self.image_name, frame)  # Saving captured frame

            cam.release()
            cv2.destroyAllWindows()

        except cv2.error:
            print('Camera is not connected')


if __name__ == '__main__':
    open_cv = Open_CV('Image.jpg')    # Don't forget to include '.jpg' or '.png' extension
    open_cv.capture()
