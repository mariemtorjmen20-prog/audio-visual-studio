# HyperFrames workplace satire pilot

A 20-second, 720 × 1280 talking cartoon with two English synthetic voices.
The default pilot uses SVG artwork. An optional PNG cast can use supplied
character images with small movements timed to the audio.

## From character images to a video

1. Put two transparent PNGs in `pilot/characters/` and point the two slots in
   `cast.json` to those filenames. Keep personal images and their renders in a
   local checkout or a private GitHub repository. The manifest uses the
   `boss` and `employee` slots:

   ```json
   {
     "boss": {"name": "Manager", "image": "manager.png"},
     "employee": {"name": "Worker", "image": "worker.png"}
   }
   ```
2. In ChatGPT, attach the same PNGs, the cast manifest and a sample screenplay.
   Ask for three pitches grounded in visible details from both images, with a
   psychological tension, a reversal and a punchline in each pitch. Choose one
   before asking for a timed screenplay.
3. Save the chosen screenplay as `pilot/story.json`. Use the existing keys and
   slot IDs for dialogue. Keep the total runtime at 20 seconds and make each spoken line short
   enough to fit its time window. The scene template is the
   office and wheel setup, so a story that needs different props also needs a
   template edit.
4. A push to `agentgpt-hyperframes-workplace-satire` starts the existing
   GitHub Actions workflow.
   Open **Actions → HyperFrames talking cartoon pilot → latest successful run**
   and download **talking-cartoon-pilot**. Unzip it and open `final.mp4`. The
   included `qa.json` records the input image paths and checksums, plus video
   dimensions, duration and audio stream.

Story suggestions and selection take place in ChatGPT. GitHub Actions renders
the saved screenplay with eSpeak NG, HyperFrames, GSAP and FFmpeg. It also
uploads **recovery-diagnostics** when a run fails.

## Windows reproduction

Install Python 3, Node 22+, FFmpeg with ffprobe and eSpeak NG, and make sure
they are on PATH. From the repository root, run:

```powershell
cd pilot
python recovery.py
```

Open `pilot/final.mp4` from the repository root after QA passes. The HyperFrames
CLI and GSAP CDN need internet access. GitHub's technical checks verify the
file and cast inputs. Visual review takes place by watching the exported MP4.

## Recovery worker

The worker retries recognized transient errors up to three attempts. If lint
finds duplicate compositions, the worker removes the obsolete template only
when its contents match the current template. Unknown errors and QA failures
stop the run.
