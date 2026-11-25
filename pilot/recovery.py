"""Bounded rule-based recovery worker. Never bypass lint or verification."""
import pathlib, subprocess, sys, json, time, shutil, re, os
ROOT=pathlib.Path(__file__).resolve().parent
LOG=ROOT/'diagnostics'; LOG.mkdir(exist_ok=True)
NPX=shutil.which('npx.cmd' if os.name=='nt' else 'npx')
def run(stage,command):
    for attempt in range(1,4):
        try:
            p=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,errors='replace',timeout=480)
            output=p.stdout; code=p.returncode
        except subprocess.TimeoutExpired as e:
            output=str(e.stdout or '')+'\nTIMEOUT'; code=124
        (LOG/f'{stage}-{attempt}.log').write_text(output,encoding='utf-8')
        print(output,flush=True)
        event={'stage':stage,'attempt':attempt,'exit_code':code,'action':'pass' if code==0 else 'stop'}
        # Only repair the known obsolete template, never delete arbitrary compositions.
        old=ROOT/'template.html'; new=ROOT/'template.html.tpl'
        if code and stage=='lint' and 'multiple_root_compositions' in output and old.exists() and new.exists() and old.read_bytes()==new.read_bytes():
            if attempt<3:
                old.unlink(); event['action']='remove identical obsolete template and retry'
        elif code and attempt<3 and stage!='verify' and re.search(r'ECONNRESET|ETIMEDOUT|EAI_AGAIN|ERR_NETWORK_CHANGED|TIMEOUT',output,re.I):
            event['action']='retry transient error'
        with (LOG/'recovery.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(event)+'\n')
        if code==0:return
        if event['action']=='stop': raise SystemExit(code or 1)
        time.sleep(3*attempt)
def main():
    if not NPX: raise SystemExit('npx not found')
    for name in ('final.mp4','qa.json'):
        (ROOT/name).unlink(missing_ok=True)
    run('prepare',[sys.executable,'prepare.py'])
    run('lint',[NPX,'--yes','hyperframes','lint'])
    run('render',[NPX,'--yes','hyperframes','render','--output','final.mp4'])
    run('verify',[sys.executable,'verify.py'])
if __name__=='__main__':main()
