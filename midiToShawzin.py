#Created by Empyrrhus

import sys
import mido
from mido import MidiFile
from conversion import ShawzinConversion
from conversion import identifyNote
from conversion import condenser
from conversion import offsetNote
from conversion import scrubName

maxNotes = 1666
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

keepOffset = 0
for current in sys.argv:
	if(current == "-keepOffset"):
		keepOffset = 1



#MIDI file attributes
ticksPerBeat = defaultTicksPerBeat
tempo = defaultTempo

#parse each MIDI track
for i, track in enumerate(mid.tracks):
	outputString = []
	notesIgnored = 0
	notesPast = 0
	trueNotesPast = 0
	secondsPast = 0
	trueSecondsPast = 0
	offset = 0
	
	#create text file
	trackName = scrubName(sys.argv[1] + ' - Track {} - {}'.format(i + 1, track.name))
	f = open(trackName + ".txt", "w")
	f2 = open(trackName + " - DEBUG.txt", "w")
	outputString.append(str(scale))
	
	#parse MIDI
	for msg in track:
		try:
			f2.write("\t" + str(msg))
		except:
			pass #prevent UnicodeEncodeError in rare cases
		if(str(msg).count("time_signature")):
			timeSignature = [str(s) for s in str(msg).replace("=", " ").split(" ")]
			ticksPerBeat = int(timeSignature[timeSignature.index("clocks_per_click") + 1]) * int(timeSignature[timeSignature.index("notated_32nd_notes_per_beat") + 1])
		if(str(msg).count("set_tempo")):
			tempoMessage = [str(s) for s in str(msg).replace("=", " ").split(" ")]
			tempo = int(int(tempoMessage[tempoMessage.index("tempo") + 1]) / playbackSpeed)
		if(str(msg).count("time=")):
			currentNote = [int(s) for s in str(msg).replace("=", " ").replace(">", " ").split(" ") if s.isdigit()]
			outputNote = ShawzinConversion(scale, currentNote, secondsPast, ticksPerBeat, tempo)
			if(str(msg).count("note_on")):
				f2.write("\n")
				if(outputNote[0][0] is not "A"):
					outputString.append(outputNote[0])
					notesPast += 1
					trueNotesPast += 1
					f2.write("#" + str(trueNotesPast))
				else:
					f2.write("(Ignored)\t" + "Note #" + str(trueNotesPast + 1))
					notesIgnored += 1
				f2.write("\t Note " + identifyNote(currentNote[1]) + str(int(currentNote[1]/12) - 1) + " at " + str(int((trueSecondsPast + 2*(outputNote[1]))/60)) + "m" + str((trueSecondsPast+ 2*(outputNote[1]))%60) + "s")
				
			#break up song to fit 256s limit
			secondsPast += outputNote[1]
			trueSecondsPast += 2*(outputNote[1])
			if(notesPast >= maxNotes or secondsPast >= maxLength):
				outputString.append("\n" + str(scale))
				notesPast = 0
				if(secondsPast >= maxLength or keepOffset == 0):
					secondsPast = 0
				offset = outputNote[0][1]
		f2.write("\n")	
		
	#print summary to console
	print("\nOutput to " + trackName)
	print("  Notes out of Scale: " + str(notesIgnored))
	if(notesIgnored):
		print("  Check \"" + trackName + " - DEBUG.txt\" for details.")
		
	#combine notes with shared frets
	for counter in range(0, 3):
		outputString = condenser(outputString)
		
	#output to file
	for note in outputString:
		f.write(note)
		
	f.close()
	f2.close()

#exit
print("\nDone. Press enter to exit.")
input()