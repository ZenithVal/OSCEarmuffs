import sys
import time
import ctypes #Required for colored error messages.

DefaultConfig = {
        "IP": "127.0.0.1",
        "ListeningPort": 9001,
        "SendingPort": 9000,
        "Logging": True,

        "InactiveUpdateInterval": 0.5,
        "ActiveUpdateInterval": 0.1,
        "RateOfChange": 0.1, #Maximum volume % change step per update invterval.

        "VolumeCurveStart": 0.1,
        "VolumeCurveStop": 0.9,
        
        "VRCMinVolume": 0.5,
        "VRCMaxVolume": 1.0,

        "LowPassEnabled": False, #Requires user experience with multiple audio lines
        "LowPassStrength": 1.0,

        "MediaControlEnabled": True,
        "MediaApplication": "", #User can input null if they do not want it to edit spotify volume
        "MediaMinVolume": 0.0,
        "MediaMaxVolume": 1.0, #Only adjust this value if you set your media application to 100% volume (Not reccomended)
        
        "MediaPauseEnbabled": False, #Unsure of a way to tell if the media is already paused?
        "MediaPauseThreshhold": 1.0, #inverted~ 1.0 is actually 0% volume. 

        "AvatarParameter": "Headphones_Stretch" #A float on a radial menu would also work for personal control
}



class Settings:
    def __init__(self, configData):
        try:
            self.createSettings(configData)
        except Exception as e:
            print('\x1b[1;31;40m' + 'Malformed config file. Loading default values.' + '\x1b[0m')
            print(e,"was the exception\n")
            self.createSettings()


    def createSettings(self, configJson = None):
        if not configJson:
            self.generalSettings = self.GeneralSettings(configJson)
            self.mediaSettings = self.MediaSettings(configJson)
            self.vrcSettings= self.VRCSettings(configJson)
        else:
            self.generalSettings = self.GeneralSettings()
            self.mediaSettings = self.MediaSettings()
            self.vrcSettings= self.VRCSettings()

    # #Voicemeter controls
    # def addVoiceMeterControls(self,Gain,EQgain1,EQgain2,EQgain3):
    #     self.Gain = Gain
    #     self.EQgain1 = EQgain1
    #     self.EQgain2 = EQgain2
    #     self.EQgain3 = EQgain3  

    def printInfo(self):
        print('\x1b[1;32;40m' + 'OSCEarmuffs is Running!' + '\x1b[0m')

        if self.IP == "127.0.0.1":
            print("IP: Localhost")
        else:  
            print("IP: Not Localhost? Wack.")

        print(f"Listening on port {self.generalSettings.ListeningPort}\n Sending on port {self.generalSettings.SendingPort}")

        print("Update Intervals of {:.0f}".format(self.generalSettings.ActiveUpdateInterval*1000),"& {:.0f}".format(self.generalSettings.InactiveUpdateInterval*1000),"ms")
        print("Maximum of {:.0f}".format(self.generalSettings.RateOfChange*100)+"% volume change each update")

        print("Mute Curve Starts at {:.0f}".format(self.generalSettings.VolumeCurveStart*100)+"%")
        print("Mute Curve Stops at {:.0f}".format(self.generalSettings.VolumeCurveStop*100)+"%")

        print("VRC min Volume: {:.0f}".format(self.vrcSettings.VRCMinVolume*100)+"%")
        print("VRC max Volume: {:.0f}".format(self.vrcSettings.VRCMaxVolume*100)+"%")

        # if self.LowPassEnabled:
        #     print("LowPass is enabled with a maximum of {:.0f}".format(self.LowPassStrength*100)+"%")

        if self.mediaSettings.MediaControlEnabled:
            print(f"Media Control is enabled: \n\t Looking for {self.mediaSettings.MediaApplication}\n\tMin volume of {self.mediaSettings.MediaMinVolume*100}%\n\tMax volume of {self.mediaSettings.MediaMaxVolume*100}%")
            # if self.MediaPauseEnabled:
            #     print(f"Media will pause when volume is <={self.MediaPauseThreshhold*100}% volume")

