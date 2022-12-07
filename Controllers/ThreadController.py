from pythonosc.udp_client import SimpleUDPClient
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from threading import Lock, Thread
import time
import os
import ctypes #Required for colored error messages.

from Controllers.DataController import ConfigSettings, Earmuffs

class Program:

    # Class variable to determine if the program is running on a thread (Prevents multiple threads)
    __running = False 

    def resetProgram(self):
        Program.__running = False 
    
    def updateProgram(self, runBool:bool, countValue:int):
        Program.__running = runBool

    def earmuffsRun(self, earmuffs: Earmuffs, counter:int = 0):

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

        AvatarParameterValue = # aaa how we get the value?

        #VRCHat Volume Controls
        vrcVol = earmuffs.AvatarParameterValue -1

        #Media Volume Controls
        if earmuffs.settings.MediaControlEnabled:
            mediaVol = earmuffs.AvatarParameterValue

            if earmuffs.settings.MediaPauseEnabled:
                if earmuffs.AvatarParamaterValue >= earmuffs.settings.MediaPauseThreshhold:
                    mediaPause = True
                else:
                    mediaPause = False
        else:
            mediaVol = 1.0
            mediaPause = False

        # #LowPass Outputs
        # if earmuffs.settings.LowPassEnabled:
        #     vmGain = earmuffs.AvatarParameterValue * -8 * earmuffs.settings.LowPassStrength
        #     vmBass = earmuffs.AvatarParameterValue * 12 * earmuffs.settings.LowPassStrength
        #     vmHighs = earmuffs.AvatarParameterValue * -12 * earmuffs.settings.LowPassStrength
        # else:
        #     vmGain=vmBass=vmHighs = 0.0

        self.earmuffsOutput (
                            vrcVol, mediaVol, mediaPause, 0, 
                            #vmGain, vmBass, vmHighs, 
                            earmuffs.settings
                            )



    def earmuffsOutput  (
                        self, vrcVol: float, mediaVol: float, mediaPause: bool, 
                        #vmGain: float, vmBass: float, vmHighs: float, 
                        settings: ConfigSettings
                        ):

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            #VRC Volume
            if session.Process and session.Process.name() == "VRChat.exe":
                volume.SetMasterVolume(vrcVol, None)
            
            #VRC Earmuff Controls
                #Blank functionaly for now https://github.com/vrchat-community/osc/issues/149

            #Media Volume
            if  ( 
                settings.MediaControlEnabled 
                and session.Process 
                and session.Process.name() == settings.MediaApplication 
                ):
                    volume.SetMasterVolume(mediaVol, None)

            # #Voicemeter LowPass Numbers
            # if settings.LowPassEnabled:
            #     settings.Gain = vmGain 
            #     settings.EQgain1 = vmBass
            #     settings.EQgain2 = settings.EQgain3 = vmHighs


    def clamp (self, n):
        return max(-1.0, min(n, 1.0))

    def clampPos (self, n):
        return max(0.0, min(n, 1.0))

    def clampNeg (self, n):
        return max(-0.99999, min(n, 0.0))

    def cls(self): # Console Clear
        """Clears Console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setWindowTitle(self): # Set window title
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW("OSCEarmuffs")
