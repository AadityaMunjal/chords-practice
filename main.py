from midi_connect import input_main, print_device_info, ACTIVE_NOTES
from generate_chords import get_random_chord
from multiprocessing import Process, freeze_support
import time

def check_chords():
  for i in range(5):
    print("hi")
    chord, chord_name, key = get_random_chord()
    print(key, chord_name)

    while True:
      # print(set(ACTIVE_NOTES), set(chord))
      # if set(ACTIVE_NOTES) == set(chord):
      #   print("correct!")
      print(ACTIVE_NOTES)


def midi_connection():
  print_device_info()
  input_main()


def main():
  check_chords_p = Process(target=check_chords)
  check_chords_p.start()
  midi_connect_p = Process(target=midi_connection)
  midi_connect_p.start()

  check_chords_p.join()
  midi_connect_p.join()


if __name__ == "__main__":
  main()