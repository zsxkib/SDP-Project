import pyaudio
import wave

import numpy as np
import subprocess
import re
from threading import Thread
import time

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read().decode('utf8')

def usb_dev_mapping(
    command = 'v4l2-ctl --list-devices',
    usb_re = re.compile('usb-([0-9\.]+)\)'),
    dev_re = re.compile('/dev/video[0-9]'),
):
    ret = {}
    lines = system_call(command).split('\n')
    for line, next_line in zip(lines[:-1], lines[1:]):
        if 'usb' in line:
            for usb, dev in zip(usb_re.findall(line), dev_re.findall(next_line)):
                ret[usb] = dev
    return ret


print('getting usbport-device mapping...')
usbmap = usb_dev_mapping()
print(usbmap)

print('importing opencv... (few seconds)')
import cv2

class Camera():
    # use the usbmap above by default, assume it doesn't change (no hot plugging)
    # no need set fps too high
    def __init__(self, usbport, width=640, height=360, fps=10, usbmap=usbmap):
        self.usbport = usbport
        self.device = usbmap[usbport]
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = cv2.VideoCapture(self.device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, fps)
        print('capturing first frame for warm-up')
        arr = self._capture()
        if arr.shape != (height, width, 3):
            print('warning: dimensions dont match settings', arr.shape, (height, width, 3))
        self.loop_thread = Thread(target=self._capture_loop)
        self.loop_thread.start()
        self.audio_buffer = []
        self.audio_buffer_size = 20
        self.audio_thread = Thread(target=self._record_loop)
        self.audio_thread.start()

    def _capture_loop(self):
        print('starting capture loop')
        while True:
            self.current_image = self._capture()

    def _capture(self):
        # TODO investigate jpeg corrupt warnings
        _, frame = self.cap.read()
        # bgr to rgb (TODO set the format directly at init time?)
        return np.array(frame)[..., ::-1]

    def capture(self):
        return self.current_image

    def _record_loop(self):
        print('starting record loop')
        audio = pyaudio.PyAudio()
        dname = lambda i: audio.get_device_info_by_index(i).get('name')
        index = [
            i for i in range(audio.get_device_count())
            if 'USB' in dname(i)
        ][0]
        print('use audio device', index, dname(index))

        # strangely 44100 doesnt work on c270?, use the next common samplerate
        format = pyaudio.paInt16
        rate = 48000
        channels = 1
        buffer_size = 12000
        stream = audio.open(
            format = format,
            rate = rate,
            channels = channels,
            frames_per_buffer = buffer_size,
            input_device_index = index,
            input = True,
        )
        while True:
            self.audio_buffer.append( stream.read(buffer_size, exception_on_overflow = False) )
            if len(self.audio_buffer) > self.audio_buffer_size:
                self.audio_buffer.pop(0)

    def record(self):
        return np.frombuffer(self.record_binary(), dtype=np.int16)

    def record_binary(self):
        return b''.join(self.audio_buffer)
