# -*- coding: utf-8 -*-

#Python 3.5.x

#V0.01

#py -3 -m pip install pyttsx3
#py -3 -m pip install pypiwin32

# https://pypi.org/project/pyttsx3/
# more voide packets can download from microsoft website


import myTTS


#example

Text="Sally sells seashells by the seashore. 1, 2, 3. One, Two, Three. The quick brown fox jumped over the lazy dog. 我是中国人，商贾云集，贾宝玉. 1, 2, 3, 4, 5."
Text1="Sally sells seashells by the seashore."
Text2=Text1.replace(" ", ". ")

#eng=myTTS.myTtsEngine_win_os_tts(debugFlag=True)
#eng.setVoices("zira")
#eng.setSpeechRate(60)
#eng.setVolume(1.0)
##eng.say(Text)
#eng.say(Text1)
#eng.say(Text2)

#eng.setVoices("huihui")
#eng.setSpeechRate(60)
#eng.setVolume(1.0)
#eng.say(Text)


eng=myTTS.myTtsEngine_win_kedaxunfei_tts(debugFlag=True)
eng.setVoices("xiaoyan")
eng.setSpeechRate(40)
eng.setVolume(1.0)
eng.say(Text)

eng.setVoices("yanping")
eng.setSpeechRate(40)
eng.setVolume(1.0)
eng.say(Text)