class GeneralSettings:
    def __init__(self, configJson = None):
        if configJson is not None:
            self.IP = configJson["IP"]
            self.ListeningPort = configJson["ListeningPort"]
            self.SendingPort = configJson["SendingPort"]
            self.Logging = configJson["Logging"]

            self.InactiveUpdateInterval = configJson["InactiveUpdateInterval"]
            self.ActiveUpdateInterval = configJson["ActiveUpdateInterval"]
            self.RateOfChange = configJson["RateOfChange"]

            self.VolumeCurveStart = configJson["VolumeCurveStart"]
            self.VolumeCurveStop = configJson["VolumeCurveStop"]
            self.VolumeCurveRange = self.VolumeCurveStop - self.VolumeCurveStart

            self.AvatarParameter = configJson["AvatarParameter"]
        else:
            self.IP = DefaultConfig["IP"]
            self.ListeningPort = DefaultConfig["ListeningPort"]
            self.SendingPort = DefaultConfig["SendingPort"]
            self.Logging = DefaultConfig["Logging"]

            self.InactiveUpdateInterval = DefaultConfig["InactiveUpdateInterval"]
            self.ActiveUpdateInterval = DefaultConfig["ActiveUpdateInterval"]
            self.RateOfChange = DefaultConfig["RateOfChange"]

            self.VolumeCurveStart = DefaultConfig["VolumeCurveStart"]
            self.VolumeCurveStop = DefaultConfig["VolumeCurveStop"]
            self.VolumeCurveRange = self.VolumeCurveStop - self.VolumeCurveStart

            self.AvatarParameter = DefaultConfig["AvatarParameter"]

class MediaSettings:
    def __init__(self, configJson = None):
        if configJson is not None:
            self.MediaControlEnabled = configJson["MediaControlEnabled"]
            self.MediaApplication = configJson["MediaApplication"]

            self.MediaMinVolume = configJson["MediaMinVolume"]
            self.MediaMaxVolume = configJson["MediaMaxVolume"]
            self.MediaVolRange = self.MediaMaxVolume - self.MediaMinVolume
                
            #Pausing doesnt fucking work lmao
            # self.MediaPauseEnabled = configJson["MediaPauseEnbabled"]
            # self.MediaPauseThreshhold = configJson["MediaPauseThreshhold"]
        else:
            self.MediaControlEnabled = DefaultConfig["MediaControlEnabled"]
            self.MediaApplication = DefaultConfig["MediaApplication"]

            self.MediaMinVolume = DefaultConfig["MediaMinVolume"]
            self.MediaMaxVolume = DefaultConfig["MediaMaxVolume"]
            self.MediaVolRange = self.MediaMaxVolume - self.MediaMinVolume

class VRCSettings:
    def __init__(self, configJson = None):
        if configJson is not None:
            self.VRCMinVolume = configJson["VRCMinVolume"]
            self.VRCMaxVolume = configJson["VRCMaxVolume"]
            self.VRCVolRange = self.VRCMaxVolume - self.VRCMinVolume
        else:
            self.VRCMinVolume = DefaultConfig["VRCMinVolume"]
            self.VRCMaxVolume = DefaultConfig["VRCMaxVolume"]
            self.VRCVolRange = self.VRCMaxVolume - self.VRCMinVolume


# class VMSettings:
#     def __init__(self, configJson = None):
#         if configJson is not None:
#             self.LowPassEnabled = configJson["LowPassEnabled"]
#             self.LowPassStrength = configJson["LowPassStrength"]

class Earmuffs:

    def __init__(self):
        self.AvatarParameterValue: float = None,

        self.VRChatVolume: float = None
        self.VRChatTargetVolume: float = None

        self.MediaVolume: float = None
        self.MediaTargetVolume: float = None


        # if self.LowPassEnabled:
        #     self.LowPassEffect: float = 0

        if self.MediaEnabled:
            self.MediaVolume: float = 0
            
            # if self.MediaPauseEnabled:
            #     self.MediaPause: bool = False

    def printOutputs(self):

        print(f"VRChat.exe: {self.VRChatVolume}%")
        if self.LowPassEnabled:
            print(f"Lowpass: {self.LowPassEffect}%")
        if self.MediaEnabled:
            print(f"{self.MediaApplication}: {self.MediaVolume}%")
            if self.MediaPauseEnabled:
                print(f"Media Paused: {self.MediaPause}%")