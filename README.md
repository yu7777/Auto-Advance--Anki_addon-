# Auto-Advance Anki addon   
This add-on has similar features with Ankimobile's auto advance feature.
<ol>
<li><b>wait for audio to finish playing. 
</b></li><li><b>automatically show answer.
</b></li><li><b>automatically choose &lt;Hard&gt; or &lt;Good&gt; and then flip card.   
</b></li><li><b>repeat specified audio field at specified play speed. </b> e.g. repeat_field = {"发音":[0.7,1.5,2.6]} , repeat 3 times at different speed
</li><li><b>slow down or speed up some selected audio files while playing.  
</b></li><li><b>mode 1: play all audios </b>(Normal study) <b>mode 0: play selected audio. </b>(Usually used for Custom Study Session. e.g. quickly review all the cards you learned today)
</li>
</ol>
    
This Anki addon can be found at  https://ankiweb.net/shared/info/1747534155

<b>Used a lot on Mac OS</b>. On <b>Linux</b> this add-on works as well as on Mac OS (tested on Ubuntu).   
<b>Windows version works</b>, but all speed setting will be ignored. It means all audios will be played with correct repeat times but only at speed 1.    
I don't use Anki on Windows, so please <b>Feel free to add any new features.</b>   

# New Features.  
Repeat audio play at differnt play speed.    
```python
repeat_field = {"发音":[0.8,1.5,2.2]} # specify repeat field and audio speed each time. Modify if applicable
    # e.g. {"voice":[0.5],"sentence":[1.5,2]} means:
    # any audio in voice field will be played once at audio speed 0.5
    # and any audio in sentence field will be played twice, one at speed 1.5 and the other at speed 2
```
Mode 0: Only play selected audio. -1 means play audio at default speed.     
NOTE: If you want to play it twice at speed 0.5 and 1.5. you can use mode_0_field = {"发音":[0.5,1.5]}
```python
mode_0_field = {"发音":[-1]}
```
Slow down or speed up some selected audio files while playing.   
```python
audio_startswith = "mdx-oalecd9_mdx" # identify audio file which start with specified letters. Modify if applicable
audio_startswith_speed_factor = 0.8 # change audio speed for identified audio files. Modify if applicable
    # e.g. audio files from different sources may have different audio speed by default.
    # my case is that the audio files from oalecd9_mdx is faster than other audio files
    # so if default audio speed is 2.0, than audio files startswith "mdx-oalecd9_mdx"
    # will be played at speed 2.0 * 0.8 = 1.6
```
Add automatically select Hard while reviewing.    
```python
answer_choice = "mw.reviewer._defaultEase()" # default ease
# answer_choice = int(2) # choose Hard
```

# Menu and Shortcuts
<p align="left">
  <img src="https://github.com/yu7777/Auto-Advance--Anki_addon-/blob/master/Screen%20Shot%202019-10-17%20at%205.05.00%20pm.png" width="550" title="menu and shortcuts">
</p>
<p align="right">
  <img src="https://github.com/yu7777/Auto-Advance--Anki_addon-/blob/master/Screen%20Shot%202019-10-17%20at%205.04.31%20pm.png" width="550" title="menu and shortcuts">
</p>
<p align="left">
  <img src="https://github.com/yu7777/Auto-Advance--Anki_addon-/blob/master/Screen%20Shot%202019-10-16%20at%204.42.45%20pm.png" width="550" title="menu and shortcuts">
</p>


# Usage

Press j or Ctrl+j to start the add on.

Press k or Ctrl+k to stop it.

Press Shift-D to add silence after front card.

Press Shift-F to add silence after back card.

Press Shift-J to add silence after both front and back cards.

Press [ to decrease the speeds of cards' audios.

Press ] to increase the speeds of cards' audios.

Press g to toggle default choice: Hard or Good

# Tips.  
1.  You can use shortcut "j" to start Auto Advance play mode BEFORE you enter your deck and click "Study Now".     
If you start Auto Advance play mode when you are reviewing a card and the audio is playing, then the first card will not be working as it should be with this add-on.     
Not sure if this is a bug. Please feel free to modify code on GitHub.     
2.  Anytime you can use shortcut "k" to stop Auto Advance play mode.     
3.  Use "[" or "]" to decrease or increase your audio play speed. This works all the time even though you don't use Auto Advance play mode.     
4.  Use Custom Study and Mode 0 to quickly review the cards (e.g. cards you learned today).
5.  When you modify config on Anki's addonManager, you need load this new config to addon. This can be done by clicking <b>load config</b> in menu Tools>>Auto Advance>>Load config. Otherwise the addon will keep using old config. When you Stop Auto Advance, the currently used config will be saved automatically.


# Original addon code.  
This Addon is a revised version of Automatically flip cards https://ankiweb.net/shared/info/631932779  https://github.com/TruongQToan/Automatically-flip-cards/tree/master
