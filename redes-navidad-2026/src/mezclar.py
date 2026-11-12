"""Mezcla voz + música + campanita en cada cambio de escena y la une al video mudo.
Uso: python3 -I mezclar.py <video> [musica.mp3]
"""
import json, os, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = sys.argv[1]
musica = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "audio", "musica_a.mp3")
meta = json.load(open(os.path.join(BASE, "html", "meta.json")))[n]
dur, cortes = meta["dur"], meta["cortes"]
fin = cortes[-1]                      # inicio de la tarjeta final: la música sube
sal = os.path.join(BASE, "salida")
campana = os.path.join(sal, "campana.wav")
if not os.path.exists(campana):
    # campanita suave: dos senos con decaimiento exponencial
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "aevalsrc='0.5*sin(2*PI*1568*t)*exp(-6*t)+0.35*sin(2*PI*2349*t)*exp(-8*t)+0.2*sin(2*PI*3136*t)*exp(-10*t)':s=44100:d=0.9",
                    "-ac", "2", campana], check=True)

golpes = [c for c in cortes[1:]]
ins = ["-i", os.path.join(BASE, "audio", f"voz_{n}_final.wav"), "-stream_loop", "-1", "-i", musica]
for _ in golpes:
    ins += ["-i", campana]
fc = [f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur={dur}[v]",
      f"[2:a]atrim=0:{dur},asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,"
      f"volume='if(lt(t,{fin}),0.16,0.16+0.30*min((t-{fin})/0.6,1))':eval=frame,"
      f"afade=t=in:st=0:d=0.4,afade=t=out:st={dur - 1.6}:d=1.6[m]"]
mezcla = "[v][m]"
for k, g in enumerate(golpes):
    ms = int(g * 1000)
    fc.append(f"[{k + 3}:a]volume=0.10,adelay={ms}|{ms},apad=whole_dur={dur}[c{k}]")
    mezcla += f"[c{k}]"
fc.append(f"{mezcla}amix=inputs={2 + len(golpes)}:normalize=0:duration=first,atrim=0:{dur},alimiter=limit=0.95[a]")
mudo = os.path.join(sal, f"{n}_mudo.mp4")
out = os.path.join(sal, f"caffany_{n}.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mudo] + ins +
               ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", out], check=True)
d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).decode().strip()
print(out, d)
