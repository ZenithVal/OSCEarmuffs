import ctypes #Required for colored error messages.
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

from Controllers.DataController import Earmuffs


#Starts the OSC Server & handles incoming OSC data
class Package:

    def __init__(self, earmuffs):
        self.__dispatcher = Dispatcher() # Recieves information from vrc client
        self.__AvatarParameter = earmuffs.AvatarParameter # Stores the Avatar Parameter name as a reference

        self.__earmuffs = earmuffs

    # Uses oscServer to "listen" for new data. (Blocking method)
    def listen(self):
        self.__dispatcher.map(f'/avatar/parameters/{self.__AvatarParameter}',self.__updateAvatarParameter)

    #NOTE: addr is an output of Dispatcher. It must be included even if not used. Otherwise,
    #   the address will be placed in the "value" parameter.
    def __updateAvatarParameter(self, addr, value):
        #Assign value
        self.__earmuffs.AvatarParameterValue = value

    # Server run (Blocking method): Reduces rate at which data is pushed by blocking
    # Reference => https://github.com/attwad/python-osc
    def runServer(self, IP, Port):
        try:
            osc_server.BlockingOSCUDPServer((IP, Port), self.__dispatcher).serve_forever()
        except Exception as e:
            print('\x1b[1;31;41m' + '                                                                    ' + '\x1b[0m')
            print('\x1b[1;31;40m' + '   Warning: An application might already be running on this port!   ' + '\x1b[0m')
            print('\x1b[1;31;41m' + '                                                                    \n' + '\x1b[0m')
            print(e)
            # No delay here as error message is called from the main script.