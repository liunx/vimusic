#!/usr/bin/env python

import time
import mido
from mido import Message, MidiFile, MidiTrack, tempo2bpm

key_dict = {
        # c4
        "a4+":22, "b4-":22, "b4": 23,
        # c3
        "c3": 24, "c3+": 25, "d3-": 25, "d3": 26, "d3+": 27, "e3-": 27, "e3": 28,
        "f3": 29, "f3+": 30, "g3-": 30, "g3": 31, "g3+": 32, "a3-": 32, "a3": 33,
        "a3+": 34, "b3-": 34, "b3": 35,
        # c2
        "c2": 36, "c2+": 37, "d2-": 37, "d2": 38, "d2+": 39, "e2-": 39, "e2": 40,
        "f2": 41, "f2+": 42, "g2-": 42, "g2": 43, "g2+": 44, "a2-": 44, "a2": 45,
        "a2+": 46, "b2-": 46, "b2": 47,
        # c1
        "c1": 48, "c1+": 49, "d1-": 49, "d1": 50, "d1+": 51, "e1-": 51, "e1": 52,
        "f1": 53, "f1+": 54, "g1-": 54, "g1": 55, "g1+": 56, "a1-": 56, "a1": 57,
        "a1+": 58, "b1-": 58, "b1": 59,
        # c
        "c": 60, "c+": 61, "d-": 61, "d": 62, "d+": 63, "e-": 63, "e": 64,
        "f": 65, "f+": 66, "g-": 66, "g": 67, "g+": 68, "a-": 68, "a": 69,
        "a+": 70, "b-": 70, "b": 71,
        # C1
        "C1": 72, "C1+": 73, "D1-": 73, "D1": 74, "D1+": 75, "E1-": 75, "E1": 76,
        "F1": 77, "F1+": 78, "G1-": 78, "G1": 79, "G1+": 80, "A1-": 80, "A1": 81,
        "A1+": 82, "B1-": 82, "B1": 83,
        # C2
        "C2": 84, "C2+": 85, "D2-": 85, "D2": 86, "D2+": 87, "E2-": 87, "E2": 88,
        "F2": 89, "F2+": 90, "G2-": 90, "G2": 91, "G2+": 92, "A2-": 92, "A2": 93,
        "A2+": 94, "B2-": 94, "B2": 95,
        # C3
        "C3": 84, "C3+": 85, "D3-": 85, "D3": 86, "D3+": 87, "E3-": 87, "E3": 88,
        "F3": 89, "F3+": 90, "G3-": 90, "G3": 91, "G3+": 92, "A3-": 92, "A3": 93,
        "A3+": 94, "B3-": 94, "B3": 95,
        # C4
        "C4": 96, "C4+": 97, "D4-": 97
        }


class Composer:
    def __init__(self, tempo=720, midi_type=1):
        self.tempo = tempo
        self.midi_file = MidiFile(type=midi_type)

    def track(self, program=1):
        midi_track = MidiTrack()
        self.midi_file.tracks.append(midi_track)
        midi_track.append(Message('program_change', program=program))
        return midi_track

    def program(self, track, program):
        track.append(Message('program_change', program=program))

    def note(self, track, note):
        midi_note = key_dict[note[0]]
        midi_time = int(self.tempo * note[1])
        track.append(Message('note_on', note=midi_note, velocity=100, time=0))
        track.append(Message('note_off', note=midi_note, velocity=0, time=midi_time))

        #track.append(Message('note_on', note=0, velocity=100, time=0))
        #track.append(Message('note_off', note=0, velocity=0, time=midi_time*10))

    def save(self, name):
        self.midi_file.save(name)


joy_notes = [
        ["e", 1./4.], ["e", 1./4.], ["f", 1./4.], ["g", 1./4.],
        ["g", 1./4.], ["f", 1./4.], ["e", 1./4.], ["d", 1./4.],
        ["c", 1./4.], ["c", 1./4.], ["d", 1./4.], ["e", 1./4.],
        ["e", 1./2.], ["d", 1./4.], ["d", 1./4.],
        ["e", 1./4.], ["e", 1./4.], ["f", 1./4.], ["g", 1./4.],
        ["g", 1./4.], ["f", 1./4.], ["e", 1./4.], ["d", 1./4.],
        ["c", 1./4.], ["c", 1./4.], ["d", 1./4.], ["e", 1./4.],
        ["d", 1./2.], ["c", 1./4.], ["c", 1./4.],
        ]


def demo1():
    demo = Composer()
    track = demo.track()

    for n in joy_notes:
        demo.note(track, n)

    demo.save('joy.mid')


def play_note():
    midi_note = 64
    midi_time = 640
    for i in range(10):
        with mido.open_output('FLUID Synth (25699):Synth input port (25699:0) 129:0') as output:
            output.send(Message('program_change', program=1))

            output.send(Message('note_on', note=midi_note, velocity=100, time=0))
            output.send(Message('note_on', note=midi_note + 4, velocity=100, time=0))
            output.send(Message('note_on', note=midi_note + 7, velocity=100, time=0))
            time.sleep(1)
            output.send(Message('note_off', note=midi_note, velocity=0, time=midi_time))
            output.send(Message('note_off', note=midi_note + 4, velocity=100, time=midi_time))
            output.send(Message('note_off', note=midi_note + 7, velocity=100, time=midi_time))


if __name__ == "__main__":
    #demo1()
    play_note()

