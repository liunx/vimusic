#!/usr/bin/env python
#-*- coding:utf-8 -*-

from pynput import keyboard
import time
import os
import mido
from mido import Message, MidiFile, MidiTrack, tempo2bpm

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

base_note = 64

def on_press(key):
    global base_note
    try:
        if key.char == 'z':
            if base_note > 12:
                base_note -= 12
        elif key.char == 'x':
            if base_note < 127 - 12:
                base_note += 12
        elif key.char == ',':
            if base_note > 12:
                base_note -= 12
        elif key.char == '.':
            if base_note < 127 - 12:
                base_note += 12
        elif key.char == '/':
            if base_note < 127 - 12:
                base_note += 12

        data = midi_seqs.get("'{}'".format(key.char))
        if data != None:
            midi_note = data[0]
            state = data[1]
            if state == False:
                midi_port.send(Message('note_on', note=(midi_note + base_note), velocity=100, time=0))
                data[1] = True
    except AttributeError:
        pass

def on_release(key):
    data = midi_seqs.get(str(key))
    if data != None:
        midi_note = data[0]
        data[1] = False
        midi_port.send(Message('note_off', note=(midi_note + base_note), velocity=100, time=0))
    if key == keyboard.Key.esc:
        # Stop listener
        return False


if __name__ == "__main__":
    fluid_port = 'FLUID Synth (2552):Synth input port (2552:0) 129:0'

    os.system("stty -echo")
    with mido.open_output(fluid_port) as midi_port:
        midi_port.send(Message('program_change', program=1))
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    os.system("stty echo")
