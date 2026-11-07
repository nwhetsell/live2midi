# live2midi

[![Actions](https://github.com/nwhetsell/live2midi/workflows/CI/badge.svg)](https://github.com/nwhetsell/live2midi/actions?workflow=CI)

[live2midi.py](live2midi.py) is a Python script that parses notes and time signature changes from MIDI tracks in an [Ableton Live](https://www.ableton.com/live/) set (.als) file, and then writes them to either a single MIDI file, or one MIDI file per track.
It can handle tracks with any number of MIDI clips, loops, deactivated clips, and clips with deactivated notes.

To set up live2midi.py in a [virtual environment](https://docs.python.org/3/library/venv.html), run:

```sh
git clone https://github.com/nwhetsell/live2midi.git
cd live2midi
python -m venv .venv
source .venv/bin/activate
pip install --requirement requirements.txt
```

You can then parse MIDI from a Live set by running:

```sh
python live2midi.py '⟨My Song⟩.als'
```

To write one MIDI file per track run:

```sh
python live2midi.py '⟨My Song⟩.als' --type 0
```

live2midi.py’s test corpus is [test_live2midi.als.xml](test_live2midi.als.xml), a decompressed Live set file.
To compress the test corpus so that it can be opened in Live, run:

```sh
gzip --to-stdout test_live2midi.als.xml > test_live2midi.als
```
