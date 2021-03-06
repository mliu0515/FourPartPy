#This is just Denero's mario. I just copied and pasted it
from wave import open
from struct import Struct
from math import floor
from RingBuffer import *
import numpy as np
from matplotlib import pyplot as plt
# plt.title("Guitar String Results")
# plt.ylabel('Value')

y = []
frame_rate = SAMPLING_RATE

def encode(x):
    """Encode float x between -1 and 1 as two bytes.
    (See https://docs.python.org/3/library/struct.html)
    """
    i = int(16384 * x)
    print(i, x)
    return Struct('h').pack(i)

def graph_soundwaves(sampler, name="soundwave", seconds=2):
    plt.title(name)
    plt.ylabel("Values")
    lst = soundwave(sampler, seconds)
    plt.plot(lst)
    plt.show()

def soundwave(sampler, seconds=2):
    t = 0
    lst = []
    while t< seconds * frame_rate:
        sample = sampler(t)
        lst.append(sample)
        t += 1
    return lst

def play_lst(lst, name='lst-testing.wav', seconds=2):
    '''Write a list of values as a wave file.'''
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(frame_rate)
    for val in lst:
        out.writeframes(encode(val))
    out.close()

def play(sampler, name='pluck-guitar.wav', seconds=2):
    """Write the output of a sampler function as a wav file.
    (See https://docs.python.org/3/library/wave.html)
    """
    print('play function called!')
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(2)
    out.setframerate(frame_rate)
    t = 0
    while t < seconds * frame_rate:
        sample = sampler(t)
        t = t + 1
        out.writeframes(encode(sample))
    out.close()
    print('play function done!')

def play_buffer(b_sampler, name="guitar-testing.wav", seconds=2):
    '''Write the ouput of a sampler function as a wave file, but
    for a sampler funtion that generates from a buffer.'''
    out = open(name, 'wb')
    out.setnchannels(1)
    out.setsampwidth(1)
    out.setframerate(frame_rate)
    for t in range(seconds * frame_rate):
        sample = b_sampler()
        if not t % 1000:
            y.append(sample)
        out.writeframes(encode(sample))
    out.close()

def tri(frequency, amplitude=0.3):
    """A continuous triangle wave."""
    period = frame_rate // frequency
    def sampler(t):
        saw_wave = t / period - floor(t / period + 0.5)
        tri_wave = 2 * abs(2 * saw_wave) - 1
        return amplitude * tri_wave
    return sampler

c_freq, e_freq, g_freq = 261.63, 329.63, 392.00

# play(tri(e_freq))

def note(f, start, end, fade=.01):
    """Play f for a fixed duration."""
    def sampler(t):
        seconds = t / frame_rate
        if seconds < start:
            return 0
        elif seconds > end:
            return 0
        elif seconds < start + fade:
            return (seconds - start) / fade * f(t)
        elif seconds > end - fade:
            return (end - seconds) / fade * f(t)
        else:
            return f(t)
    return sampler

# play(note(tri(e_freq), 1, 1.5))

def both(f, g):
    return lambda t: f(t) + g(t)

c = tri(c_freq)
e = tri(e_freq)
g = tri(g_freq)
low_g = tri(g_freq / 2)

# play(both(note(e, 0, 1/8), note(low_g, 1/8, 3/8)))

# play(both(note(c, 0, 1), both(note(e, 0, 1), note(g, 0, 1))))

def mario(c, e, g, low_g):
    z = 0
    song = note(e, z, z + 1/8)
    z += 1/8
    song = both(song, note(e, z, z + 1/8))
    z += 1/4
    song = both(song, note(e, z, z + 1/8))
    z += 1/4
    song = both(song, note(c, z, z + 1/8))
    z += 1/8
    song = both(song, note(e, z, z + 1/8))
    z += 1/4
    song = both(song, note(g, z, z + 1/4))
    z += 1/2
    song = both(song, note(low_g, z, z + 1/4))
    return song

def mario_at(octave):
    c = tri(octave * c_freq)
    e = tri(octave * e_freq)
    g = tri(octave * g_freq)
    low_g = tri(octave * g_freq / 2)
    return mario(c, e, g, low_g)
# print(y)
# plt.plot(y)
# plt.show()
# need to change the scaling of the graph
# A4_sampler = pluck_guitar('A4', 0.5, 3)
# play(A4_sampler, 'checking.wav')


# play(both(mario_at(1), mario_at(1/2)))
# guitar = GuitarString(441)
# guitar.pluck()
# # make it sound better and get rid of all the static
# for _ in range(500):
#     guitar.sampler()
#
# # print(guitar.sample())
# play_buffer(guitar.sampler)
