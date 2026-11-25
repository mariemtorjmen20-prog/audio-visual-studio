"""Build the HyperFrames composition from the selected screenplay and cast."""
import hashlib
import json
import math
import pathlib
import struct
import subprocess
import wave
from html import escape
from shutil import copyfile
from string import Template

ROOT = pathlib.Path(__file__).resolve().parent
SPEECH = {"boss": ("en-us+m3", "30"), "employee": ("en-us+m1", "65")}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def stage_cast(assets):
    cast = json.loads((ROOT / "cast.json").read_text(encoding="utf-8"))
    if set(cast) != set(SPEECH):
        raise ValueError("cast.json must define the boss and employee slots")

    source_dir = ROOT / "characters"
    images = []
    evidence = {}
    for slot, character in cast.items():
        source = (source_dir / character["image"]).resolve()
        if source.parent != source_dir or source.suffix.lower() != ".png":
            raise ValueError(f"{slot}: choose a PNG file directly inside characters/")
        data = source.read_bytes()
        if not data.startswith(PNG_SIGNATURE) or data[12:16] != b"IHDR":
            raise ValueError(f"{slot}: {source.name} is not a PNG")
        staged = assets / f"{slot}.png"
        copyfile(source, staged)
        images.append(
            f'<img id="{slot}" class="character" src="assets/{staged.name}" '
            f'alt="{escape(character["name"], quote=True)}">'
        )
        evidence[slot] = {
            "source": source.relative_to(ROOT).as_posix(),
            "render_input": staged.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    return "\n".join(images), evidence


def main():
    story = json.loads((ROOT / "story.json").read_text(encoding="utf-8"))
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    # Leave the existing SVG pilot usable when no image cast has been supplied.
    evidence_path = assets / "cast-evidence.json"
    evidence_path.unlink(missing_ok=True)
    image_cast = (ROOT / "cast.json").is_file()
    characters, evidence = stage_cast(assets) if image_cast else ("", {})
    clips = []
    cues = []

    for index, line in enumerate(story["dialogue"]):
        speaker = line["speaker"]
        voice, pitch = SPEECH[speaker]
        start, end = line["start"], line["end"]
        path = assets / f"line{index}.wav"
        subprocess.run(
            ["espeak-ng", "-v", voice, "-p", pitch, "-s", "165",
             "-w", str(path), "--stdin"],
            input=line["text"], encoding="utf-8", check=True,
        )
        with wave.open(str(path), "rb") as audio:
            rate = audio.getframerate()
            frames = audio.getnframes()
            samples = struct.unpack(f"<{frames}h", audio.readframes(frames))
        duration = frames / rate
        if not 0 <= start < end <= story["duration"] or duration > end - start:
            raise ValueError(f"Dialogue line {index + 1} needs {duration:.2f}s within its time slot")

        timing = f'data-start="{start}" data-duration="{duration}"'
        clips.append(
            f'<audio id="audio{index}" class="clip" src="assets/{path.name}" '
            f'{timing} data-track-index="2"></audio>'
        )
        # Use voice amplitude for sprite movement or the original SVG mouth cues.
        window = rate // 12
        for offset in range(0, frames, window):
            part = samples[offset:offset + window]
            rms = math.sqrt(sum(value * value for value in part) / len(part))
            strength = min(1, rms / 3000)
            cues.append([speaker, start + offset / rate, strength if image_cast else max(0.12, strength)])
        cues.append([speaker, start + duration, 0 if image_cast else 0.12])
        clips.append(
            f'<div id="caption{index}" class="clip caption" {timing} '
            f'data-track-index="3">{escape(line["text"])}</div>'
        )

    media = "\n".join(clips)
    motion = json.dumps(cues)
    if image_cast:
        template = (ROOT / "characters.html.tpl").read_text(encoding="utf-8")
        composition = Template(template).substitute(
            title=escape(story["title"]), characters=characters, media=media, cues=motion,
        )
    else:
        template = (ROOT / "template.html.tpl").read_text(encoding="utf-8")
        composition = template.replace("<!-- MEDIA -->", media).replace("/* CUES */", motion)

    (ROOT / "index.html").write_text(composition, encoding="utf-8")
    if image_cast:
        evidence_path.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(f"Prepared {len(clips) // 2} voice clips and {len(cues)} motion cues")


if __name__ == "__main__":
    main()
