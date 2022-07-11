import soundfile
import sounddevice


class Record_Sound:
    def __init__(self, name='Record.wav', rate=40000, duration=60):
        self.name = name           # .wav (extension)
        self.rate = rate           # Hertz
        self.duration = duration   # Seconds

    def record_sound(self):
        '''Record sound from your speaker'''

        data = sounddevice.rec(int(self.rate * self.duration), samplerate=self.rate, channels=1, blocking=True)  # Recording ...
        soundfile.write(self.name, data, self.rate)   # Saving the file


if __name__ == '__main__':
    record = Record_Sound()
    record.record_sound()
