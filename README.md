# Auto-Advance Anki addon  
This is an Anki addon which automatically show answer, make choice and then flip card.   
Similar with auto play cards function.

Currently only tested on Mac.   
Windows version need to add code to load_audio_to_player() and wait_for_audio()  

Feel free to add any new features.   

# Describition.  
This Addon is a revised version of Automatically flip cards https://ankiweb.net/shared/info/631932779  https://github.com/TruongQToan/Automatically-flip-cards/tree/master

# New Features.  
Repeat audio files at differnt play speed.    
Slow down or speed up some selected audio files while playing.   
Add automatically select Hard while reviewing.    


# Usage

Press j or Ctrl+j to start the add on.

Press k or Ctrl+k to stop it.

Press Shift-D to add silence after front card.

Press Shift-F to add silence after back card.

Press Shift-J to add silence after both front and back cards.

Press [ to decrease the speeds of cards' audios.

Press ] to increase the speeds of cards' audios.


# Config Details.  
```python
class Config(object):
    # anything related time will be count in senconds in this Config
    time_limit_question = 0 #Don't change, the value will be calculated by code
    time_limit_answer = 0 #Don't change, the value will be calculated by code
    addition_time = 0 # add more waiting time to both question and answer side. Modify if applicable
    addition_time_question = 0 # add more waiting time to question side. Modify if applicable
    addition_time_answer = 0 # add more waiting time to answer side. Modify if applicable
    add_time = True
    play = False # default flag if Auto Advance start.Don't change. Use shortcut J or k to start or stop while reviewing cards
    timer = None # Don't change
    is_question = True # Don't change
    adjust_both = False
    default_waiting_time = 2.5 # default waiting time for both sides, Modify if applicable
    audio_speed = 2.2 # default audio speed, Modify if applicable
    _soundReg = r"\[sound:(.*?)\]" # Don't change
    mode = 1 # 1: add times in all audios, 0: get time in the first audio
    stdoutQueue = Queue()
    show_notif = True # show notification or not. Modify if applicable
    show_notif_timeout = 0.8 # time of showing notification, notification will automatically disappear. Modify if applicable
    wait_for_audio = True # if wait for audio finished or not. Modify if applicable
    is_question_audio = True # Don't change
    is_answer_audio = True # Don't change
    repeat_field = {"发音":[0.8,1.5,2.2]} # specify repeat field and audio speed each time. Modify if applicable
    # e.g. {"voice":[0.5],"sentence":[1.5,2]} means:
    # any audio in voice field will be played once at audio speed 0.5
    # and any audio in sentence field will be played twice, one at speed 1.5 and the other at speed 2
    audio_startswith = "mdx-oalecd9_mdx" # identify audio file which start with specified letters. Modify if applicable
    audio_startswith_speed_factor = 0.8 # change audio speed for identified audio files. Modify if applicable
    # e.g. audio files from different sources may have different audio speed by default.
    # my case is that the audio files from oalecd9_mdx is faster than other audio files
    # so if default audio speed is 2.0, than audio files startswith "mdx-oalecd9_mdx"
    # will be played at speed 2.0 * 0.8 = 1.6
    # Thus while reviewing cards all audio files sound at similar speed
    playlist_question = [] # Don't change
    playlist_answer = [] # Don't change
    # following is your default answer choice. Modify if applicable
    # answer_choice = mw.reviewer._defaultEase() # default ease
    answer_choice = int(2) # choose Hard
    player = None # Don't change
    ignore_duplicated_field = True #if ignore duplicated field
    # e.g. i set {{发音}}{{发音}}{{发音}} in my card template so that the audio in this field
    # will be played three times. This is useful on Ankimobile.
    # but in my Mac, i need ignore duplicated field because i have already set repeat_field

```
