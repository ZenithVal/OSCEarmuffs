"""
Small example OSC client
"""
import random
import time

from pythonosc import udp_client

LeashNameString = "Leash_North"
PORT = 9001
IP = "127.0.0.1"

def sendData():
  
  AvatarParameter = "Headphones_Stretch"
  ParamValue = random.random()

  print(f"Sending {AvatarParameter}: {ParamValue}\n\t: ")
  client.send_message(f"/avatar/parameters/{AvatarParameter}", ParamValue)

  time.sleep(1)

if __name__ == "__main__":

  client = udp_client.SimpleUDPClient(IP, PORT)

  for x in range(10000):
    sendData()
