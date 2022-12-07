from array import array
import time
import sys
import ctypes #Required for colored error messages.
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from threading import Lock, Thread

from Controllers.DataController import Earmuffs
from Controllers.ThreadController import Program


#Starts the OSC Server & handles incoming OSC data
class Package:

    def __init__(self, earmuffs):
        self.__dispatcher = Dispatcher()
        self.__statelock = Lock()

        self.AvatarParameter = AvatarParameter
        except Exception as e:
            print(e)
            time.sleep(5)


    def listenAvatarParameter(self):
            self.__dispatcher.map(f'/avatar/parameters/{Earmuffs.AvatarParameter}',self.__updateAvatarParameter, earmuffs) 

    def __updateAvatarParameter(self, addr, extraArgs, value):
        try:
            earmuffs: Earmuffs = extraArgs[0]
            self.__statelock.acquire()
            earmuffs.AvatarParameterValue = value
            self.__statelock.release()
        except Exception as e:
            print(e)
            time.sleep(5)

    #Server Start
    def runServer(self, IP, Port):
        try:
            osc_server.ThreadingOSCUDPServer((IP, Port), self.__dispatcher).serve_forever()
        except Exception as e:
            print('\x1b[1;31;41m' + '                                                                    ' + '\x1b[0m')
            print('\x1b[1;31;40m' + '   Warning: An application might already be running on this port!   ' + '\x1b[0m')
            print('\x1b[1;31;41m' + '                                                                    \n' + '\x1b[0m')
            print(e)
            # No delay here as error message is called from the main script.
