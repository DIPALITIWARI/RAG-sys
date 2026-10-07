#converts the videos into mp3
import os
import subprocess

files = os.listdir("dataset")

for file in files:

    if file == ".DS_Store":
        continue
    tutorial_number = file.split(" [")[0].split(" #")[1]
    file_name=file.split(" ｜")[0]
    print( file_name,'-',tutorial_number)
    subprocess.run(["ffmpeg","-i",f"dataset/{file}",f'audios/{tutorial_number}_{file_name}.mp3'])