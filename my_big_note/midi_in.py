import time
import rtmidi

apis = {}
for api in rtmidi.get_compiled_api():
    apis[rtmidi.get_api_name(api)] = api
print(apis)

midiin = rtmidi.MidiIn(apis['jack'])
# midiin = rtmidi.MidiIn(apis['alsa'])
available_ports = midiin.get_ports()

print(midiin)
print(available_ports)

midiin.open_port(1)

with midiin:
    while True:
        while msg := midiin.get_message():
            if msg:
                print(msg)
        time.sleep(.1)
