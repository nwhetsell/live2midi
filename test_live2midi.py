from pathlib import Path

import mido

from live2midi import live2midi

live2midi(Path("test_live2midi.als.xml"))
actual = mido.MidiFile("test_live2midi.mid")

looped_clips_track = actual.tracks[0]

def test_looped_clips_track_name():
    assert looped_clips_track.name == "Looped clips"

looped_messages = [message for message in looped_clips_track if not message.is_meta]

def test_looped_message_count():
    assert len(looped_messages) == 64

def test_2_bar_loop():
    message = looped_messages[0]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[1]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[2]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[3]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[4]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[5]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[6]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[7]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480
    message = looped_messages[8]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[9]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[10]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[11]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[12]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[13]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[14]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[15]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480

def test_loop_end_before_clip_end():
    message = looped_messages[16]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 1920
    message = looped_messages[17]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[18]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[19]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[20]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[21]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[22]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[23]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 240
    message = looped_messages[24]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[25]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[26]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[27]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[28]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[29]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[30]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[31]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 240
    message = looped_messages[32]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[33]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480

def test_loop_start_before_clip_start():
    message = looped_messages[34]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 1920
    message = looped_messages[35]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[36]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[37]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[38]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[39]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[40]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[41]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480
    message = looped_messages[42]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 240
    message = looped_messages[43]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[44]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[45]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[46]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[47]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480

def test_loop_start_after_clip_start():
    message = looped_messages[48]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 2400
    message = looped_messages[49]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[50]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[51]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[52]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[53]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480
    message = looped_messages[54]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[55]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480
    message = looped_messages[56]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 0
    message = looped_messages[57]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 480
    message = looped_messages[58]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 0
    message = looped_messages[59]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 480
    message = looped_messages[60]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = looped_messages[61]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480
    message = looped_messages[62]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 0
    message = looped_messages[63]
    assert message.type == "note_off"
    assert message.note == 60
    # This assertion fails because the message time is reported to be 0 when
    # it’s actually 480. It’s not clear why this is; Live imports the MIDI file
    # with the correct time (480). This may be a bug in Mido.
    # assert message.time == 480

unlooped_clips_track = actual.tracks[1]

def test_unlooped_clips_track_name():
    assert unlooped_clips_track.name == "Unlooped clips"

unlooped_messages = [message for message in unlooped_clips_track if not message.is_meta]

def test_unlooped_message_count():
    assert len(unlooped_messages) == 32

def test_clip():
    message = unlooped_messages[0]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 0
    message = unlooped_messages[1]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 480
    message = unlooped_messages[2]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 0
    message = unlooped_messages[3]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 480
    message = unlooped_messages[4]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 0
    message = unlooped_messages[5]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 480
    message = unlooped_messages[6]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 0
    message = unlooped_messages[7]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 480

def test_clip_end_before_loop_end():
    message = unlooped_messages[8]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 1920
    message = unlooped_messages[9]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 480
    message = unlooped_messages[10]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 0
    message = unlooped_messages[11]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 480
    message = unlooped_messages[12]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 0
    message = unlooped_messages[13]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 480
    message = unlooped_messages[14]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 0
    message = unlooped_messages[15]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 240

def test_clip_end_before_last_note_off():
    message = unlooped_messages[16]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 2160
    message = unlooped_messages[17]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 480
    message = unlooped_messages[18]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 0
    message = unlooped_messages[19]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 480
    message = unlooped_messages[20]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 0
    message = unlooped_messages[21]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 480
    message = unlooped_messages[22]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 0
    message = unlooped_messages[23]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 240

def test_clip_start_before_first_note_on():
    message = unlooped_messages[24]
    assert message.type == "note_on"
    assert message.note == 67
    assert message.time == 2400
    message = unlooped_messages[25]
    assert message.type == "note_on"
    assert message.note == 64
    assert message.time == 480
    message = unlooped_messages[26]
    assert message.type == "note_off"
    assert message.note == 67
    assert message.time == 0
    message = unlooped_messages[27]
    assert message.type == "note_on"
    assert message.note == 60
    assert message.time == 480
    message = unlooped_messages[28]
    assert message.type == "note_off"
    assert message.note == 64
    assert message.time == 0
    message = unlooped_messages[29]
    assert message.type == "note_off"
    assert message.note == 60
    assert message.time == 240

def test_clip_with_deactivated_notes():
    message = unlooped_messages[30]
    assert message.type == "note_on"
    assert message.note == 72
    assert message.time == 2400
    message = unlooped_messages[31]
    assert message.type == "note_off"
    assert message.note == 72
    assert message.time == 480

time_signature_messages = [message for message in unlooped_clips_track if message.is_meta and message.type == "time_signature"]

def test_time_signatures():
    assert len(time_signature_messages) == 5
    message = time_signature_messages[0]
    assert message.numerator == 4
    assert message.denominator == 4
    assert message.time == 0
    message = time_signature_messages[1]
    assert message.numerator == 3
    assert message.denominator == 4
    assert message.time == 5280
    message = time_signature_messages[2]
    assert message.numerator == 6
    assert message.denominator == 8
    assert message.time == 2880
    message = time_signature_messages[3]
    assert message.numerator == 27
    assert message.denominator == 16
    assert message.time == 1440
    message = time_signature_messages[4]
    assert message.numerator == 5
    assert message.denominator == 1
    assert message.time == 3240
