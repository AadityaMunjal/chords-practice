from constants import NOTES, CHORDS, BLACK_NOTES

class Note:
  def __init__(self, note):
    if note in NOTES:
      self.note = note

    elif enharmonic_of(note) in NOTES:
      self.note = enharmonic_of(note)

    else:
      del self
      print("NOTE DOES NOT EXIST")


class ChordType:
  def __init__(self, chord: str):
    if chord in CHORDS.keys():
      self.chord_type = chord
      self.chord_degs = CHORDS[chord]

    else:
      del self
      print("CHORD TYPE DOES NOT EXIST")


def enharmonic_of(note: str):
  for n in BLACK_NOTES:
    for idx in range(2):
      if n[idx] == note:
        en_idx = 0 if idx == 1 else 1
        return n[en_idx]

def resolve_degree(deg: int):
  return deg % 12


def create_chord(root: Note, chord_type: ChordType):
  chord = []

  for degree in chord_type.chord_degs:
    chord.append(NOTES[resolve_degree(NOTES.index(root.note) + degree)])

  return chord



if __name__ == "__main__":
  c = create_chord(Note("Bb"), ChordType("MAJ7"))
  print(c)