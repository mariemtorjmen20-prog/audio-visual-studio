"""Check the exported video format and record which cast assets were staged."""
import hashlib
import json
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
probe = json.loads(subprocess.check_output([
    "ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json",
    str(ROOT / "final.mp4"),
]))
video = next(stream for stream in probe["streams"] if stream["codec_type"] == "video")
assert (video["width"], video["height"]) == (720, 1280)
assert any(stream["codec_type"] == "audio" for stream in probe["streams"])
assert abs(float(probe["format"]["duration"]) - 20) < 0.5

report = {"technical": "pass", "visual_review": "pending", "probe": probe}
if (ROOT / "cast.json").is_file():
    cast = json.loads((ROOT / "assets/cast-evidence.json").read_text(encoding="utf-8"))
    for slot, asset in cast.items():
        for field in ("source", "render_input"):
            digest = hashlib.sha256((ROOT / asset[field]).read_bytes()).hexdigest()
            if digest != asset["sha256"]:
                raise ValueError(f"{slot}: cast image checksum mismatch for {asset[field]}")
    report["cast"] = cast

(ROOT / "qa.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print("PASS: video dimensions, duration, audio stream and any configured cast input checksums")
