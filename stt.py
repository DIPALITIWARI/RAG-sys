#speech to text
import whisper
import json 
model = whisper.load_model("large-v2")
result = model.transcribe(audio="first10.mp3",language="hi",task="translate")
#print(result['segments'])
chunks=[]
for segment in result['segments']:
    chunks.append({'start':segment['start'],'end':segment['end'],'id':segment['id'],'text':segment['text']})

print(chunks)
with open("output1.json","w")as f:
    json.dump(chunks,f)    