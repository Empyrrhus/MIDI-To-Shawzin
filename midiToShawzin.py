#Created by Empyrrhus

import sys
import mido
from mido import MidiFile
from conversion import ShawzinConversion
from conversion import identifyNote
from conversion import condenser
from conversion import widthFinder

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
			tempo = int(str(msg)[30:-8])
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
			secondsPast += outputNote[1] #actually half of real value, so "slow playback" can be used to double song length
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
		#print("Run " + str(counter))
		outputString = condenser(outputString)
		
	#break up song to fit copy-paste limit
		#10 lines, 79 units each; see letterWidthDict in conversion.py
	notesWidth = 0.0 #current width of the line, cannot exceed 79
	lineNumber = 1
	for note in outputString:
		#if note would overflow last line, make new song
		if(lineNumber == 10 and (notesWidth + widthFinder(note)) > maxLineWidth):
			lineNumber = 1
			notesWidth = widthFinder(str(scale))
			f.write("\n" + str(scale))
		#check if each character would overflow each line
		for character in range(0, len(note)):
			notesWidth += widthFinder(note[character])
			if(notesWidth > maxLineWidth or note.count("\n")):
				notesWidth = 0.0
				if(lineNumber == 10):
					lineNumber = 0
					f.write("\n" + str(scale))
					notesWidth += widthFinder(str(scale))
				notesWidth += widthFinder(note[character])
				lineNumber += 1
			f.write(note[character])
	f.close()
	f2.close()
print("\nDone. Press enter to exit.")
input()