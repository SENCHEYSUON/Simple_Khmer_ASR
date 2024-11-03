import os
import requests
import re
import shutil  
import csv  
import progressbar  
import time 

directory_path = r"D:\Intern\Khmer_Asr\Khmer_ASR_Dataset\LJ_Format\RFI_Not\RFI_Speech"
unk_folder = r"D:\Intern\Khmer_Asr\Khmer_ASR_Dataset\LJ_Format\RFI_Not\Unk"
one_word_folder = r"D:\Intern\Khmer_Asr\Khmer_ASR_Dataset\LJ_Format\RFI_Not\One"
Good = r"D:\Intern\Khmer_Asr\Khmer_ASR_Dataset\LJ_Format\RFI_Not\Good"

os.makedirs(unk_folder, exist_ok=True)
os.makedirs(one_word_folder, exist_ok=True)
os.makedirs(Good, exist_ok=True)


def extract_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group(1)) if match else None


filenames = [f for f in os.listdir(directory_path) if f.endswith('.flac')]
filenames.sort(key=extract_number)
total_files = len(filenames) 

progress_bar_style = [
    ' [', progressbar.Percentage(), '] ',
    progressbar.Bar(marker='\033[38;5;214m█\033[0m', left='', right=''),
    ' (', progressbar.SimpleProgress(), ') ', 
    ' (', progressbar.ETA(), ') ',
]

print("Transcribing and classifying files...")


progress = progressbar.ProgressBar(max_value=total_files, widgets=progress_bar_style).start()

with open(os.path.join(unk_folder, "unk_transcriptions.tsv"), 'w', encoding='utf-8') as unk_tsv, \
     open(os.path.join(one_word_folder, "one_word_transcriptions.tsv"), 'w', encoding='utf-8') as one_word_tsv, \
     open(os.path.join(Good, "others_transcriptions.tsv"), 'w', encoding='utf-8') as others_tsv:
    
    unk_writer = csv.writer(unk_tsv, delimiter='\t')
    one_word_writer = csv.writer(one_word_tsv, delimiter='\t')
    others_writer = csv.writer(others_tsv, delimiter='\t')
    
   
    unk_writer.writerow(["Filename", "TranscribedText"])
    one_word_writer.writerow(["Filename", "TranscribedText"])
    others_writer.writerow(["Filename", "TranscribedText"])

 
    for index, filename in enumerate(filenames, start=1):
        file_path = os.path.join(directory_path, filename)
        
      
        with open(file_path, "rb") as file:
            files = {"file": file}
            res = requests.post("http://188.245.75.254:8001/speech-to-text", files=files)
            base_filename = os.path.splitext(filename)[0]
            text = res.json()['text'].replace(':', '').replace(',', '')

       
        time.sleep(0.1)

       
        if 'UNK' in text:
            
            shutil.move(file_path, os.path.join(unk_folder, filename))
            unk_writer.writerow([base_filename, text])
        
        
        elif len(text.split()) == 1:
           
            shutil.move(file_path, os.path.join(one_word_folder, filename))
            one_word_writer.writerow([base_filename, text])
        
        
        else:
            
            shutil.move(file_path, os.path.join(Good, filename))
            others_writer.writerow([base_filename, text])

        
        progress.update(index)

progress.finish()
print("Classification completed. Files have been moved to their respective folders.")
