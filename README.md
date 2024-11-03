# Simple Khmer ASR Project

This repository contains a simple Khmer Automatic Speech Recognition (ASR) project from scratch. Feel free to fork this repository, submit pull requests, or send us suggestions on what should be improved! I just do it for fun and celebrating my bd :D

## 1. Data Collection and Preprocessing

### Data Collection

- **YouTube Videos**
  - We crawl YouTube videos using `yt_dlp` and `ffmpeg`.
  - **Instructions**: Just follow the links to download the tools and refer to the given channel names for crawling.
  - **yt_dlp**: [Download yt_dlp](https://github.com/yt-dlp/yt-dlp)
  - **ffmpeg**: [Download ffmpeg](https://www.ffmpeg.org/)
  
- **OpenSLR Dataset**
  - Alternatively, you can use the OpenSLR dataset, which is open-source.
  - [OpenSLR Dataset Link](https://www.openslr.org/42/)

### Data Cleaning

- **Background Noise Removal**
  - We use Ultimate Vocal Remover for background noise removal.
  - [Ultimate Vocal Remover](https://ultimatevocalremover.com/)
  - Separate code and model's files are provided in the folder `Background_Noise`.

- **Chunking**
  - Automated chunking is performed using Python. For non-stratified results, manual checking with Audacity is recommended.
  - [Download Audacity](https://www.audacityteam.org/)

### 2. Transcription

- **Transcribe_New.py**
  - The script outputs three folders: `1_word`, `UNK` (unknown), and `non-transcript`.
  - Manual checking is recommended for perfect transcription accuracy.

## 3. Data Training

### Wav2Vec2

- **About Wav2Vec2**
  - Wav2Vec2 is a state-of-the-art model developed by Facebook AI (now Meta AI) for ASR. It converts raw audio waveforms into meaningful text.
  - ![Wav2Vec2 Model](https://lh3.googleusercontent.com/0eXW1sKIjJi_peKvr2eUAjH5CX03RbB-ct7IBSUFhH1cSx481Be7_xdVRAJ3UfxBAwSlT-KON18ZwipgGtivI7roEjacmD4Cm5jWlJBdrWz6DOabDtO5ynX65Id8vkNhnAgh_uYO)
  - The model was trained using connectionist temporal classification (CTC), so the output has to be decoded using `Wav2Vec2CTCTokenizer`.

### Metrics

- **WER (Word Error Rate)**
  - WER is a metric used to evaluate the quality of transcriptions produced by ASR systems.
  - ![Word Error Rate](https://sonix.ai/packs/media/images/corp/articles/word-error-rate-2017-c5aba7282b39531154f5676a184c7ec4.png)
  - In many applications, it is of interest to estimate WER given a pair of a speech utterance and a transcript.

## 4. Simple StreamLit Application

- This application records voice or inputs a file and returns the transcript text!

## References

- [LJ Speech Dataset](https://keithito.com/LJ-Speech-Dataset/)
- [Wav2Vec2 on Hugging Face](https://huggingface.co/docs/transformers/en/model_doc/wav2vec2)
- [OpenSLR Resource](https://www.openslr.org/resources/42)
- [Wav2Vec2 Khmer Model](https://github.com/seanghay/wav2vec2-khmer-openslr)
- [Separate Model](https://github.com/TRvlvr/model_repo/releases/tag/all_public_uvr_models)
