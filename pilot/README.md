# HyperFrames workplace satire pilot
AgentGPT-generated prototype. Original SVG artwork; no uploaded reference footage reused.
20 seconds, 720x1280, two English synthetic voices. eSpeak NG is a deliberately
lightweight smoke-test voice backend; mouth motion follows audio amplitude, not true phonemes.
Natural Kokoro speech, Rhubarb cues, ComfyUI assets, independent visual review and
Remotion/Blender comparison are future integration work, not implemented here.

## Architecture
Human-selected idea -> screenplay JSON -> speech and mouth cues -> HyperFrames/GSAP
-> MP4 -> ffprobe acceptance checks -> GitHub Actions artifact.

## Windows reproduction
Install Python 3, Node 22+, FFmpeg/ffprobe and eSpeak NG; ensure all executables are on PATH.
From repository root, run:
```powershell
cd pilot
python prepare.py
npx --yes hyperframes lint
npx --yes hyperframes render --output final.mp4
python verify.py
```
The CLI is currently unpinned for discovery; pin a verified version before production.
The GSAP script is pinned but fetched from a CDN; vendor it for offline operation.
No GPU is required for speech generation. Keep one render job running at once.
GitHub Actions performs the technical test automatically on branch pushes.
Download the artifact from the Actions run. Technical verification does not certify
speech intelligibility, artwork quality or accurate lip sync.

## Recovery worker
Run `python recovery.py` from pilot. The worker retries recognized transient errors up to three attempts, removes only an identical obsolete template when lint detects duplicate roots, and stops on unknown or QA failures. Diagnostics are uploaded even on failure. This is deterministic recovery, not an autonomous LLM debugger. No main branch writes.
