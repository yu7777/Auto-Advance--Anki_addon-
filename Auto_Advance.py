from anki import hooks, sound
from aqt import mw, utils
from aqt.qt import *
from aqt import progress
import time
from aqt.utils import getText
from anki.utils import  isWin
from aqt.reviewer import Reviewer
import string
from .mutagen.mp3 import MP3
from .mutagen.mp4 import MP4
from .mutagen import contextlib
import platform
import wave
import time
import os, subprocess
import anki.sound
from threading import Event
from threading import Condition
from threading import Thread
from threading import Thread
from .mutagen.Queue import Queue, Empty
from .mutagen.Queue import Queue
from anki.sound import play, mpvManager
from anki.sound import mplayerQueue, mplayerClear, mplayerEvt
from anki.sound import MplayerMonitor
from anki.hooks import addHook, wrap, runHook
from aqt.utils import showInfo
import re



class CustomMessageBox(QMessageBox):

    def __init__(self, *__args):
        QMessageBox.__init__(self, parent=mw.app.activeWindow() or mw)
        self.timeout = 0
        self.autoclose = False
        self.currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoclose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)

    @staticmethod
    def showWithTimeout(timeoutSeconds, message, title, icon=QMessageBox.Information, buttons=QMessageBox.Ok):
        w = CustomMessageBox()
        w.autoclose = True
        w.timeout = timeoutSeconds
        w.setText(message)
        w.setWindowTitle(title)
        w.setIcon(icon)
        sg = w.parent().rect()
        x = sg.width() / 2 - w.pos().x() - w.rect().width()
        y = sg.height() / 2 - w.pos().y() - w.rect().height()
        w.move(x, y)
        w.exec_()


class Config(object):
    # anything related time will be count in senconds in this Config
    time_limit_question = 0 #Don't change, the value will be calculated by code
    time_limit_answer = 0 #Don't change, the value will be calculated by code
    addition_time = 0 # add more waiting time to both question and answer side. Modify if applicable
    addition_time_question = 0 # add more waiting time to question side. Modify if applicable
    addition_time_answer = 0.5 # add more waiting time to answer side. Modify if applicable
    add_time = True
    play = False # default flag if Auto Advance start.Don't change. Use shortcut J or k to start or stop while reviewing cards
    timer = None # Don't change
    is_question = True # Don't change
    adjust_both = False
    default_waiting_time = 0.5 # default waiting time for both sides, Modify if applicable
    audio_speed = 2.2 # default audio speed, Modify if applicable
    _soundReg = r"\[sound:(.*?)\]" # Don't change
    mode = 1 # 1: add times in all audios, 0: get time in the first audio
    stdoutQueue = Queue()
    show_notif = True # show notification or not. Modify if applicable
    show_notif_timeout = 0.8 # time of showing notification, notification will automatically disappear. Modify if applicable
    wait_for_audio = True # if wait for audio finished or not. Modify if applicable
    is_question_audio = True # Don't change
    is_answer_audio = True # Don't change
    repeat_field = {"发音":[0.7,1.6,2.8]} # specify repeat field and audio speed each time. Modify if applicable
    # e.g. {"voice":[0.5],"sentence":[1.5,2]} means:
    # any audio in voice field will be played once at audio speed 0.5
    # and any audio in sentence field will be played twice, one at speed 1.5 and the other at speed 2
    audio_startswith = "mdx-oalecd9_mdx" # identify audio file which start with specified letters. Modify if applicable
    audio_startswith_speed_factor = 0.6 # change audio speed for identified audio files. Modify if applicable
    # e.g. audio files from different sources may have different audio speed by default.
    # my case is that the audio files from oalecd9_mdx is faster than other audio files
    # so if default audio speed is 2.0, than audio files startswith "mdx-oalecd9_mdx"
    # will be played at speed 2.0 * 0.6 = 1.2
    # Thus while reviewing cards all audio files sound at similar speed
    playlist_question = [] # Don't change
    playlist_answer = [] # Don't change
    # following is your default answer choice. Modify if applicable
    # answer_choice = mw.reviewer._defaultEase() # default ease
    answer_choice = int(2) # chose Hard
    player = None # Don't change
    ignore_duplicated_field = True #if ignore duplicated field
    # e.g. i set {{发音}}{{发音}}{{发音}} in my card template so that the audio in this field
    # will be played three times. This is useful on Ankimobile.
    # but in my Mac, i need ignore duplicated field because i have already set repeat_field

    def __init__(self):
        pass


def find_audio_fields(card):
    audio_fields = []
    fields_with_audio = {}
    for field, value in card.note().items():
        match = re.findall(Config._soundReg, value)
        if match:
            audio_fields.append(field)
            fields_with_audio[field] = match
    return audio_fields, fields_with_audio


