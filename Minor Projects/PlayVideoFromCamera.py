import cv2


class PlayVideoFromCamera:
    '''Getting live video from your webcam'''

    def __init__(self, window_name='Live Stream'):
        self.window_name = window_name

    def live_stream(self):
        '''Streaming Video'''

        cam = cv2.VideoCapture(cv2.CAP_DSHOW)

        try:
            while True:
                ret, frame = cam.read()  # Getting frame

                frame = cv2.flip(frame, 180)   # Rotating frame to 180 degree

                cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(self.window_name, (800, 600))
                cv2.imshow(self.window_name, frame)

                if cv2.waitKey(1) == 27:   # Press esc to quit everything
                    break

            cam.release()   # Destroying camera
            cv2.destroyAllWindows()   # Destroying all your active windows

        except cv2.error:
            print('Camera is not connected')


if __name__ == '__main__':
    live_stream = PlayVideoFromCamera()
    live_stream.live_stream()
