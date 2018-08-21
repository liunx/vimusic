#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pynput import keyboard
import time
import os
import mido
from mido import Message, MidiFile, MidiTrack, tempo2bpm
import queue
import threading
from enum import Enum


midi_seqs = {
        "'a'": [0, False],
        "'w'": [1, False],
        "'s'": [2 , False],
        "'e'": [3 , False],
        "'d'": [4 , False],
        "'f'": [5 , False],
        "'g'": [6 , False],
        "'h'": [6 , False],
        "'j'": [7 , False],
        "'i'": [8 , False],
        "'k'": [9 , False],
        "'o'": [10, False],
        "'l'": [11, False],
        "';'": [12, False]
        }

midi_shift_keys = {
        "'z'": -12,
        "'x'": +12,
        "','": -12,
        "'.'": +12,
        "'/'": +12,
        }

# mode
C = 64
Csharp = 65
Dflat = 65
D = 66
Dsharp = 67
Eflat = 67
E = 68
F = 69
Fsharp = 70
Gflat = 70
G = 71
Gsharp = 72
Aflat = 72
A = 73
Asharp = 74
Bflat = 74
B = 75


def on_press(key):
    global base_note
    try:
        q.put(['P', "'{}'".format(key.char)])
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        q.put(['R', 'QUIT'])
        return False

    q.put(['R', str(key)])


def worker2(q):
    print("starting Worker2 thread...")

    count = 0
    stack = []
    while True:
        if not q.empty():
            item = q.get_nowait()
            q.task_done()
            if item[1] == "QUIT":
                print("Worker2 thread quit!")
                return
            if count < 5:
                stack.append(item)
                time.sleep(0.001)
                count += 1
                continue
        if stack:
            for i in stack:
                if i[0] == 'P':
                    print(i[1])
            stack = []
            count = 0

        time.sleep(0.001)


def worker(q):
    print("starting Worker thread...")

    fluid_port = 'FLUID Synth (2552):Synth input port (2552:0) 129:0'
    base_note = C

    with mido.open_output(fluid_port) as midi_port:
        midi_port.send(Message('program_change', program=1))
        while True:
            if not q.empty():
                item = q.get_nowait()
                q.task_done()

                if item[1] == "QUIT":
                    print("Worker thread quit!")
                    return

                if item[0] == 'P':
                    data = midi_shift_keys.get(item[1])
                    if data != None:
                        tmp_note = base_note + data
                        if tmp_note > 0 and tmp_note < 127:
                            base_note = tmp_note
                        continue

                    data = midi_seqs.get(item[1])
                    if data != None:
                        midi_note = data[0]
                        state = data[1]
                        if state == False:
                            midi_port.send(Message('note_on', note=(midi_note + base_note), velocity=100, time=0))
                            data[1] = True
                elif item[0] == 'R':
                    data = midi_seqs.get(item[1])
                    if data != None:
                        midi_note = data[0]
                        data[1] = False
                        midi_port.send(Message('note_off', note=(midi_note + base_note), velocity=100, time=0))
            time.sleep(0.001)


if __name__ == "__main__":
    q = queue.Queue()
    t = threading.Thread(target=worker2, args=(q,))
    t.start()

    os.system("stty -echo")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    os.system("stty echo")
    t.join()
