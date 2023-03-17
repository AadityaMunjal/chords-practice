from constants import CHORDS, NOTES
from chords import create_chord, Note, ChordType
import random 

def get_random_chord():
  key = random.choice(NOTES)
  chord_type, chord_deg = random.choice(list(CHORDS.items()))

  c = create_chord(Note(key), ChordType(chord_type))

  return c, chord_type, key


