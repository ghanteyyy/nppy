try:
    import cv2

except (ImportError, ModuleNotFoundError):
    print('[opencv-python] cv2 package found not installed')


def capture_image(name):
    '''Capture image from your camera'''

    try:
        cam = cv2.VideoCapture(0)  # Setting default camera

        for _ in range(30):   # This loop prevents black image
            cam.read()

        ret, frame = cam.read()  # Reading each frame
        cv2.imwrite(str(name), frame)  # Saving captured frame

        cam.release()
        cv2.destroyAllWindows()

    except NameError:
        print('String value was expected')


if __name__ == '__main__':
    capture_image('Image.jpg')    # Don't forget to include '.jpg' or '.png' extension
