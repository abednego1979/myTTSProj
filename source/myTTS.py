# -*- coding: utf-8 -*-

#Python 3.5.x

#V0.01

#py -3 -m pip install pyttsx3
#py -3 -m pip install pypiwin32

# https://pypi.org/project/pyttsx3/
# more voide packets can download from microsoft website


import pyttsx3
from pydub import AudioSegment

import os
import sys
from ctypes import *
import time
import struct
import pyaudio
import wave


__metaclass__ = type

class BaseTtsEngine():
    def setVoices(self, voice_name):
        print ("BaseTtsEngine: Set voice as %s" % voice_name)
        return
    def setSpeechRate(self, setValue):      #setValue between 0-100
        print ("BaseTtsEngine: Set Speech Rate as %d" % setValue) 
        return
    def setVolume(self, setValue):          #setValue between 0.0-1.0
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
        temp=int(min(max(setValue*2, 50), 200))
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
        self.dll = windll.LoadLibrary("msc_x64.dll")
        self.login_params = b"appid = 5b1ffcbf, work_dir = ."
        self.wav_header = b'RIFF6n\x06\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x80>\x00\x00\x00}\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00'  
        
        self.session_begin_params = ["engine_type = local", \
                                     "voice_name = xiaoyan", \
                                     "text_encoding = UTF8", \
                                     "tts_res_path = fo|res\\tts\\xiaoyan.jet;fo|res\\tts\\common.jet", \
                                     "sample_rate = 16000", \
                                     "speed = 80", \
                                     "volume = 70", \
                                     "pitch = 50", \
                                     "rdn = 0", \
                                     ]
        
        self.MSP_SUCCESS = 0
        self.MSP_TTS_FLAG_STILL_HAVE_DATA = 1
        self.MSP_TTS_FLAG_DATA_END = 2
        self.MSP_TTS_FLAG_CMD_CANCELED = 4
        
        self.filename = "_tts_sample.wav"
        self.fileprefix = ""
        
        self.dbgFlag=debugFlag
        
        self.logState=False
        
        return
    
    def login(self):
        ret = self.dll.MSPLogin(None, None, self.login_params)
        print(('MSPLogin =>'), ret)
        if ret==self.MSP_SUCCESS:
            self.logState=True
    
    def logout(self):
        ret = self.dll.MSPLogout()
        print(('MSPLogout =>'), ret)
        if ret==self.MSP_SUCCESS:
            self.logState=False
    
    def setVoices(self, voice_name):
        #打印所有可能的voice
        
        for i in range(len(self.session_begin_params)):
            if self.session_begin_params[i].startswith("voice_name"):
                self.session_begin_params[i]="voice_name = %s" % voice_name
        self.fileprefix=voice_name
        return
    
    def setSpeechRate(self, setValue):
        temp=int(min(max(setValue, 0), 100))
        if self.dbgFlag:
            print ("Set Speech Rate as %d" % temp)           
        for i in range(len(self.session_begin_params)):
            if self.session_begin_params[i].startswith("speed"):
                self.session_begin_params[i]="speed = %d" % temp
        return
    
    def setVolume(self, setValue):  #para: http://mscdoc.xfyun.cn/windows/api/iFlytekMSCReferenceManual/qtts_8h.html
        temp=min(max(setValue, 0.0), 1.0)
        if self.dbgFlag:
            print ("Set Volume as %.02f" % temp)        
        for i in range(len(self.session_begin_params)):
            if self.session_begin_params[i].startswith("volume"):
                self.session_begin_params[i]="spevolumeed = %d" % int(temp*100)        
        return
    
    def say(self, text):
        if self.dbgFlag:
            print ("Reading:", text)
            
        if not self.logState:
            self.login()
        else:
            self.logout()
            self.login()
            
        self.tts(text.encode('U8'), self.fileprefix+self.filename, ", ".join(self.session_begin_params).encode('utf-8'))
        
        if self.logState:
            self.logout()
        return
    
    def tts(self, text, filename, session_begin_params):
        ret, audio_len, synth_status, getret, wav_datasize = c_int(), c_int(), c_int(), c_int(), c_int()
        sessionID = self.dll.QTTSSessionBegin(session_begin_params, byref(ret))
        if self.dbgFlag:
            print ('QTTSSessionBegin => sessionID:', sessionID, 'ret:', ret.value)
        ret = self.dll.QTTSTextPut(sessionID, text, len(text), None)
        if self.dbgFlag:
            print ('QTTSTextPut => ret:', ret)
            #11212:试用资源过期
    
        wavFile = open(filename, 'wb')
        wavFile.write(self.wav_header)
        
        if self.dbgFlag:
            print ('QTTSAudioGet => ',)
        while True:
            self.dll.QTTSAudioGet.restype = POINTER(c_ushort * (1024 * 1024))
            data = self.dll.QTTSAudioGet(sessionID, byref(audio_len), byref(synth_status), byref(getret))
            if self.dbgFlag:
                print ('QTTSAudioGet => audio_len:', audio_len.value, 'synth_status:', synth_status.value, 'getret:', getret.value)
                
            if audio_len.value>0:
                print('datasize:%d\r' % wav_datasize.value, end='\r')
                pass
            if getret.value != self.MSP_SUCCESS:
                if self.dbgFlag:
                    print ('!MSP_SUCCESS => getret:', getret.value)     #10132:MSP_ERROR_INVALID_OPERATION
                break
            if data:
                wavFile.write(string_at(data, audio_len))
                wav_datasize.value += audio_len.value
            if synth_status.value == self.MSP_TTS_FLAG_DATA_END:
                break
            time.sleep(0.01)
        # fix wav header
        WAVE_HEADER_SIZE = 44
        if wav_datasize.value>0:
            wav_size8 = c_int()
            wav_size8.value = WAVE_HEADER_SIZE + wav_datasize.value - 8
            wavFile.seek(4)
            wavFile.write(wav_size8)
            wavFile.seek(40)
            wavFile.write(wav_datasize)
        wavFile.close()
        ret = self.dll.QTTSSessionEnd(sessionID, "Normal")
        if self.dbgFlag:
            print ('QTTSSessionEnd => ret:', ret)
        
        #trans wav to mp3
        myAudioEngine_wav2mp3().trans(filename, filename.replace(".wav", ".mp3"))
        
        #play the wav file
        chunk = 1024
        f = wave.open(filename,"rb")
        p = pyaudio.PyAudio()
        stream = p.open(format = p.get_format_from_width(f.getsampwidth()), channels = f.getnchannels(), rate = f.getframerate(), output = True)
        data = f.readframes(chunk)
        
        while data:  
            stream.write(data)
            data = f.readframes(chunk)
        stream.stop_stream()  
        stream.close()
        p.terminate()
        f.close()
        #delete the wav file
        try:
            os.remove(filename)
        except:
            pass
        
class myAudioEngine_wav2mp3():  #wav转mp3的引擎
    def __init__(self, debugFlag=False):
        return
    
    def trans(self, inFile, outFile):
        #voice=AudioSegment.from_wav(inFile)
        #voice.export(outFile, format="mp3")
        return