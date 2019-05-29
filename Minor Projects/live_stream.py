try:
    import cv2

except (NameError, ImportError, ModuleNotFoundError):
    print('cv2 package installed not found')


def live_stream():
    '''Stream your live video'''

    cam = cv2.VideoCapture(cv2.CAP_DSHOW)

    while True:
        ret, frame = cam.read()  # Getting frame
        frame = cv2.flip(frame, 180)   # Rotating frame to 180 degree

        cv2.namedWindow('LIVE STREAM', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('LIVE STREAM', (800, 600))
        cv2.imshow('LIVE STREAM', frame)

        if cv2.waitKey(1) == 27:   # Press esc to quit everything
            break

    cam.release()   # Destroying camera
    cv2.destroyAllWindows()   # Destroying all your active windows


if __name__ == '__main__':
    live_stream()
