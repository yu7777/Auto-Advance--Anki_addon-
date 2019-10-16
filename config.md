 Anything related time will be count in <b>senconds</b> in this config.  
<li><b>Time sequence.</b>
</li><li>show question.<br><b>
 Time of audio play (if no audio play, use default_waiting_time) + addition_time + addition_time_question.</b>
 </li><li>show answer.<br>
 <b>Time of audio play (if no audio play, use default_waiting_time) + addition_time + addition_time_answer.
 </b></li><li>action Hard or Good. Then next card.
</li><br>
<b>Windows version will ignore any speed setting.</b><br>
<li>"audio_speed": 2.2, <b>This is the default play speed, you can change it with shortcuts [ or ]</b>
</li><li> "mode": 1, <b> play all audios (Normal study) mode 0: play selected audio.(Usually used for Custom Study Session. e.g. quickly review all the cards you learned today)
</b></li><li>"mode_0_field": {"发音":[-1]}<br>
 <b>Mode 0 selected field "发音". -1 means play audio at default speed. NOTE: If you want to play it twice at speed 0.5 and 1.5. you can use mode_0_field = {"发音":[0.5,1.5]}</b>
 </li><li>"show_notif": true, #if show notification or not
 </li><li>"show_notif_timeout": 0.8, 
 </li><li>"wait_for_audio": true, 
 </li><li>"repeat_field": {"发音":[0.7,1.5,2.6]}, <br><strong>
 specify repeat field and audio speed each time.<br>
 e.g. {"voice":[0.5],"sentence":[1.5,2]} means:<br>
 any audio in voice field will be played once at audio speed 0.5, and any audio in sentence field will be played twice, one at speed 1.5 and the other at speed 2</strong>
 <br><br>
 </li><li>"audio_startswith": "mdx-oalecd9_mdx", 
 </li><li>"audio_startswith_speed_factor": 0.6, <br></b>
 change audio speed for identified audio files by "audio_startswith". <br>
 e.g. audio files from different sources may have different audio speed by default. My case is that the audio files from oalecd9_mdx is faster than other audio files, so if default audio speed is 2.0, than audio files startswith "mdx-oalecd9_mdx" will be played at speed 2.0 * 0.8 = 1.6.</b>
 </li><li>"ignore_duplicated_field": true #if ignore duplicated field
