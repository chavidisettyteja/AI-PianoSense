class ChordDetector:

    def __init__(self):

        self.chords = {
            frozenset(["C", "E", "G"]): "C Major",
            frozenset(["A", "C", "E"]): "A Minor",
            frozenset(["F", "A", "C"]): "F Major",
            frozenset(["G", "B", "D"]): "G Major",
            frozenset(["D", "F", "A"]): "D Minor",
            frozenset(["E", "G", "B"]): "E Minor"
        }

    def detect(self, notes_with_octave):

        # Remove octave numbers (C4 -> C, Gb5 -> Gb)
        notes = set()

        for note in notes_with_octave:

            if note[-1].isdigit():
                notes.add(note[:-1])
            else:
                notes.add(note)

        return self.chords.get(frozenset(notes), None)