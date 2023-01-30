from pythonosc.udp_client import SimpleUDPClient
#from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from threading import Thread, Lock
import time
import os #Windows dependancy
import ctypes #Required for colored error messages.

from Controllers.DataController import Settings, Earmuffs

class Program:

    __statelock = Lock()

    # __Active = False

    # def __setActive(self):
    #     Program.__Active = True

    # def __setInactive(self):
    #     Program.__Active = False
    
    # def isRunning(self):
    #     return self.__Active

    def volCalculate(self, convertedVol, range, multi,translate):
        return ((convertedVol*range)*multi)+translate

    def programThread(self, earmuffs: Earmuffs, settings: Settings, active = False):
        timeDelay = None
        if active:
            timeDelay = settings.generalSettings.ActiveUpdateInterval
        else:
            timeDelay = settings.generalSettings.InactiveUpdateInterval

        time.sleep(timeDelay)
        Thread(target=self.earmuffsUpdate, args=(earmuffs,settings)).start()

    def earmuffsUpdate(self, earmuffs: Earmuffs, settings: Settings):
        
        '''Display'''
        self.cls()
        settings.printInfo()

        '''State Checks'''
        ### TEST VALUE ###
        earmuffs.AvatarParameterValue = 0.5

        endThread = False
        self.__statelock.acquire()
        if earmuffs.AvatarParameterValue is None:
            endThread = True
            self.programThread(earmuffs, settings, False)
        self.__statelock.release()

        if endThread: return

        self.__statelock.acquire()
        if earmuffs.VRChatVolume == earmuffs.VRChatTargetVolume:
            endThread = True
            self.programThread(earmuffs, settings, False)
        self.__statelock.release()

        if endThread: return

        '''Calculations'''

        self.__statelock.acquire()
        #avatarParamValue = earmuffs.AvatarParameterValue
        # Inverse deadzone Range for Volume (Living range?)
        convertedVol = self.clamp(((earmuffs.AvatarParameterValue - settings.generalSettings.VolumeCurveStart) / settings.generalSettings.VolumeCurveRange))
        self.__statelock.release()
        
        # convertedVol = self.clamp(((avatarParamValue - settings.generalSettings.VolumeCurveStart) / settings.generalSettings.VolumeCurveRange))

        # VRC Volume Calculations
        vrcVol = self.volCalculate(convertedVol, settings.vrcSettings.VRCVolRange, 1, settings.vrcSettings.VRCMinVolume)

        # Media Volume Calculations
        if settings.mediaSettings.MediaControlEnabled:
            mediaVol = self.volCalculate(convertedVol, settings.mediaSettings.MediaVolRange,-1, settings.mediaSettings.MediaMaxVolume)
        else:
            mediaVol = 1.0

        self.__statelock.acquire()
        earmuffs.MediaTargetVolume = mediaVol
        earmuffs.VRChatTargetVolume = vrcVol
        self.__statelock.release()

        self.programThread(earmuffs, settings, True)

        # Lowpass Calculations
        # if settings.vmSettings.LowPassEnabled:
        #     vmGain = convertedVol * -8 * settings.vmSettings.LowPassStrength
        #     vmBass = convertedVol * 12 * settings.vmSettings.LowPassStrength
        #     vmHighs = convertedVol * -12 * settings.vmSettings.LowPassStrength
        # else:
        #     vmGain=vmBass=vmHighs = 0.0

    # def earmuffsOutput(earmuffs: Earmuffs, settings: Settings):

    #     '''State Checks'''
    #     endThread = False
    #     self.__statelock.acquire()
    #     if earmuffs.AvatarParameterValue is None:
    #         endThread = True
    #         self.programThread(earmuffs, settings, False)
    #     self.__statelock.release()

    #     if endThread: return

    #     self.__statelock.acquire()
    #     if earmuffs.VRChatVolume == earmuffs.VRChatTargetVolume:
    #         endThread = True
    #         self.programThread(earmuffs, settings, False)
    #     self.__statelock.release()

    #     if endThread: return

    #     sessions = AudioUtilities.GetAllSessions()
    #     for session in sessions:
    #         volume = session._ctl.QueryInterface(ISimpleAudioVolume)
    #         #VRC Volume
    #         if session.Process and session.Process.name() == "VRChat.exe":
    #             volume.SetMasterVolume(vrcVol, None)
    #         else:
    #             print("VRC application not found")
            
    #         #VRC Earmuff Controls
    #             #VRC has not exposed earmuff endpoints https://github.com/vrchat-community/osc/issues/149

    #         #Media Volume
    #         if  ( 
    #             settings.MediaControlEnabled 
    #             and (session.Process and session.Process.name() == settings.MediaApplication)
    #             ):
    #                 volume.SetMasterVolume(mediaVol, None)

    #         #Voicemeter LowPass Numbers
    #         # if settings.LowPassEnabled:
    #         #     settings.Gain = vmGain 
    #         #     settings.EQgain1 = vmBass
    #         #     settings.EQgain2 = settings.EQgain3 = vmHighs

    def clamp (self, value): #Basic 0.0 - 1.0 clamp
        return max(0.0, min(value, 1.0))

    def cls(self): # Console Clear
        """Clears Console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def setWindowTitle(self): # Set window title
        if os.name == 'nt':
            ctypes.windll.kernel32.SetConsoleTitleW("OSCEarmuffs")
