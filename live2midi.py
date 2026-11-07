import argparse
import copy
import gzip
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import mido
import pitchtools
from rich.console import Console
from rich.table import Table


def live2midi(file_path: Path, midi_type=1, verbose=False):
    class Note:
        def __init__(self, midi_note_number: int, element: ET.Element):
            self.midi_note_number = midi_note_number
            self.time = float(element.attrib["Time"])
            self.duration = float(element.attrib["Duration"])
            self.velocity = float(element.attrib["Velocity"])
            self.off_velocity = float(element.attrib["OffVelocity"])

    def find_value(element: ET.Element, path: str, default="0") -> str:
        e = element.find(path)
        if e is None:
            return default
        return e.attrib["Value"]

    def note_table(notes: list[Note]) -> Table:
        table = Table(header_style="bold")
        table.add_column("Note No.")
        table.add_column("Pitch")
        table.add_column("Start time", justify="right")
        table.add_column("Duration", justify="right")
        for note in sorted(notes, key=lambda note: note.time):
            table.add_row(str(note.midi_note_number), pitchtools.m2n(note.midi_note_number), str(note.time), str(note.duration))
        return table

    ticks_per_beat = mido.MidiFile().ticks_per_beat

    console = Console()

    with console.status("Parsing Live set...") as status:
        if file_path.suffix == ".xml":
            with open(file_path, "r") as f:
                xml_content = f.read()
        else:
            with gzip.open(file_path, "rb") as f:
                xml_content = f.read()
        root = ET.fromstring(xml_content)

        # Get time signature changes.
        time_signature_events: list[mido.MetaMessage] = []
        for event in root.findall("LiveSet/MainTrack/AutomationEnvelopes/Envelopes/AutomationEnvelope/EnvelopeTarget/PointeeId[@Value='10']/../..Automation/Events/EnumEvent"):
            numerator = int(event.attrib["Value"]) + 1
            denominator = 1
            while numerator > 99:
                numerator -= 99
                denominator *= 2
            time_signature_events.append(mido.MetaMessage(
                "time_signature",
                numerator=numerator,
                denominator=denominator,
                time=int(max(float(event.attrib["Time"]), 0) * ticks_per_beat)
            ))

        midi_tracks: list[mido.MidiTrack] = []
        for live_track in root.findall("LiveSet/Tracks/MidiTrack"):
            track_name = find_value(live_track, "Name/EffectiveName")
            if verbose:
                console.print(f"Parsing track “[bold green]{track_name}[/bold green]”\n")

            track_messages: list[mido.Message | mido.MetaMessage] = []
            track_messages.extend(copy.deepcopy(time_signature_events))

            for midi_clip in live_track.findall("DeviceChain/MainSequencer/ClipTimeable/ArrangerAutomation/Events/MidiClip"):
                if find_value(midi_clip, "Disabled") == "true":
                    continue;

                midi_clip_start = float(find_value(midi_clip, "CurrentStart"))
                midi_clip_end = float(find_value(midi_clip, "CurrentEnd"))
                if verbose:
                    clip_name = find_value(midi_clip, "Name", default="")
                    if len(clip_name) > 0:
                        console.print(f"Parsing clip “[bold]{clip_name}[/bold]”.")
                    else:
                        console.print(f"Parsing clip with start time {midi_clip_start}, end time {midi_clip_end}.")

                midi_clip_notes: list[Note] = []
                for key_track in midi_clip.findall("Notes/KeyTracks/KeyTrack"):
                    midi_note_number = int(find_value(key_track, "MidiKey"))
                    for note_element in key_track.findall("Notes/MidiNoteEvent"):
                        if note_element.get("IsEnabled") != "false":
                            midi_clip_notes.append(Note(midi_note_number, note_element))

                notes: list[Note] = []

                loop = midi_clip.find("Loop")
                assert loop is not None
                loop_start = float(find_value(loop, "LoopStart"))
                if find_value(loop, "LoopOn") != "true":
                    for note in midi_clip_notes:
                        note.time -= loop_start
                        if note.time >= 0:
                            notes.append(note)
                else:
                    loop_start_relative = float(find_value(loop, "StartRelative"))
                    loop_end = float(find_value(loop, "LoopEnd"))
                    absolute_start_time = loop_start + loop_start_relative
                    if verbose:
                        console.print(f"Parsing loop with relative start {loop_start_relative}, start time {loop_start} (absolute start time {absolute_start_time}), end time {loop_end}, clip notes:")
                        console.print(note_table(midi_clip_notes))

                    time_offset = -absolute_start_time
                    for note in copy.deepcopy(midi_clip_notes):
                        if absolute_start_time <= note.time and note.time < loop_end:
                            note.time += time_offset
                            note.duration = min(note.duration, loop_end - note.time)
                            notes.append(note)

                    looped_notes: list[Note] = []
                    if loop_start_relative < 0:
                        time_offset = loop_start_relative
                    for note in midi_clip_notes:
                        if loop_start <= note.time and note.time < loop_end:
                            note.time += time_offset
                            note.duration = min(note.duration, loop_end - note.time)
                            if note.duration > 0:
                                looped_notes.append(note)
                    if verbose:
                        console.print(f"Looping {len(looped_notes)} notes:")
                        console.print(note_table(looped_notes))

                    time_offset = loop_end
                    loop_duration = loop_end - loop_start
                    max_time = midi_clip_end - midi_clip_start + loop_duration
                    while time_offset < max_time:
                        for note in copy.deepcopy(looped_notes):
                            note.time += time_offset
                            notes.append(note)
                        time_offset += loop_duration

                if len(notes) > 0:
                    if verbose:
                        console.print(f"Parsed {len(notes)} notes:")
                        console.print(note_table(notes))

                    for note in notes:
                        time = midi_clip_start + note.time
                        note.duration = min(note.duration, midi_clip_end - time)
                        if note.duration > 0:
                            track_messages.append(mido.Message(
                                "note_on",
                                note=note.midi_note_number,
                                time=int(time * ticks_per_beat),
                                velocity=int(note.velocity)
                            ))
                            track_messages.append(mido.Message(
                                "note_off",
                                note=note.midi_note_number,
                                time=int((time + note.duration) * ticks_per_beat),
                                velocity=int(note.off_velocity)
                            ))
                else:
                    track_messages.clear()

            if len(track_messages) > 0:
                midi_track = mido.MidiTrack()
                midi_track.name = track_name
                midi_tracks.append(midi_track)

                previous_time = 0
                for message in sorted(track_messages, key=lambda message: message.time): # pyright: ignore
                    time = message.time # pyright: ignore
                    message.time -= previous_time # pyright: ignore
                    midi_track.append(message)
                    previous_time = time

    with console.status("Writing files...") as status:
        if midi_type == 0:
            midi_path = file_path.parent.joinpath("midi")
            midi_path.mkdir(exist_ok=True)

            for midi_track in midi_tracks:
                midi_file = mido.MidiFile(type=0, tracks=[midi_track], ticks_per_beat=ticks_per_beat)
                name = f"{re.sub(r"/", "-", midi_track.name)}"
                midi_file.save(midi_path.joinpath(name).with_suffix(".mid"))
        else:
            midi_file = mido.MidiFile(type=1, tracks=midi_tracks, ticks_per_beat=ticks_per_beat)
            while file_path.suffix:
                file_path = file_path.with_suffix("")
            midi_file.save(file_path.with_suffix(".mid"))

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str, help="file path")
    parser.add_argument("--type", type=int, choices=[0, 1], default=1, help="MIDI file type (0 for multiple files)")
    parser.add_argument("--verbose", action="store_true", help="increase output verbosity")
    args = parser.parse_args()
    live2midi(Path(args.file_path), args.type, args.verbose)
    return 0

if __name__ == "__main__":
    sys.exit(main())
