from pythonosc.udp_client import SimpleUDPClient
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from threading import Thread
import time
import os
import ctypes #Required for colored error messages.

from Controllers.DataController import Settings, Earmuffs

class Program:

    def earmuffsRun(self, earmuffs: Earmuffs, settings: Settings):
        
        self.cls()
        settings.printInfo()

        # Logging, seems to be screaming and breaking
        # if settings.generalSettings.Logging:
        #     earmuffs.printOutputs()
        # print("\nCurrent Status:\n")

        # Inverse deadzone Range for Volume (Living range?)
        convertedVol = self.clamp(((earmuffs.AvatarParameterValue - settings.generalSettings.VolumeCurveStart) / settings.generalSettings.VolumeCurveRange))

        # VRC Volume Calculations
        vrcVol = self.volCalculate(convertedVol,settings.vrcSettings.VRCVolRange,1,settings.vrcSettings.VRCMinVolume)


        # Media Volume Calculations
        if settings.mediaSettings.MediaControlEnabled:
            mediaVol = self.volCalculate(convertedVol,settings.mediaSettings.MediaVolRange,-1,settings.mediaSettings.MediaMaxVolume)

            mediaPause = False

            #Pausing Functionality, currently disabled.
            # if earmuffs.settings.MediaPauseEnabled:  
            #     if earmuffs.AvatarParamaterValue >= earmuffs.settings.MediaPauseThreshhold:
            #         mediaPause = True
            #     else:
            #         mediaPause = False
        
        else:
            mediaVol = 1.0
            mediaPause = False

        # Lowpass Calculations
        if settings.vmSettings.LowPassEnabled:
            vmGain = convertedVol * -8 * settings.vmSettings.LowPassStrength
            vmBass = convertedVol * 12 * settings.vmSettings.LowPassStrength
            vmHighs = convertedVol * -12 * settings.vmSettings.LowPassStrength
        else:
            vmGain=vmBass=vmHighs = 0.0

        self.earmuffsOutput (
                            vrcVol, mediaVol, mediaPause, 0, 
                            vmGain, vmBass, vmHighs, 
                            settings
                            )

    def volCalculate(convertedVol, range, multi,translate):
        return ((convertedVol*range)*multi)+translate

    def earmuffsOutput  (
                        self, vrcVol: float, mediaVol: float, mediaPause: bool, 
                        #vmGain: float, vmBass: float, vmHighs: float, 
                        settings: Settings
                        ):

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            #VRC Volume
            if session.Process and session.Process.name() == "VRChat.exe":
                volume.SetMasterVolume(vrcVol, None)
            
            #VRC Earmuff Controls
                #VRC has not exposed earmuff endpoints https://github.com/vrchat-community/osc/issues/149

            #Media Volume
            if  ( 
                settings.MediaControlEnabled 
                and session.Process 
                and session.Process.name() == settings.MediaApplication 
                ):
                    volume.SetMasterVolume(mediaVol, None)

            #Voicemeter LowPass Numbers
            if settings.LowPassEnabled:
                settings.Gain = vmGain 
                settings.EQgain1 = vmBass
                settings.EQgain2 = settings.EQgain3 = vmHighs

    def clamp (self, value):
        return max(0.0, min(value, 1.0))

    def cls(self): # Console Clear
        """Clears Console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setWindowTitle(self): # Set window title
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW("OSCEarmuffs")
