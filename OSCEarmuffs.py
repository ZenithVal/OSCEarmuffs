from threading import Thread
import json
import os
import time

from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from Controllers.DataController import DefaultConfig, Settings, Earmuffs
from Controllers.PackageController import Package
from Controllers.ThreadController import Program

def createDefaultConfigFile(configPath): # Creates a default config
    try:
        with open(configPath, "w") as cf:
            json.dump(DefaultConfig, cf)

        print("Default config file created")
        time.sleep(3)

    except Exception as e:
        print(e)
        time.sleep(5)
        exit()

if __name__ == "__main__":

    #*************Setup*************#
    program = Program()
    program.setWindowTitle()
    program.cls()

    """
    Steps to work on:
    1 - setWindowTitle
    2 - Clear
    3 - Prepare config
    4 - create settings object
    5 - 
    ? - Add voicemeter setup
    """
    

    # Test if Config file exists. Create the default if it does not.
    configRelativePath = "./config.json"
    if not os.path.exists(configRelativePath):
        print("Config file was not found...", "\nCreating default config file...")
        createDefaultConfigFile(configRelativePath)
    else:
        print("Config file found\n")

    configData = json.load(open(configRelativePath)) # Config file should be prepared at this point.
    settings = Settings(configData) # Get settings from config file

    ############# Temporarily Commented to focus on main function #############
    # VoiceMeter setup
    if settings.vmrSettings.LowPassEnabled:
        import voicemeeter
        voicemeeter.launch("basic")
        with voicemeeter.remote("Basic") as vmr:
            settings.addVoiceMeterControls(
                vmr.inputs[2].gain,
                vmr.inputs[2].eqgain1,
                vmr.inputs[2].eqgain2,
                vmr.inputs[2].eqgain3)

    earmuffs = Earmuffs

    # Manage data coming in
    package = Package(earmuffs)
    package.listen()

    try:
        # Start server
        serverThread = Thread(target=package.runServer, args=(settings.generalSettings.IP, settings.generalSettings.ListeningPort))
        serverThread.start()
        time.sleep(.1)

        #initialize input
        if serverThread.is_alive():
            Thread(target=program.earmuffsRun, args=(earmuffs,settings)).start()
        else: 
            print("IT'S ALL FUCKING DYING AHHHHHHHH")
            raise Exception()
            
    except Exception as e:
        print(e)
        time.sleep(10)