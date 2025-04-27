# import required module
# pip install pydub
# pip install translate
# pip install SpeechRecognition
# pip install pipwin
# pipwin install pyaudio

'''
###===================
Audio files to text works for files below 10mb,
This module needs ffmpeg to run as it uses conversion techniques
The commented part of code is for spiliting the files over 1 minute mark but is not implemented
Google's Speech recognition only works for mono audio files
https://ffmpeg.org/download.html  == for ffmpeg
===================###
'''

from pydub import AudioSegment
import math
import os

# def __init__(self, folder, filename):
#         self.folder = folder
#         self.filename = filename
#         self.filepath = folder + '\\' + filename
#
#         self.audio = AudioSegment.from_wav(self.filepath)
#
#     def get_duration(self):
#         return self.audio.duration_seconds
#
#     def single_split(self, from_min, to_min, split_filename):
#         t1 = from_min * 60 * 1000
#         t2 = to_min * 60 * 1000
#         split_audio = self.audio[t1:t2]
#         split_audio.export(self.folder + '\\' + split_filename, format="wav")
#
#     def multiple_split(self, min_per_split):
#         total_mins = math.ceil(self.get_duration() / 60)
#         for i in range(0, total_mins, min_per_split):
#             split_fn = str(i) + '_' + self.filename
#             self.single_split(i, i+min_per_split, split_fn)
#             print(str(i) + ' Done')
#             if i == total_mins - min_per_split:
#                 print('All splited successfully')

import speech_recognition as sr
from os import path
from pydub import AudioSegment

def voice_text(file):
	''''
	parameters location of folder (excluding the file name) and file_name
	'''
	# print(file,file_name)
	if file_name.endswith(".mp3"):
		input_file = file_name
		output_file = "result.wav"
		sound = AudioSegment.from_mp3(input_file)
		sound.export(output_file, format="wav")
		file=file.replace(file_name,'result.wav')
		file_name=file_name.replace(file_name,'result.wav')

	# sound = AudioSegment.from_wav(file_name)
	# sound = sound.set_channels(1)
	# sound.export(file, format="wav")

	# print(file,file_name)
	r = sr.Recognizer()
	s=[]
	with sr.AudioFile(file_name) as source:
		audio = r.listen(source)
		text = r.recognize_google(audio,  language='hi-IN')
	s+=text.split()
	return s

	# folder =file_name+'//audio_split'
	# f = os.path.join(file_name,'audio_split')
	# os.mkdir(f)
	# file =file
	# split_wav = SplitWavAudioMubin(folder, file)
	# split_wav.multiple_split(min_per_split=0.5)
	# s=[]
	# for filename in os.listdir(folder):
	# 	# f = os.path.join(file)
	# 	# os.mkdir(f)
	# 	if os.path.isfile(file):
	# 		audio = r.listen(source)
	# 		text = r.recognize_google(audio,  language='hi-IN')
	# 		s+=text.split()
	# shutil.rmtree(directory)
	# return s

# print(voice_text('','m.mp3'))
