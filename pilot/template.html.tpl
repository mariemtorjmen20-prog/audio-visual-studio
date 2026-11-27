<!doctype html><html><head><meta charset="utf-8">
<style>
*{box-sizing:border-box}body{margin:0;background:#ead9b7}#stage{position:relative;width:720px;height:1280px;overflow:hidden;background:#ead9b7}svg{position:absolute;inset:0;width:100%;height:100%}.caption{position:absolute;left:40px;right:40px;bottom:85px;text-align:center;background:#30271f;color:#fff5db;padding:22px;border-radius:20px;font:bold 34px Arial,sans-serif}
</style><script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script></head><body>
<div id="stage" data-composition-id="main" data-start="0" data-duration="20" data-width="720" data-height="1280">
<svg viewBox="0 0 720 1280" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="paper" width="12" height="12" patternUnits="userSpaceOnUse"><path d="M0 2h3M7 9h2" stroke="#b49b77" opacity=".3"/></pattern></defs>
<rect width="720" height="1280" fill="url(#paper)"/><rect x="25" y="25" width="670" height="1230" rx="8" fill="none" stroke="#71563c" stroke-width="3"/>
<text x="360" y="100" text-anchor="middle" font-family="Georgia,serif" font-size="43" fill="#3f3025">ONE BIG FAMILY</text>
<path d="M60 130H660M60 1000H660" stroke="#71563c" stroke-width="3"/>
<!-- Separate wheel, limbs and mouths allow independent movement. -->
<g id="wheel" stroke="#795b3b" fill="none" stroke-width="12"><circle cx="460" cy="700" r="210"/><circle cx="460" cy="700" r="190"/><path d="M250 700h420M460 490v420M311 551l298 298M311 849l298-298"/></g>
<g id="employee" stroke="#533d30" stroke-width="5" stroke-linejoin="round">
<path id="leg1" d="M435 755l-45 85 45 22" fill="none" stroke-width="29" stroke-linecap="round"/><path id="leg2" d="M470 755l45 85-45 22" fill="none" stroke-width="29" stroke-linecap="round"/>
<path d="M411 660q45-35 83 0l-8 110h-78z" fill="#777f6a"/><path id="arm" d="M485 680l50 35 29-20" fill="none" stroke="#c38f79" stroke-width="21" stroke-linecap="round"/>
<ellipse cx="451" cy="606" rx="64" ry="69" fill="#d5a68a"/><path d="M401 580l-5-57 43 26M477 550l40-29-5 62" fill="#d5a68a"/><path d="M390 555q55-65 115-8l18 15H384z" fill="#696856"/>
<ellipse cx="483" cy="618" rx="35" ry="25" fill="#ba7b70"/><circle cx="474" cy="617" r="5"/><circle cx="493" cy="617" r="5"/><circle cx="459" cy="585" r="6" fill="#2e211b"/>
<ellipse id="employee-mouth" cx="466" cy="650" rx="19" ry="13" fill="#502b27"/>
</g>
<g id="boss" stroke="#533d30" stroke-width="5" stroke-linejoin="round">
<path d="M80 400q70-65 145 0l20 190H65z" fill="#64513f"/><path d="M122 370l32 90 37-90" fill="#f8edd7"/><path d="M154 430l-13 85 26-4z" fill="#a34f38"/>
<ellipse cx="155" cy="305" rx="81" ry="86" fill="#ac875e"/><ellipse cx="80" cy="282" rx="24" ry="52" fill="#78563d"/><ellipse cx="230" cy="282" rx="24" ry="52" fill="#78563d"/><ellipse cx="155" cy="337" rx="56" ry="42" fill="#d7bd98"/><ellipse cx="155" cy="312" rx="23" ry="14" fill="#3d2c22"/><circle cx="126" cy="279" r="8"/><circle cx="184" cy="279" r="8"/>
<ellipse id="boss-mouth" cx="155" cy="356" rx="28" ry="17" fill="#502b27"/>
<path id="gesture" d="M205 429l70-45 32 8" fill="none" stroke="#ac875e" stroke-width="25" stroke-linecap="round"/>
<rect x="45" y="545" width="245" height="100" rx="9" fill="#946b44"/><path d="M40 545h255" stroke-width="15"/>
</g>
<text x="100" y="190" font-family="Arial,sans-serif" font-size="23" fill="#57432e">THE BOSS</text><text x="430" y="970" font-family="Arial,sans-serif" font-size="23" fill="#57432e">THE WORKER</text>
</svg>
<!-- MEDIA -->
</div><script>
// HyperFrames seeks this paused timeline; no wall-clock animations.
window.__timelines=window.__timelines||{};
const tl=gsap.timeline({paused:true});
window.__timelines.main=tl;
tl.to('#wheel',{rotation:2160,transformOrigin:'50% 50%',duration:15,ease:'none'},0);
tl.to('#wheel',{rotation:2340,duration:3,ease:'power2.out'},15);
tl.to('#employee',{y:-10,duration:.22,yoyo:true,repeat:67,ease:'sine.inOut'},0);
tl.to('#leg1',{rotation:35,svgOrigin:'435 755',duration:.24,yoyo:true,repeat:61},0);
tl.to('#leg2',{rotation:-35,svgOrigin:'470 755',duration:.24,yoyo:true,repeat:61},0);
tl.to('#gesture',{rotation:22,svgOrigin:'205 429',duration:.5,yoyo:true,repeat:5},1);
tl.to('#boss',{y:-8,duration:.25,yoyo:true,repeat:7},11);
tl.set(['#boss-mouth','#employee-mouth'],{scaleY:.12,transformOrigin:'50% 50%'},0);
const cues=/* CUES */;
for(const [speaker,time,shape] of cues){tl.set('#'+speaker+'-mouth',{scaleY:shape},time);}
tl.to({}, {duration:20},0);
</script></body></html>