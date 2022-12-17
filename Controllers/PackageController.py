import ctypes #Required for colored error messages.
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

from Controllers.DataController import Earmuffs


#Starts the OSC Server & handles incoming OSC data
class Package:

    def __init__(self, earmuffs):
        self.__dispatcher = Dispatcher() # Recieves information from vrc client

        self.earmuffs = earmuffs
        self.__AvatarParameter = earmuffs

    def listen(self, earmuffs):
        self.__dispatcher.map(f'/avatar/parameters/{self.__AvatarParameter}',self.__updateAvatarParameter)

    def __updateAvatarParameter(self, 
                                #addr, #Address is not needed at thie time, we're not sending any data out.
                                value):
        self.earmuffs.AvatarParameterValue = value

    #Server run (Blocking)
    def runServer(self, IP, Port):
        try:
            osc_server.BlockingOSCUDPServer((IP, Port), self.__dispatcher).serve_forever()
        except Exception as e:
            print('\x1b[1;31;41m' + '                                                                    ' + '\x1b[0m')
            print('\x1b[1;31;40m' + '   Warning: An application might already be running on this port!   ' + '\x1b[0m')
            print('\x1b[1;31;41m' + '                                                                    \n' + '\x1b[0m')
            print(e)
            # No delay here as error message is called from the main script.