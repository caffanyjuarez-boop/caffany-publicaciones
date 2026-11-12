"""Recorta silencios largos de la voz (máx 0.3 s) y acelera 1.1x. Uso: recortar.py entrada.mp3 salida.wav"""
import re, subprocess, sys
src, dst = sys.argv[1], sys.argv[2]
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src]))
log = subprocess.run(["ffmpeg","-hide_banner","-i",src,"-af","silencedetect=noise=-38dB:d=0.25","-f","null","-"],capture_output=True,text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
keep, cur = [], 0.0
for s, e in zip(st, en):
    if s <= 0.05:  # silencio inicial: dejar 0.05
        cur = max(0, e - 0.05); continue
    cap = 0.30
    keep.append((cur, s + cap/2)); cur = e - cap/2
if len(st) > len(en):
    keep.append((cur, st[-1] + 0.15))
else:
    keep.append((cur, dur))
parts = "".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[p{i}];" for i,(a,b) in enumerate(keep))
fc = parts + "".join(f"[p{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=0:a=1,atempo=1.1,loudnorm=I=-16:TP=-1.5[o]"
subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",src,"-filter_complex",fc,"-map","[o]","-ar","44100",dst],check=True)
nd = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",dst]))
print(f"{src}: {dur:.2f}s -> {nd:.2f}s ({len(keep)} tramos)")
