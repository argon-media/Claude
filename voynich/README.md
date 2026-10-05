# Voynich Manuscript (Beinecke MS 408) — text transcription

- `text16e6.evt` — Landini–Stolfi *Interlinear Archive* (release 1.6e6, 1998) in EVA
  (European Voynich Alphabet). Several transcribers per line; codes include
  H = Takahashi (complete), C = Currier, F = Friedman, etc. Header comments describe the format.
  Copied from https://github.com/viking-sudo-rm/voynich2vec.
- `extract.py` — pulls one transcriber's lines into plain text (`python extract.py H`).
- `takahashi.txt` — output of `extract.py H`: 5,213 lines, 225 pages, ~37,000 words.
  Format: `<page.unit.line>\t<words separated by spaces>`. `*` = unreadable glyph.

Page images are public domain at Yale's Beinecke Library
(https://collections.library.yale.edu/catalog/2002046), not included here.