def split_audio_fields(card, m, audio_fields):
    def helper(q):
        q_times = []
        start = 0
        while True:
            s = q.find('{{', start)
            if s == -1: break
            e = q.find('}}', s)
            if e != -1:
                if q[s + 2:e] in audio_fields:
                    q_times.append(q[s + 2:e][:])
                start = e + 2
            else: break
        return q_times

    question_audio_fields = []
    answer_audio_fields = []
    if card is not None:
        t = m['tmpls'][card.ord]
        q = t.get('qfmt')
        a = t.get('afmt')
        question_audio_fields.extend(helper(q))
        answer_audio_fields.extend(helper(a))
    if question_audio_fields:
        Config.is_question_audio = True
    else:
        Config.is_question_audio = False
    if answer_audio_fields:
        Config.is_answer_audio = True
    else:
        Config.is_answer_audio = False
    #utils.showInfo(str(question_audio_fields))
    #utils.showInfo(str(answer_audio_fields))
    if Config.ignore_duplicated_field:
        question_audio_fields = list(dict.fromkeys(question_audio_fields))
        answer_audio_fields = list(dict.fromkeys(answer_audio_fields))
    return question_audio_fields, answer_audio_fields


def calculate_file_length(suffix, mp):
    if not os.path.exists(mp):
        return 0
    if suffix == 'mp3':
        audio = MP3(mp)
        length = str(audio.info.length)
        time = int(float(length) * 1000)
    elif suffix == 'wav':
        with contextlib.closing(wave.open(mp, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            length = frames / float(rate)
            time = int(float(length) * 1000)
    elif suffix == 'm4a':
        audio = MP4(mp)
        length = str(audio.info.length)
        time = int(float(length) * 1000)
    else:
        time = 0
    return time

def get_audio_speed(audio, field, audio_time):
    playlist_single = []
    time_tmp = 0
    if audio.startswith(Config.audio_startswith):
        speed = Config.audio_speed * Config.audio_startswith_speed_factor
    else:
        speed = Config.audio_speed
    if field in Config.repeat_field.keys():
        for speed in Config.repeat_field[field]:
            playlist_single.append((audio,speed))
            time_tmp += audio_time / speed
        return playlist_single, time_tmp
    playlist_single.append((audio,speed))
    time_tmp += audio_time / speed
    return playlist_single, time_tmp


def calculate_time(media_path, audio_fields, fields_with_audio):
    time = 0
    playlist = []
    if len(audio_fields) > 0:
        for field in audio_fields:
            audios_in_field = fields_with_audio[field]
            for audio in audios_in_field:
                path = media_path + audio
                audio_time = calculate_file_length(audio[-3:], path)
                playlist_single, time_tmp = get_audio_speed(audio, field, audio_time)
                playlist.extend(playlist_single)
                time += time_tmp
                if Config.mode == 0: break #first audio
            if Config.mode == 0: break #first field
    if time == 0:
        time = Config.default_waiting_time * 1000
    else:
        time += len(playlist) * 250
    return time, playlist

def set_time_limit():
    card = mw.reviewer.card
    # need to False autoplay of anki.
    if card is not None:
        note = card.note()
        model = note.model()
        audio_fields, fields_with_audio = find_audio_fields(card)
        audio_fields_q, audio_fields_a = split_audio_fields(card, model, audio_fields)
        if isWin:
            media_path = mw.col.path.rsplit('\\', 1)[0] + '\\collection.media\\'
        else:
            media_path = mw.col.path.rsplit('/', 1)[0] + '/collection.media/'
        time_question, playlist_question = calculate_time(media_path, audio_fields_q, fields_with_audio)
        time_answer, playlist_answer = calculate_time(media_path, audio_fields_a, fields_with_audio)
        Config.playlist_question = playlist_question
        Config.playlist_answer = playlist_answer

        Config.time_limit_question = time_question + int((Config.addition_time + Config.addition_time_question) * 1000)
        Config.time_limit_answer = time_answer + int((Config.addition_time + Config.addition_time_answer) * 1000)

    return

def load_audio_to_player(playlist):
    if not playlist:
        return
    if isWin:
        #not test in Windows
        pass
    else:
        if not Config.player:
            # print('set up sound')
            setupSound()
        for file,speed in playlist:
            try:
                path = os.path.join(os.getcwd(), file)
                Config.player.command("loadfile", path, "append-play","speed="+ f"{speed:.2f}")
            except:
                print('something wrong while loading file to MPV')
                break


def setupSound():
    if isWin:
        return
    try:
        if mpvManager:
            Config.player = mpvManager
        else:
            anki.sound.setupMPV()
            Config.player = mpvManager
    except FileNotFoundError:
        print("mpv not found, reverting to mplayer")
    except anki.mpv.MPVProcessError:
        print("mpv too old, reverting to mplayer")

def wait_for_audio():
    if isWin:
        pass
    else:
        i = 0
        while True and (i < 5):
            i += 1
            if Config.player:
                try:
                    if Config.player.get_property("idle-active"):
                        # print('not playing')
                        break
                    else:
                        t_remain = Config.player.get_property("playtime-remaining")
                        # print(str(i)+" times try")
                        # print(t_remain)
                        time.sleep(max(t_remain+0.05,0.1))
                except:
                    try:
                        anki.sound.cleanupMPV()
                        Config.player = None
                    except:
                        pass


def show_answer():
    if Config.wait_for_audio and Config.is_question_audio:
        wait_for_audio()
    if mw.reviewer and mw.col and mw.reviewer.card and mw.state == 'review':
        Config.is_question = False
        if mw.reviewer.typedAnswer == None:
            mw.reviewer.typedAnswer = ""
        mw.reviewer._showAnswer()
    if Config.play:
        Config.timer = mw.progress.timer(Config.time_limit_answer, change_card, False)
        load_audio_to_player(Config.playlist_answer)

def change_card():
    if Config.wait_for_audio and Config.is_answer_audio:
        wait_for_audio()
    if mw.reviewer and mw.col and mw.reviewer.card and mw.state == 'review':
        Config.is_question = True
        mw.reviewer._answerCard(Config.answer_choice)

def check_valid_card():
    # utils.showInfo("Check Valid Card")
    card = mw.reviewer.card
    if card is None: return False
    if card.note() is None: return False
    return True

def show_question():
    if not check_valid_card():
        return
    set_time_limit()
    if Config.play:
        Config.timer = mw.progress.timer(Config.time_limit_question, show_answer, False)
        load_audio_to_player(Config.playlist_question)

def mask_autoplay(self,card):
    if Config.play:
        return False
    else:
        return self.mw.col.decks.confForDid(card.odid or card.did)['autoplay']

def start():
    if Config.play: return
    Reviewer.autoplay = mask_autoplay
    apply_audio_speed()
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Auto Advance: start", "Message")
    sound.clearAudioQueue()
    if Config.add_time:
        set_time_limit()
        Config.add_time = False
    hooks.addHook("showQuestion", show_question)
    Config.play = True
    if mw.reviewer.state == 'question':
        if check_valid_card():
            show_answer()
    elif mw.reviewer.state == 'answer':
        if check_valid_card():
            change_card()

def stop():
    #global audio_speed
    if not Config.play:
        return
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Auto Advance: stop", "Message")
    Config.play = False
    hooks.remHook("showQuestion",show_question)
    if Config.timer is not None:
        Config.timer.stop()
    Config.timer = None
    # Config.audio_speed = 1.0


def add_time_base(t=1):
    if Config.play:
        stop()
    if t == 1:
        at = utils.getText("Add additional time for questions and answers")
    elif t == 2:
        at = utils.getText("Add additional time for questions")
    else:
        at = utils.getText("Add additional time for answers")
    if at is not None and len(at) > 0:
        try:
            at = float(at[0])
        except:
            utils.showInfo('You must enter a positive number between 0 and 20!')
            return
    else:
        return
    if at >= 0 and at <= 20:
        if t == 1:
            Config.addition_time = at
            utils.showInfo('Set additional time for questions and answers')
        elif t == 2:
            Config.addition_time_question = at
            utils.showInfo('Set additional time for questions')
        else:
            Config.addition_time_answer = at
            utils.showInfo('Set additional time for answers')
        Config.add_time = True
    else:
        utils.showInfo('Invalid additional time. Time value must be in the range 0 to 20')


def change_default_waiting_time():
    if Config.play:
        stop()
    default_waiting_time = utils.getText("Change default waiting time")
    if default_waiting_time is not None and len(default_waiting_time) > 0:
        try:
            default_waiting_time = float(default_waiting_time[0])
        except:
            utils.showInfo('You must enter a positive number between 0 and 20!')
            return
    else:
        return
    if default_waiting_time >= 0 and default_waiting_time <= 20:
        Config.default_waiting_time = default_waiting_time
    else:
        utils.showInfo('Invalid additional time. Time value must be in the range 0 to 20')


def add_time():
    add_time_base(1)


def add_time_question():
    add_time_base(2)


def add_time_answer():
    add_time_base(3)


def switch_mode():
    Config.mode = 1 - Config.mode
    if Config.mode == 1:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Get time of all audios", "Message")
    else:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Only get time of the first audio", "Message")

def toggle_show_notification():
    Config.show_notif = not Config.show_notif

def toggle_wait_for_audio():
    Config.show_notif = not Config.show_notif

def decrease_audio_speed():
    Config.audio_speed = max(0.1, Config.audio_speed - 0.1)
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Decrease audio speed. Current speed flip: " + f"{Config.audio_speed:.1f}", "Message")
    apply_audio_speed()

def increase_audio_speed():
    Config.audio_speed = min(4.0, Config.audio_speed + 0.1)
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Increase audio speed. Current speed flip: " + f"{Config.audio_speed:.1f}", "Message")
    apply_audio_speed()

def pause_flip():
    if not Config.play: return
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, "Automatically flip cards: Pause", "Message")
    audio_pause()
    Config.play = False
    hooks.remHook("showQuestion",show_question)
    if Config.timer is not None:
        Config.timer.stop()
    # Config.timer = None

def apply_audio_speed():
    if isWin:
        if anki.sound.mplayerManager is not None:
            if anki.sound.mplayerManager.mplayer is not None:
                anki.sound.mplayerManager.mplayer.stdin.write(b"af_add scaletempo=stride=10:overlap=0.8\n")
                anki.sound.mplayerManager.mplayer.stdin.write((b"speed_set %f \n" % Config.audio_speed))
    else:
        if anki.sound.mpvManager is not None:
            if anki.sound.mpvManager.command is not None:
                    anki.sound.mpvManager.set_property("speed", Config.audio_speed)

def audio_pause():
    if isWin:
        if anki.sound.mplayerManager is not None:
            if anki.sound.mplayerManager.mplayer is not None:
                anki.sound.mplayerManager.mplayer.stdin.write("pause\n")
    else:
        if anki.sound.mpvManager is not None:
            anki.sound.mpvManager.togglePause()

def toggle_choice_hard_good():
    if Config.answer_choice == int(2):
        Config.answer_choice = mw.reviewer._defaultEase()
        choice = "Good"
    else:
        Config.answer_choice = int(2)
        choice = "Hard"
    if Config.show_notif:
        CustomMessageBox.showWithTimeout(Config.show_notif_timeout, \
        "Default choice: " + choice, "Message")


def auto_option():
    pass
    # d = MyDialog()
    # if d.exec():
    #     showInfo('dialog closed')

afc = mw.form.menuTools.addMenu("Auto Advance")

action = QAction("Option...", mw)
action.triggered.connect(auto_option)
afc.addAction(action)


action = QAction("Start automatically flipping card", mw)
action.setShortcut('j')
action.triggered.connect(start)
afc.addAction(action)

action = QAction("Stop automatically flipping card", mw)
action.setShortcut('k')
action.triggered.connect(stop)
afc.addAction(action)

action = QAction("Start automatically flipping card", mw)
action.setShortcut('Ctrl+j')
action.triggered.connect(start)
afc.addAction(action)

action = QAction("Stop automatically flipping card", mw)
action.setShortcut('Ctrl+k')
action.triggered.connect(stop)
afc.addAction(action)

action = QAction("Switch mode", mw)
action.setShortcut('Ctrl+y')
action.triggered.connect(switch_mode)
afc.addAction(action)

action = QAction("Add additional time", mw)
action.setShortcut('Shift+J')
action.triggered.connect(add_time)
afc.addAction(action)

action = QAction("Add additional time to questions", mw)
action.setShortcut('Shift+D')
action.triggered.connect(add_time_question)
afc.addAction(action)

action = QAction("Add additional time to answers", mw)
action.setShortcut('Shift+F')
action.triggered.connect(add_time_answer)
afc.addAction(action)

action = QAction("Change default waiting time", mw)
action.setShortcut("Shift+L")
action.triggered.connect(change_default_waiting_time)
afc.addAction(action)

action = QAction("Don't show notification", mw)
action.setCheckable(True)
action.triggered.connect(toggle_show_notification)
afc.addAction(action)

action = QAction("Decrease audio speed", mw)
action.setShortcut("[")
action.triggered.connect(decrease_audio_speed)
afc.addAction(action)
#
action = QAction("Increase audio speed", mw)
action.setShortcut("]")
action.triggered.connect(increase_audio_speed)
afc.addAction(action)
#
action = QAction("Pause audio playback", mw)
action.setShortcut("p")
action.triggered.connect(audio_pause)
afc.addAction(action)

action = QAction("Toggle Choice: Hard or Good", mw)
action.setShortcut("g")
action.triggered.connect(toggle_choice_hard_good)
afc.addAction(action)

# action = QAction("Pause audio playback and card flip", mw)
# action.setShortcut("p")
# action.triggered.connect(pause_flip)
# afc.addAction(action)
