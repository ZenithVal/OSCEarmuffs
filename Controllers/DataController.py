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

        "MuteCurveStart": 0.1,
        "MuteCurveStop": 0.9,
        
        "VRCMinVolume": 0.5,
        "VRCMaxVolume": 1.0,

        "LowPassEnabled": False, #Requires user experience with multiple audio lines
        "LowPassStrength": 1.0,

        "MediaControlEnabled": True,
        "MediaApplication": "Spotify.exe", #User can input null if they do not want it to edit spotify volume
        "MediaMinVolume": 0.0,
        "MediaMaxVolume": 1.0, #Only adjust this value if you set your media application to 100% volume (Not reccomended)
        
        "MediaPauseEnbabled": False, #Unsure of a way to tell if the media is already paused?
        "MediaPauseThreshhold": 1.0, #inverted~ 1.0 is actually 0% volume. 

        "AvatarParameter": "Headphones_Stretch" #A float on a radial menu would also work for personal control
}

class ConfigSettings:

    def __init__(self, configData):
            self.setSettings(configData) #Set config values
        
    def setSettings(self, configJson):
        try:
            self.IP = configJson["IP"]
            self.ListeningPort = configJson["ListeningPort"]
            self.SendingPort = configJson["SendingPort"]
            self.Logging = configJson["Logging"]

            self.InactiveUpdateInterval = configJson["InactiveUpdateInterval"]
            self.ActiveUpdateInterval = configJson["ActiveUpdateInterval"]
            self.RateOfChange = configJson["RateOfChange"]

            self.MuteCurveStart = configJson["MuteCurveStart"]
            self.MuteCurveStop = configJson["MuteCurveStop"]

            self.VRCMinVolume = configJson["VRCMinVolume"]
            self.VRCMaxVolume = configJson["VRCMaxVolume"]
            self.LowPassEnabled = configJson["LowPassEnabled"]
            self.LowPassStrength = configJson["LowPassStrength"]

            self.MediaControlEnabled = configJson["MediaControlEnabled"]
            self.MediaApplication = configJson["MediaApplication"]
            self.MediaMinVolume = configJson["MediaMinVolume"]
            self.MediaMaxVolume = configJson["MediaMaxVolume"]
            self.MediaPauseEnabled = configJson["MediaPauseEnbabled"]
            self.MediaPauseThreshhold = configJson["MediaPauseThreshhold"]
            self.AvatarParameter = configJson["AvatarParameter"]
        except Exception as e: 
            print('\x1b[1;31;40m' + 'Malformed config file. Loading default values.' + '\x1b[0m')
            print(e,"was the exception\n")
            self.IP = DefaultConfig["IP"]
            self.ListeningPort = DefaultConfig["ListeningPort"]
            self.SendingPort = DefaultConfig["SendingPort"]
            self.Logging = DefaultConfig["Logging"]

            self.InactiveUpdateInterval = DefaultConfig["InactiveUpdateInterval"]
            self.ActiveUpdateInterval = DefaultConfig["ActiveUpdateInterval"]
            self.RateOfChange = DefaultConfig["RateOfChange"]

            self.MuteCurveStart = DefaultConfig["MuteCurveStart"]
            self.MuteCurveStop = DefaultConfig["MuteCurveStop"]

            self.VRCMinVolume = DefaultConfig["VRCMinVolume"]
            self.VRCMaxVolume = DefaultConfig["VRCMaxVolume"]
            self.LowPassEnabled = DefaultConfig["LowPassEnabled"]
            self.LowPassStrength = DefaultConfig["LowPassStrength"]

            self.MediaControlEnabled = DefaultConfig["MediaControlEnabled"]
            self.MediaApplication = DefaultConfig["MediaApplication"]
            self.MediaMinVolume = DefaultConfig["MediaMinVolume"]
            self.MediaMaxVolume = DefaultConfig["MediaMaxVolume"]
            self.MediaPauseEnabled = DefaultConfig["MediaPauseEnbabled"]
            self.MediaPauseThreshhold = DefaultConfig["MediaPauseThreshhold"]
            self.AvatarParameter = DefaultConfig["AvatarParameter"]
            time.sleep(3)

        #Voicemeter controls
    def addVoiceMeterControls(self,Gain,EQgain1,EQgain2,EQgain3):
        self.Gain = Gain
        self.EQgain1 = EQgain1
        self.EQgain2 = EQgain2
        self.EQgain3 = EQgain3     

    def printInfo(self):        
        print('\x1b[1;32;40m' + 'OSCEarmuffs is Running!' + '\x1b[0m')

        if self.IP == "127.0.0.1":
            print("IP: Localhost")
        else:  
            print("IP: Not Localhost? Wack.")

        print(f"Listening on port {self.ListeningPort}\n Sending on port {self.SendingPort}")

        print("Update Intervals of {:.0f}".format(self.ActiveUpdateInterval*1000),"& {:.0f}".format(self.InactiveUpdateInterval*1000),"ms")
        print("Maximum of {:.0f}".format(self.RateOfChange*100)+"% volume change each update")

        print("Mute Curve Starts at {:.0f}".format(self.MuteCurveStart*100)+"%")
        print("Mute Curve Stops at {:.0f}".format(self.MuteCurveStop*100)+"%")

        print("VRC min Volume: {:.0f}".format(self.VRCMinVolume*100)+"%")
        print("VRC max Volume: {:.0f}".format(self.VRCMaxVolume*100)+"%")

        if self.LowPassEnabled:
            print("LowPass is enabled with a maximum of {:.0f}".format(self.LowPassStrength*100)+"%")

        if self.MediaControlEnabled:
            print(f"Media Control is enabled: \n\t Looking for {self.MediaApplication}\n\tMin volume of {self.MediaMinVolume*100}%\n\tMax volume of {self.MediaMaxVolume*100}%")
            if self.MediaPauseEnabled:
                print(f"Media will pause when volume is <={self.MediaPauseThreshhold*100}% volume")

class Earmuffs:

    def __init__(self, settings: ConfigSettings):

        self.settings = settings
        self.AvatarParameterValue: float = None,
        self.VRChatVolume: float = 0


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