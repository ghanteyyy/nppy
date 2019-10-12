try:
    import soundfile
    import sounddevice

except (NameError, ImportError, ModuleNotFoundError):
    print('Either soundfile or sounddevice is not installed')


def rec_sound():
    '''Record sound from your speaker'''

    rec_rate = 40000  # Hertz
    rec_duration = 10  # seconds
    rec_name = 'names.wav'  # Giving name to file. Don't forget to give extension 'wav'

    rec_data = sounddevice.rec(int(rec_rate * rec_duration), samplerate=rec_rate, channels=1, blocking=True)  # Recording ...
    soundfile.write(rec_name, rec_data, rec_rate)   # Saving the file


if __name__ == '__main__':
    rec_sound()
