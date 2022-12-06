import voicemeeter

# Can be 'basic', 'banana' or 'potato'
kind = 'basic'

# Ensure that Voicemeeter is launched
voicemeeter.launch(kind)

with voicemeeter.remote(kind) as vmr:
    vmr.inputs[2].eqgain1 = 12.0
    vmr.inputs[2].eqgain2 = -10.0
    vmr.inputs[2].eqgain3 = -4.2
    vmr.inputs[2].gain = -22.0