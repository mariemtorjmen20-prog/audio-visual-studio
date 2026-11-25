"""Generate a deterministic HyperFrames composition and offline test dialogue.
eSpeak NG is deliberately used for the first smoke test; replace it with Kokoro
and Rhubarb for natural speech and phonetic mouth cues."""
import json, subprocess, pathlib, wave, struct, math
from xml.sax.saxutils import escape
root=pathlib.Path(__file__).resolve().parent
story=json.loads((root/'story.json').read_text())
assets=root/'assets'; assets.mkdir(exist_ok=True)
clips=[]; cues=[]
for i,line in enumerate(story['dialogue']):
    name=f'line{i}.wav'
    path=assets/name
    subprocess.run(['espeak-ng','-v','en-us+m3' if line['speaker']=='boss' else 'en-us+m1','-p','30' if line['speaker']=='boss' else '65','-s','165','-w',str(path),line['text']],check=True)
    with wave.open(str(path),'rb') as w:
        rate=w.getframerate(); samples=struct.unpack('<'+'h'*w.getnframes(),w.readframes(w.getnframes()))
    duration=len(samples)/rate
    assert duration <= line['end']-line['start'], (line,duration)
    clips.append(f'<audio id="audio{i}" class="clip" src="assets/{name}" data-start="{line["start"]}" data-duration="{duration}" data-track-index="2"></audio>')
    # Audio-envelope mouth movement, not phoneme-accurate lip sync.
    for j in range(0,len(samples),rate//12):
        part=samples[j:j+rate//12]
        rms=math.sqrt(sum(x*x for x in part)/len(part))
        cues.append([line['speaker'],line['start']+j/rate, max(0.12,min(1,rms/3000))])
    cues.append([line['speaker'],line['start']+duration,0.12])
    clips.append(f'<div id="caption{i}" class="clip caption" data-start="{line["start"]}" data-duration="{duration}" data-track-index="3">{escape(line["text"])}</div>')
template=(root/'template.html').read_text()
(root/'index.html').write_text(template.replace('<!-- MEDIA -->','\n'.join(clips)).replace('/* CUES */',json.dumps(cues)),encoding='utf-8')
print('Prepared',len(story['dialogue']),'voice clips and',len(cues),'mouth cues')
