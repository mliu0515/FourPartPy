from sound import *
from RingBuffer import *
from piece_classes import *
from wave import open
from struct import Struct
import numpy as np
from matplotlib import pyplot as plt

frame_rate = SAMPLING_RATE

class Music:
    """A class which plays the music as read in by a piece class"""
    def __init__(self):
        '''Set up the guitar and piece reading capabilities'''
        Note.generate_equal()
        pitch_dict = Note.pitch_dict
        self.strings = {}
        for note in Note.pitch_dict:
            self.strings[note] = GuitarString(Note.pitch_dict[note])

    def pluck_guitar(self, note, start, end):
        '''Takes in a note object and a duration and plucks the guitar
        with its frequency. Start is the time that you want the guitar to be
        plucked and end is when you want the sound to cut out.'''
        string = self.strings[str(note)]
        string.pluck()
        def sampler(t):
            seconds = t/frame_rate
            if seconds < start:
                return 0
            elif seconds > end:
                return 0
            else:
                return string.sampler()
        return sampler

    def encode(self, x):
        """Encode float x between -1 and 1 as two bytes.
        (See https://docs.python.org/3/library/struct.html)
        """
        i = int(16384 * x)
        print(i, x)
        return Struct('h').pack(i)

    def graph_soundwaves(self, sampler, name="soundwave", seconds=2):
        plt.title(name)
        plt.ylabel("Values")
        lst = soundwave(sampler, seconds)
        plt.plot(lst)
        plt.show()

    def soundwave(self, sampler, start=0, end=2):
        t = start * frame_rate
        lst = []
        while t< end * frame_rate:
            sample = sampler(t)
            lst.append(sample)
            t += 1
        self.normalize_lst(lst)
        return lst

    def play_lst(self, lst, name='class-testing.wav'):
        '''Write a list of values as a wave file.'''
        out = open(name, 'wb')
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(frame_rate)
        for val in lst:
            out.writeframes(self.encode(val))
        out.close()

    def chord_sampler(self, chord, start, end):
        '''Returns a sampler of a chord instance from piece_classes.py
        >>> chord is a Chord instance with C3, G3, E4, and C5
        >>> play_chord2(chord, start, end)
        '''
        samplers = []
        for note in chord.voices.values():
            samplers.append(self.pluck_guitar(note, start, end))
        def sampler(t):
            total = 0
            for s in samplers:
                total += s(t)
            return total
        return sampler

    def play_chord(self, chord, start=0):
        '''Plays a chord instance from the piece_classes.py classes
        and determines its length in seconds. Has a predetermined starting point
        which is given in seconds.'''
        sampler = self.chord_sampler(chord, start, start + chord.num_seconds)
        lst = self.soundwave(sampler, start, start + chord.num_seconds)
        self.play_lst(lst)


    def normalize_lst(self, lst):
        '''Take a list which has values which are larger than the limit and then
        normalize that list so that is within the normal limit (-1, 1)'''
        curr = max(lst)
        for i in range(len(lst)):
            lst[i] = lst[i]/curr

### testing for chord sampler
muse = Music()
C3 = Note('C', 3)
C4 = Note('C', 4)
G4 = Note('G', 4)
E4 = Note('E', 4)
c_major_triad = Chord(C3, C4, G4, E4)
c_major_triad.num_seconds = 4
muse.play_chord(c_major_triad)
