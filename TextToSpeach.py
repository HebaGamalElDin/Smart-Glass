# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 06:47:54 2020

@author: Heba Gamal EL-Din
"""

#from numpy import unique
import time
import pyttsx3


class TextToSpeach:
    def __init__(self):

        """ Initialize TTS Engine """
        self.Voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', self.Voice)
        self.engine.say("Welcome to the Navigation assistante")
        self.engine.runAndWait()
        
    def Speaker_(self, Texts): 
        self.engine.say(Texts)
        self.engine.runAndWait()
        # if len(Texts) > 0:            
        #     print(' and '.join(Texts))
        #     #for text in Texts:
        #     if self.engine.isBusy():       
        #         time.sleep(3.0)
        #         self.engine.say(' and '.join(Texts))
        #     else:
        #         self.engine.say(' and '.join(Texts))
        #     self.engine.runAndWait()
        #     self.engine.stop()
        # else:
        #    self.engine.stop()    

obj = TextToSpeach()
obj.Speaker_(u"الحمد لله رب العالمين")