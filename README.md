# OSCEarmuffs

OSC Earmuffs is a companion tool for VRC's already built in earmuffs which adds functionality and windows media integration.<br>
You can bind an avatar parameter to VRC's Volume & a media application of choice. Voicemeter integration to add a lowpass filter over VRC is optional.

<br>

The tool is not in a functional state yet.
## ~~Options for running OSCEarmuffs~~
*~~OSCearmuffs relies on windows functions, so I don't believe it's compatible with linux~~*

1. **~~Via an executable~~**
   - ~~Download latest zip [from releases](https://github.com/ZenithVal/OSCEarmuffs/releases)~~
   - ~~Extract wherever.~~
   - ~~Edit Config.json~~
   - ~~Run Executable~~
2. **~~From the source~~**
   - ~~Clone the github~~
   - ~~Run `pip install -r requirements.txt` in the directory to install libraries~~
   - ~~Run the python script##Avatar Setup~~

<br>

## Setup - 1 Avatar 
*Requires VRC3 Avatar SDK.*

There's two reccomended ways to control this app with VRC OSC; <br> with a float in the radial menu or with the stretch of a physbone.

#### Option A - Radial Menu Slider
- Add a radial menu control to your avatar with as parameter rotation
- Assign "AvatarParameter" in config.json to your parameter

#### Option B - Physbone stretch
- Add a physbone
- Set "Max Stretch" to at least 0.2
- Set Parameter to whatever you'd like
- Assign "AvatarParameter" in config.json to YourParameterName_Stretch
- EG If your parameter is "Headphones" you'd write Headphones_Stretch

<br>

## Setup - 2 Media Application (Optional)
This interfaces with any application running audio on windows~ just find the executable name. <br>
*EG: Spotify.exe or Chrome.exe*

- set MediaControlEnabled in config.json to "true"
- Find the executable name of whatever application is playing music. 
- Fill in your application as MediaApplication in config.json

- MediaPauseEnbabled is set to false by default due to potential syncing issues
- If set to true, the tool will attempt to pause your music when the parameter is above MediaPauseThreshhold.

<br>

## Setup - 3 Voicemeter integration for lowpass (Optional)
This can be confusing, I would not reccomend it unless you have messed with virtual audio cables before. <br>

- Install voicemeter basic https://vb-audio.com/Voicemeeter/
- Windows Settings > Sound > Advanced sound options > App volume and device preferences
- Assign VRC to output to voicemeter input
- Assign voicemeter's A1 Hardware out to MME: (your VR audio)

<br>

## Setup - 4 I think I forgot something


For setup questions/support feel free to shoot me a DM or ask in #OSC-Talkin in [my Discord](https://discord.gg/7VAm3twDyy)

---

# Config

| Value                  | Info                                                           | default   |
|:---------------------- | -------------------------------------------------------------- |:---------:|
| IP                     | Address to send OSC data to                                    | 127.0.0.1 |
| ListeningPort          | Port to listen for OSC data on                                 | 9001      |
| Sending port           | Port to send OSC data to                                       | 9000      |
| Logging                | Messages in the console.                                       | true      |
| InactiveUpdateInterval | App delay when idle                                            | 0.5       |
| ActiveUpdateInterval   | App delay when active                                          | 0.05      |
| RateOfChange           | Maximum volume percent change per active update inverval       | 0.1       |
| VolumeCurveStart       | Value at which audio change begins                             | 0.05      |
| VolumeCurveStop        | Value at which audio change ends                               | 0.95      |
| VRCMinVolume           | Minimum volume of VRC                                          | 0.5       |
| VRCMaxVolume           | Maximum volume of VRC                                          | 1.0       |
| LowPassEnabled         | Enable Voicemeter basic integration for a lowpass effect       | false     |
| LowPassStrength        | Ammount of Lowpass effect (0.0-1.0)                            | 1.0       |
| MediaControlEnabled    | Enabling media control                                         | true      |
| MediaApplication       | Application the app looks for                                  |           |
| MediaMinVolume         | Minimum volume of media                                        | 0.25      |
| MediaMaxVolume         | Maximum volume of media                                        | 1.0       |
| MediaPauseEnbabled     | Allow the app to pause the media application                   | false     |
| MediaPauseThreshhold   | At this treshhold the app will attempt to pause media          | 0.9       |
| AvatarParameter        | OSC Parameter we listen to VRC for.                            |           |

ᴹᵃⁿ ᵗʰᵉʳᵉ'ˢ ᵃ ˡᵒᵗ ᵒᶠ ˢᵉᵗᵗᶦⁿᵍˢ

---

### Default Config.json

```json
tbd
```

# Credits

- @ALeonic is the actaul coder brain putting together my patchwork disfunctional code/ideas.
