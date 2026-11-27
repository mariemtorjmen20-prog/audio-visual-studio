<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>$title</title>
<style>
* { box-sizing: border-box; }
body { margin: 0; background: #ead9b7; }
#stage { position: relative; width: 720px; height: 1280px; overflow: hidden; background: #ead9b7; }
svg { position: absolute; inset: 0; width: 100%; height: 100%; }
h1 {
  position: absolute; top: 65px; left: 58px; right: 58px; margin: 0;
  color: #3f3025; text-align: center; font: bold 53px/1.05 Georgia, serif;
}
.character { position: absolute; object-fit: contain; }
#boss { width: 420px; height: 420px; left: -15px; top: 205px; }
#employee { width: 305px; height: 305px; left: 340px; top: 665px; }
.caption {
  position: absolute; left: 40px; right: 40px; bottom: 85px; text-align: center;
  background: #30271f; color: #fff5db; padding: 22px; border-radius: 20px;
  font: bold 34px Arial, sans-serif;
}
</style>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
</head>
<body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="20" data-width="720" data-height="1280">
  <svg viewBox="0 0 720 1280" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <defs>
      <pattern id="paper" width="12" height="12" patternUnits="userSpaceOnUse">
        <path d="M0 2h3M7 9h2" stroke="#b49b77" opacity=".3"/>
      </pattern>
    </defs>
    <rect width="720" height="1280" fill="url(#paper)"/>
    <rect x="25" y="25" width="670" height="1230" rx="8" fill="none" stroke="#71563c" stroke-width="3"/>
    <path d="M60 195H660M60 1015H660" stroke="#71563c" stroke-width="3"/>
    <g stroke="#795b3b" fill="none" stroke-width="8">
      <circle cx="490" cy="794" r="189"/>
      <circle cx="490" cy="794" r="175"/>
      <g id="wheel" opacity=".38">
        <path d="M316 794h348M490 620v348M367 671l246 246M367 917l246-246"/>
      </g>
    </g>
    <ellipse cx="195" cy="618" rx="126" ry="19" fill="#9d7953" opacity=".23"/>
  </svg>
  <h1>$title</h1>
  $characters
  $media
</div>
<script>
// HyperFrames seeks the paused timeline when it renders each frame.
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
window.__timelines.main = tl;
tl.to('#wheel', { rotation: 2160, svgOrigin: '490 794', duration: 15, ease: 'none' }, 0);
tl.to('#wheel', { rotation: 2340, duration: 3, ease: 'power2.out' }, 15);
tl.to('#employee', { x: -6, duration: 0.32, yoyo: true, repeat: 45, ease: 'sine.inOut' }, 0);

const cues = $cues;
for (const [speaker, time, strength] of cues) {
  tl.to('#' + speaker, { y: -12 * strength, duration: 0.08, ease: 'sine.out' }, time);
}
tl.to({}, { duration: 20 }, 0);
</script>
</body>
</html>
