import os
import whisper
import json 
model = whisper.load_model("large-v2")

audios=os.listdir("audios")
for audio in audios:
    #print(audio)
    if not audio.endswith(".mp3"):
        continue
    number=audio.split("_")[0]
    title=audio.split("_")[1][:-4]
    print(number ," - " ,title)
    result = model.transcribe(audio=f"audios/{audio}",language="hi",task="translate")

    chunks=[]
    for segment in result['segments']:
       chunks.append({'no':number,'title':title,'start':segment['start'],'end':segment['end'],'id':segment['id'],'text':segment['text']})
    chunks_with_metadata={"chunks":chunks,"text":result['text']}
    print(chunks)
    with open(f"jsons/{audio}.json","w")as f:
        json.dump(chunks_with_metadata,f)    