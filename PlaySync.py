# file names
import threading
import requests
import keyboard
import time
import vlc


# imports
movie_name = '11.mp4'
subtitle_name = '11.srt'

# server functions
def set_data(time):
    requests.get(
        f'https://nemspace.ir/syncplay/withJQ/set_data.php?time={time}')


def get_data():
    text = requests.get(f'https://nemspace.ir/syncplay/withJQ/get_data.php')
    return int(text.text)


# initialization
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(movie_name)
player.video_set_subtitle_file(subtitle_name)
player.set_media(media)
player.play()
time.sleep(0.1)
player.pause()
player.set_time(0)
set_data(-2)

# player thread function
def movie_thread_function():
    while True:
        current_status = get_data()
        if current_status == -1:  # server playing
            if media.get_state() != 3:  # pc not playing
                player.set_pause(0)  # play pc
        else:  # server paused
            if current_status != -2:  # at some value
                player.set_time(current_status)  # go there
            if media.get_state() != 4:  # pc not paused
                player.set_pause(1)  # pause pc


def main():
    movie_thread = threading.Thread(target=movie_thread_function)
    movie_thread.start()
    already_pressed = False
    while True:
        if keyboard.is_pressed("space"):
            # pause key
            if already_pressed == False:
                if get_data() == -1:  # playing
                    set_data(-2)  # pause
                else:
                    set_data(-1)  # playing
            already_pressed = True
        elif keyboard.is_pressed("right"):
            # +5s jump key
            if already_pressed == False:
                current_time = player.get_time()
                new_time = current_time+5000
                set_data(new_time)
            already_pressed = True
        elif keyboard.is_pressed("left"):
            # -5s jump key
            if already_pressed == False:
                current_time = player.get_time()
                new_time = current_time-5000
                set_data(new_time)
            already_pressed = True
        else:
            already_pressed = False


if __name__ == "__main__":
    main()
