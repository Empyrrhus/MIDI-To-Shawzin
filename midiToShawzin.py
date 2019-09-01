#Created by Empyrrhus

import sys
import mido
from mido import MidiFile
from conversion import ShawzinConversion
from conversion import identifyNote
from conversion import condenser
from conversion import widthFinder
from conversion import offsetNote

maxNotes = 107
maxLineWidth = 79.5 #varies between 79-80, alternates every line?
maxLength = 256
defaultTicksPerBeat = 480
defaultTempo = 500000

#read midi file from command line
if(len(sys.argv) == 1):
	print("To convert a MIDI, drag the MIDI file onto this executable, or add a MIDI file as a command line argument.")
	input()
	sys.exit()
	
mid = MidiFile(sys.argv[1])

#get song scale from user
print("\nEnter the song's musical scale.\nYou can use a tool such as scales-chords.com/scalefinder.php.\nIf you have problems getting your MIDI into scale, use Chromatic.\n")
print("Scales:\n  1. Pentatonic Minor\n  2. Pentatonic Major\n  3. Chromatic\n  4. Hexatonic\n  5. Major\n  6. Minor\n  7. Hirajoshi\n  8. Phrygian\n\nEnter Scale:")
scale = 0
while True:
	scale = input()
	try:
		scale = int(scale)
		if(0 < scale and scale <= 8):
			break
	except:
		pass
	print("Please enter a valid number from 1-8.")
	
#other settings
playbackSpeed = 1.0
print("\nEnter a playback speed modifier.\n(1 is default, 2 is double speed, 0.5 is half speed, etc.)\n\nEnter Playback Speed:")
while True:
	playbackSpeed = input()
	try:
		playbackSpeed = float(playbackSpeed)
		if(0 < playbackSpeed):
			break
	except:
		pass
	print("Please enter a valid positive number.")
	
removeOffset = 1
print("\nDo you want to keep or remove song offsets?\n  MIDI:\n\t1\t2\t3\t4\n\tA\tB\tC\tD\n  1. Keep Offset\n\t1\t2\t3\t4\n\tA\tB\n\t\t\tC\tD\n  2. Remove Offset\n\t1\t2\t3\t4\n\tA\tB\n\tC\tD\n\nEnter option:")
while True:
	removeOffset = input()
	try:
		removeOffset = int(removeOffset)
		if(0 < removeOffset and removeOffset <= 2):
			break
	except:
		pass
	print("Please enter a valid number from 1-2.")

#MIDI file attributes
ticksPerBeat = defaultTicksPerBeat
tempo = defaultTempo

#parse each MIDI track
for i, track in enumerate(mid.tracks):
	outputString = []
	notesIgnored = 0
	trueNotesPast = 0
	secondsPast = 0
	trueSecondsPast = 0
	
	#create text file
	trackName = sys.argv[1] + ' - Track {} - {}'.format(i + 1, track.name)
	f = open(trackName + ".txt", "w")
	f2 = open(trackName + " - DEBUG.txt", "w")
	outputString.append(str(scale))
	
	#parse MIDI
	for msg in track:
		f2.write("\t" + str(msg))
		if(str(msg).count("time_signature")):
			timeSignature = [int(s) for s in str(msg).replace("=", " ").split(" ") if s.isdigit()]
			ticksPerBeat = timeSignature[2] * timeSignature[3]
		if(str(msg).count("set_tempo")):
			tempo = int(int(str(msg)[30:-8]) / playbackSpeed)
		if(str(msg).count("time=")):
			currentNote = [int(s) for s in str(msg).replace("=", " ").replace(">", " ").split(" ") if s.isdigit()]
			outputNote = ShawzinConversion(scale, currentNote, secondsPast, ticksPerBeat, tempo)
			if(str(msg).count("note_on")):
				f2.write("\n")
				if(outputNote[0][0] is not "A"):
					outputString.append(outputNote[0])
					trueNotesPast += 1
					f2.write("#" + str(trueNotesPast))
				else:
					f2.write("(Ignored)\t" + "Note #" + str(trueNotesPast + 1))
					notesIgnored += 1
				f2.write("\t Note " + identifyNote(currentNote[1]) + str(int(currentNote[1]/12) - 1) + " at " + str(int((trueSecondsPast + 2*(outputNote[1]))/60)) + "m" + str((trueSecondsPast+ 2*(outputNote[1]))%60) + "s")
				
			#break up song to fit 256s limit
			secondsPast += outputNote[1]
			trueSecondsPast += 2*(outputNote[1])
			if(secondsPast >= maxLength):
				outputString.append("\n" + str(scale))
				secondsPast = 0
		f2.write("\n")	
		
	#print summary to console
	print("\nOutput to " + trackName)
	print("  Notes out of Scale: " + str(notesIgnored))
	if(notesIgnored):
		print("  Check \"" + trackName + " - DEBUG.txt\" for details.")
		
	#combine notes with shared frets
	for counter in range(0, 3):
		outputString = condenser(outputString)
		
	#break up song to fit copy-paste limit
		#10 lines, 79 units each; see letterWidthDict in conversion.py
	notesWidth = 0.0 #current width of the line, cannot exceed 79
	lineNumber = 1
	finalOutputString = []
	noSilenceString = []
	
	#variables for removing silence
	timeOffset = 0
	offsetFlag = 1
			
	#parse track song notes in shawzin format
	for note in outputString:
		#if note would overflow last line, make new song part
		currentNoteWidth = 0
		if(len(note) == 3 and removeOffset == 2):
			currentNoteWidth = widthFinder(note[0] + offsetNote(note[1], timeOffset) + note[2])
		else:
			currentNoteWidth = widthFinder(note)
		if(lineNumber == 10 and (notesWidth + currentNoteWidth) > maxLineWidth):
			lineNumber = 1
			notesWidth = widthFinder(str(scale))
			finalOutputString.append("\n" + str(scale))
			offsetFlag = 1

		#for removing silence at beginning of track
		if(len(note) == 3 and offsetFlag and removeOffset == 2):
			timeOffset = note[1]
			offsetFlag = 0
			
		#check if each character would overflow each line
		for character in range(0, len(note)):
			if(character == 1 and removeOffset == 2):
				notesWidth += widthFinder(offsetNote(note[character], timeOffset))
			else:
				notesWidth += widthFinder(note[character])
				
			#keep track and reset line width when next line is reached
			if(notesWidth > maxLineWidth or (note.count("\n") and removeOffset != 2)):
				notesWidth = 0.0 #reset current line width used
				
				#create a new song part if current part has hit the limit
				if(lineNumber == 10 or (note.count("\n") and removeOffset != 2)):
					lineNumber = 0
					notesWidth += widthFinder(str(scale))
					if(lineNumber == 10):
						finalOutputString.append("\n" + str(scale))
						if(removeOffset == 2):
							timeOffset = note[1]
					if(note.count("\n") and removeOffset == 2):
						offsetFlag = 1	
					
				#re-add character width since we reset
				if(character == 1 and removeOffset == 2):
					notesWidth += widthFinder(offsetNote(note[character], timeOffset))
				else:
					notesWidth += widthFinder(note[character])
				lineNumber += 1
			#add to output
			if(character == 1 and removeOffset == 2):
				finalOutputString.append(offsetNote(note[character], timeOffset))
			elif(note.count("\n") and removeOffset == 2):
				pass
			else:
				finalOutputString.append(note[character])
			
	#output to file
	for note in finalOutputString:
		f.write(note)
	f.close()
	f2.close()

#exit
print("\nDone. Press enter to exit.")
input()