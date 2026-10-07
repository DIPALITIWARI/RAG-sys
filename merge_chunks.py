import os
import json
import math
n=5

for file in os.listdir('jsons'):
    if file.endswith('.json'):
        file_path=os.path.join('jsons', file)
        with open(file_path, 'r') as f:
            data = json.load(f)
            # print(len(data['chunks'])," ------- ")
            new_chunks=[]
            num_chunks=len(data['chunks'])
            num_grp=math.ceil(num_chunks/n)
            for i in range(num_grp):
                start=i*n
                end=min((i+1)*n,num_chunks)
                chunk_grp=data['chunks'][start:end]
                new_chunks.append(
                    {"number":data['chunks'][0]['no'],
                    "title":chunk_grp[0]['title'],
                    "start":chunk_grp[0]['start'],
                    "end":chunk_grp[-1]['end'],
                    "text":''.join([chunk['text'] for chunk in chunk_grp])

                })
                os.makedirs('merged_jsons', exist_ok=True)
                with open(os.path.join('merged_jsons', f'merged_{file}'), 'w') as f:
                    json.dump(new_chunks, f, indent=4)



