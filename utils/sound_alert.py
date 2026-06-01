import threading
import winsound


def play_fire_alarm():

    def sound():
        winsound.Beep(1500, 500)
        winsound.Beep(1500, 500)
        winsound.Beep(1500, 500)

    threading.Thread(target=sound, daemon=True).start()