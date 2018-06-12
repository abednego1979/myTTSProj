# -*- coding: utf-8 -*-

#Python 3.5.x

#V0.01

#py -3 -m pip install pyttsx3
#py -3 -m pip install pypiwin32

# https://pypi.org/project/pyttsx3/
# more voide packets can download from microsoft website


import pyttsx3          



__metaclass__ = type

class BaseTtsEngine():
    def setVoices(self, voice_name):
        print ("BaseTtsEngine: Set voice as %s" % voice_name)
        return
    def setSpeechRate(self, setValue):
        print ("BaseTtsEngine: Set Speech Rate as %d" % setValue) 
        return
    def setVolume(self, setValue):
        print ("BaseTtsEngine: Set Volume as %.02f" % setValue)
        return
    def say(self, text):
        print ("BaseTtsEngine: Reading:", text)
        return


class myTtsEngine_win_os_tts(BaseTtsEngine):        #windows system tts
    
    def __init__(self, debugFlag=False):
        self.engine = pyttsx3.init()
        self.dbgFlag=debugFlag
        return
    
    def setVoices(self, voice_name):
        voices = self.engine.getProperty('voices')
        if self.dbgFlag:
            for index,voice in enumerate(voices):
                print (index, voice.id)
        
        selVoice=None
        for voice in voices:
            if voice_name.lower() in voice.id.lower():
                selVoice=voice
                break
        if not selVoice:
            selVoice=voices[0]
        
        if self.dbgFlag:
            print ("Set voice as %s" % selVoice.id)
        self.engine.setProperty('voice', selVoice.id)
        
        return
    
    def setSpeechRate(self, setValue):
        temp=int(min(max(setValue, 50), 200))
        if self.dbgFlag:
            print ("Set Speech Rate as %d" % temp)        
        self.engine.setProperty('rate', temp)
        return
    
    def setVolume(self, setValue):
        temp=min(max(setValue, 0.0), 1.0)
        if self.dbgFlag:
            print ("Set Volume as %.02f" % temp)        
        self.engine.setProperty('volume', temp)
        return
    
    def say(self, text):
        if self.dbgFlag:
            print ("Reading:", text)
        self.engine.say(text)
        self.engine.runAndWait()
        return
    
class myTtsEngine_win_kedaxunfei_tts(BaseTtsEngine):        #windows 科大讯飞
    def __init__(self, debugFlag=False):
        self.engine = pyttsx3.init()
        self.dbgFlag=debugFlag
        return
    
    
#example

eng=myTtsEngine_win_os_tts(debugFlag=True)
eng.setVoices("zira")
eng.setSpeechRate(120)
eng.setVolume(1.0)
eng.say("Sally sells seashells by the seashore. The quick brown fox jumped over the lazy dog. 我是中国人，商贾云集，贾宝玉")

eng.setVoices("huihui")
eng.setSpeechRate(120)
eng.setVolume(1.0)
eng.say("Sally sells seashells by the seashore. The quick brown fox jumped over the lazy dog. 我是中国人，商贾云集，贾宝玉")


