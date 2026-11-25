"""Independent technical acceptance checks; visual review remains manual."""
import json,subprocess,pathlib
p=pathlib.Path(__file__).resolve().parent/'final.mp4'
d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
v=next(s for s in d['streams'] if s['codec_type']=='video')
assert (v['width'],v['height'])==(720,1280)
assert any(s['codec_type']=='audio' for s in d['streams'])
assert abs(float(d['format']['duration'])-20)<.5
(p.parent/'qa.json').write_text(json.dumps({'technical':'pass','visual_review':'pending','probe':d},indent=2))
print('PASS: video dimensions, duration, audio stream')
