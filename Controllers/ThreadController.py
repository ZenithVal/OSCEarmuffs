from pythonosc.udp_client import SimpleUDPClient
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from threading import Lock, Thread
import time
import os
import ctypes #Required for colored error messages.

from Controllers.DataController import ConfigSettings, earmuffs

class Program:

    # Class variable to determine if the program is running on a thread (Prevents multiple threads)
    __running = False 

    def resetProgram(self):
        Program.__running = False 
    
    def updateProgram(self, runBool:bool, countValue:int):
        Program.__running = runBool

    def earmuffsRun(self, earmuffs: earmuffs, counter:int = 0):

        if counter == 0 and Program.__running or not earmuffs.Active:
            return
        
        if counter < 0: # Prevents int overflow possibility by resetting counter at continuation state
            counter = 1
        
        statelock = Lock()
        statelock.acquire()
        
        self.cls()
        earmuffs.settings.printInfo()
        if earmuffs.settings.Logging:
            earmuffs.printOutputs()
        print("\nCurrent Status:\n")

        #Volume Math

        #VRCHat Volume Outputs

        #Media Volume Outputs

        #LowPass Outputs

    def earmuffsOutput(self, vrcVol: float, mediaVol: float, mediaPause: bool, lowpassPerc: float, settings: ConfigSettings):

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            #VRC Volume
            if session.Process and session.Process.name() == "VRChat.exe":
                volume.SetMasterVolume(vrcVol, None)
            
            #Media Volume
            if  ( 
                earmuffs.settings.MediaControlEnabled 
                and session.Process 
                and session.Process.name() == earmuffs.settings.MediaApplication
                ):
                    volume.SetMasterVolume(mediaVol, None)

        #if earmuffs.settings.LowPassEnabled:
            #Control Voicemeter lowpass here, woah.
        
    def clamp (self, n):
        return max(-1.0, min(n, 1.0))

    def clampPos (self, n):
        return max(0.0, min(n, 0.99999))

    def clampNeg (self, n):
        return max(-0.99999, min(n, 0.0))

    def cls(self): # Console Clear
        """Clears Console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setWindowTitle(self): # Set window title
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW("OSCEarmuffs")
