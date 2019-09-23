#Created by Empyrrhus

import sys
import mido
from mido import MidiFile
from conversion import ShawzinConversion
from conversion import identifyNote
from conversion import condenser
from conversion import offsetNote
from conversion import scrubName
from conversion import identifyTime

maxNotes = 1666
maxLength = 256
defaultTicksPerBeat = 200
defaultTempo = 800000

#read midi file from command line or input
midname = ""
mid = ""
if(len(sys.argv) == 1):
	print("To convert a MIDI, drag the MIDI file onto this executable, add a MIDI file as a command line argument, or enter the MIDI filepath below.")
	midname = input()
	try:
		mid = MidiFile(midname)
	except FileNotFoundError:
		sys.exit()
else:
	try:
		midname = sys.argv[1]
		mid = MidiFile(sys.argv[1])
	except FileNotFoundError:
		print("Please enter a valid MIDI file as an argument.")
		sys.exit()

#get song scale from user
print("\nEnter the song's musical scale.\nYou can use a tool such as scales-chords.com/scalefinder.php.\nIf you have problems getting your MIDI into scale, use Chromatic.\n")
print("Scales:\n  1. Pentatonic Minor\n  2. Pentatonic Major\n  3. Chromatic\n  4. Hexatonic\n  5. Major\n  6. Minor\n  7. Hirajoshi\n  8. Phrygian\n  9. Yo\n\nEnter Scale:")
scale = 0
while True:
	scale = input()
	try:
		scale = int(scale)
		if(0 < scale and scale <= 9):
			break
	except:
		pass
	print("Please enter a valid number from 1-9.")
	
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
tempo = defaultTempo / playbackSpeed

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
	trackNameFromFile = ""
	if(track.name == "\0"):
		trackNameFromFile = ""
	else:
		trackNameFromFile = track.name
	trackName = midname + ' - Track {} - {}'.format(i + 1, scrubName(trackNameFromFile))
	
	f = open(trackName + ".txt", "w")
	f2 = ""
	if(trackName.count('\\')):
		f2 = open(trackName[:trackName.rfind('\\') + 1] + "DEBUG - " + trackName[trackName.rfind('\\') + 1:] + ".txt", "w")
	else:
		f2 = open("DEBUG - " + trackName + ".txt", "w")
	outputString.append(str(scale))
	
	#parse MIDI
	for msg in track:
		try:
			f2.write("\t" + str(msg))
		except:
			pass #prevent UnicodeEncodeError in rare cases

		#parse MIDI parameters
		if(str(msg).count("time_signature")):
			timeSignature = [str(s) for s in str(msg).replace("=", " ").split(" ")]
			ticksPerBeat = int(timeSignature[timeSignature.index("clocks_per_click") + 1]) * int(timeSignature[timeSignature.index("notated_32nd_notes_per_beat") + 1])
			f2.write("\nTicks per Beat = " + str(ticksPerBeat))
		if(str(msg).count("set_tempo")):
			tempoMessage = [str(s) for s in str(msg).replace("=", " ").split(" ")]
			tempo = int(int(tempoMessage[tempoMessage.index("tempo") + 1]) / playbackSpeed)
			f2.write("\nTempo = " + str(tempo))
		if(str(msg).count("time=")):
			#break up song to fit 256s limit
			if(notesPast >= maxNotes - 1 or secondsPast >= maxLength - 1):
				outputString.append("\n" + str(scale))
				notesPast = 0
				if(secondsPast >= maxLength or keepOffset == 0):
					secondsPast = 0
				offset = outputNote[0][1]

			#parse MIDI message
			currentNote = [int(s) for s in str(msg).replace("=", " ").replace(">", " ").split(" ") if s.isdigit()]
			outputNote = ShawzinConversion(scale, currentNote, secondsPast, ticksPerBeat, tempo)
			
			#parse notes
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
			
			#keep track of progress
			secondsPast += outputNote[1]
			trueSecondsPast += 2*(outputNote[1])
		f2.write("\n")	
		
	#combine notes with shared frets
	for counter in range(0, 3):
		outputString = condenser(outputString)
		
	#remove impossible notes & output to file
	numberOfImpossibleNotes = 0
	lastNoteTime = "AA"
	for note in outputString:
		if(len(note) == 3 and note[1:3] == lastNoteTime):
			numberOfImpossibleNotes += 1
			f2.write("(Impossible)\t Note at " + identifyTime(note) + "\n")
			continue
		lastNoteTime = note[1:3]
		f.write(note)
		
	#print summary to console
	print("\nOutput to " + trackName)
	print("\tNotes out of Scale: " + str(notesIgnored))
	print("\tImpossible Notes: " + str(numberOfImpossibleNotes))
	if(notesIgnored or numberOfImpossibleNotes):
		print("\tCheck \"" + trackName + " - DEBUG.txt\" for details.")
		
	f.close()
	f2.close()

#exit
print("\nDone. Press enter to exit.")
input()