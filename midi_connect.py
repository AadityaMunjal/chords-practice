from constants import NOTES
from generate_chords import get_random_chord

import pygame as pg
import pygame.midi

from colorama import Fore


def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()


def _print_device_info():
    for i in range(pygame.midi.get_count()):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print(
            "%2i: interface :%s:, name :%s:, opened :%s:  %s"
            % (i, interf, name, opened, in_out)
        )

def input_main(device_id=None):
    pg.init()
    pg.fastevent.init()
    event_get = pg.fastevent.get
    event_post = pg.fastevent.post

    pygame.midi.init()

    _print_device_info()

    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print("using input_id :%s:" % input_id)
    i = pygame.midi.Input(input_id)

    pg.display.set_mode((1, 1))

    going = True
    while going:
        events = event_get()
        for e in events:
            if e.type in [pg.QUIT]:
                going = False
            if e.type in [pg.KEYDOWN]:
                going = False
            if e.type in [pygame.midi.MIDIIN]:
                print(e)

        if i.poll():
            midi_events = i.read(1)
            # print(midi_events)
            note_id = midi_events[0][0][1]




            if midi_events[0][0][0] == 144:
              store_note(note_id)
            elif midi_events[0][0][0] == 128:
              delete_note(note_id)

            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                # event_post(m_e)
                pass

            on_event_change()
            a = ACTIVE_NOTES

    del i
    pygame.midi.quit()


ACTIVE_NOTES = []
all_current_chords = [get_random_chord()]
score = 0


def convert_id(resolved_id):
  return NOTES[resolved_id]

def store_note(note_id):
  ACTIVE_NOTES.append(convert_id(note_id % 12))

def delete_note(note_id):
  ACTIVE_NOTES.remove(convert_id(note_id % 12))

def on_event_change():
  if set(all_current_chords[-1][0]) == set(ACTIVE_NOTES):
    print(Fore.GREEN + "CORRECT!", end='\n\n\n')
    all_current_chords.append(get_random_chord())
    print(Fore.WHITE + all_current_chords[-1][2], Fore.WHITE + all_current_chords[-1][1])



def midi_connection():
  print_device_info()
  input_main()


def main():
  print(Fore.WHITE + all_current_chords[0][2], Fore.WHITE + all_current_chords[0][1])
  global time_start
  midi_connection()

if __name__ == "__main__":
  main()