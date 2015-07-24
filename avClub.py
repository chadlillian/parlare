#!/home/chad/anaconda/bin/python

import	os
import	shlex
import	subprocess

class	avClub:
	def	runSubProc(self,args):
		fnull	=open(os.devnull,'w')
		p	=subprocess.Popen(args,stdout=fnull,stderr=fnull)
		p.communicate()
		fnull.close()
	
	def	concatenateAudio(self,files,outputfilename):
		files	='|'.join(files)
		command	='ffmpeg -i "concat:%s" -c copy %s'%(files,outputfilename)
		args	=['ffmpeg','-i','concat:%s'%(files), '-c', 'copy', outputfilename]
		self.runSubProc(args)
		
	def	makeTextImage(self,text,imageFileName):
		imagecmd	="convert -background blue -size 800x480 -fill \"#ffffff\" -pointsize 72 -gravity center label:XXX "+imageFileName
		args		=shlex.split(imagecmd)
		args[11]	='label:'+text+''
		self.runSubProc(args)

	def	makeTextSoundToVideo(self,*positional, **keywords):
		if 'text' not in keywords.keys():
			text	='\n'
		else:
			text=keywords['text']
		self.makeTextImage(text,'temp.png')
	
		if 'duration' in keywords.keys():
			self.makeAudioPause(keywords['duration'])
			soundfile	='silence.mp3'
		else:
			soundfile	=keywords['soundfile']

		if 'videofile' in keywords.keys():
			videofile	=keywords['videofile']
		else:
			videofile	='temp.mp4'

		if os.path.exists(videofile):
			os.remove(videofile)
			
		videocmd	="ffmpeg -loop 1 -i temp.png -i XXX -c:v libx264 -c:a copy -shortest XXX"
		args		=shlex.split(videocmd)
		args[6]		=soundfile
		args[-1]	=videofile
		self.runSubProc(args)

		os.remove('temp.png')
		if soundfile=='silence.mp3':
			os.remove('silence.mp3')
	
	def	makeVideoPause(self,pauselen):
		if os.path.exists('silence.mp4'):
			os.remove('silence.mp4')
		cmd		="ffmpeg -f lavfi -i color=c=blue:s=800x480:d=%f  silence.mp4"%(pauselen)
		args	=shlex.split(cmd)
		self.runSubProc(args)

	def	makeAudioPause(self,pauselen):
		if os.path.exists('silence.mp3'):
			os.remove('silence.mp3')
		args	=['ffmpeg', '-filter_complex','aevalsrc=0', '-t', '%i'%(pauselen), 'silence.mp3']
		self.runSubProc(args)
	
	def	concatenateVideo(self,videofiles,videooutput):
		tempfile	='.inputs'
		output	=open(tempfile,'w')
		for f in videofiles:
			line	="file '%s'\n"%(f)
			output.write(line.encode('utf8'))
		output.close()
		command	='ffmpeg -f concat -i inputs.txt -c copy %s'%(videooutput)
		args	=['ffmpeg','-f','concat','-i',tempfile,'-c', 'copy', videooutput]
		self.runSubProc(args)

		os.remove(tempfile)
		
	def	concatenateAudio(self,files,outputfilename):
		files	='|'.join(files)
		command	='ffmpeg -i "concat:%s" -c copy %s'%(files,outputfilename)
		args	=['ffmpeg','-i','concat:%s'%(files), '-c', 'copy', outputfilename]
		self.runSubProc(args)

if __name__=="__main__":
	a	=avClub()
	a.makeTextSoundToVideo(text='Hello',duration=3,videofile='output.mp4')
	a.makeTextSoundToVideo(text='Hello',soundfile='audio/german_nouns/das_Weh.mp3',videofile='test.mp4')
