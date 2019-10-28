 Anything related time will be count in <b>senconds</b> in this config.  
#### Time sequence.
<li>show <b>Question.</b>   
 Time of audio play (if no audio play, use default_waiting_time) + addition\_time + addition\_time\_question.</li>
<li>show <b>Answer.</b>   
Time of audio play (if no audio play, use default_waiting_time) + addition\_time + addition\_time\_answer + temp\_answer\_addition\_time (if you use shortcut , or . to set a temporary answer action, prefered because you can do this even when card is on question side and answer buttons are not showing. Note: before this add-on take answer action and flip card, you can always use default answer buttons or shortcuts 1,2,3,4 to manually choose your own answer)</li>
<li><b>Action</b> Again, Hard or Good. Then next card.
</li>
#### Windows version will ignore any speed setting.
**"audio_speed"**: 2.2, This is the default play speed, you can change it with shortcuts [ or ].   
**"mode"**: 1, play all audios (Normal study) mode 0: play selected audio.(Usually used for Custom Study Session. e.g. quickly review all the cards you learned today).  
**"mode\_0\_field"**: {"发音":[-1]},  Mode 0 selected field "发音". -1 means play audio at default speed. NOTE: If you want to play it twice at speed 0.5 and 1.5. you can use mode_0_field = {"发音":[0.5,1.5]}   
**"show\_notif"**: true, #if show notification or not.   
**"show\_notif\_timeout"**: 0.8,   
**"wait\_for\_audio"**: true,   
**"repeat\_field"**: {"发音":[0.7,1.5,2.6]},    
 specify repeat field and audio speed each time.<br>
 e.g. {"voice":[0.5],"sentence":[1.5,2]} means:<br>
 any audio in voice field will be played once at audio speed 0.5, and any audio in sentence field will be played twice, one at speed 1.5 and the other at speed 2.  
**"audio\_startswith"**: "mdx-oalecd9\_mdx",   
**"audio\_startswith\_speed\_factor"**: 0.6, change audio speed for identified audio files by "audio\_startswith". e.g. audio files from different sources may have different audio speed by default. My case is that the audio files from oalecd9\_mdx is faster than other audio files, so if default audio speed is 2.0, than audio files startswith "mdx-oalecd9\_mdx" will be played at speed 2.0 * 0.8 = 1.6.    
**"ignore\_duplicated\_field"**: true #if ignore duplicated field.
#### All shortcuts can be changed in Auto\_Advance.py   
e.g. action.setShortcut("g"), shortcut "g" can be changed to any other key which is not used by any other software. "Ctrl+," also can be changed to other keyboard shortcuts.   
You need to restart you Anki to take effect if you change anything on Auto\_Advance.py 

```
action = QAction("Toggle Default Action: Hard or Good", mw)
action.setShortcut("g")
action.triggered.connect(toggle_choice_hard_good)
afc.addAction(action)

action = QAction("Temporary Answer Action: Again", mw)
action.setShortcut(",")
action.triggered.connect(temp_answer_action_again)
afc.addAction(action)
```