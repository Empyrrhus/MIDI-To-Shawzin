import mido
from mido import MidiFile

secondsPerMeasure = 4
secondsPerTick = 0.0625
 
#base64 encoding
base64 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/"]

#Basic note order is BCE JKM RSU hik
scaleModulo = [36, 36, 12, 24, 24, 24, 36, 24]
pentatonicMinor = {
	0:"B", #C
	1:"A", #C#/Db
	2:"A", #D
	3:"C", #D#/Eb
	4:"A", #E
	5:"E", #F
	6:"A", #F#/Gb
	7:"J", #G
	8:"A", #G#/Ab
	9:"A", #A
	10:"K", #A#/Bb
	11:"A", #B
	12:"M", #C
	13:"A", #C#/Db
	14:"A", #D
	15:"R", #D#/Eb
	16:"A", #E
	17:"S", #F
	18:"A", #F#/Gb
	19:"U", #G
	20:"A", #G#/Ab
	21:"A", #A
	22:"h", #A#/Bb
	23:"A", #B
	24:"i", #C
	25:"A", #C#/Db
	26:"A", #D
	27:"k", #D#/Eb
	28:"A", #E
	29:"B", #F
	30:"A", #F#/Gb
	31:"C", #G
	32:"A", #G#/Ab
	33:"A", #A
	34:"E", #A#/Bb
	35:"A", #B
}
pentatonicMajor = {
	0:"B", #C
	1:"A", #C#/Db
	2:"C", #D
	3:"A", #D#/Eb
	4:"E", #E
	5:"A", #F
	6:"A", #F#/Gb
	7:"J", #G
	8:"A", #G#/Ab
	9:"K", #A
	10:"A", #A#/Bb
	11:"A", #B
	12:"M", #C
	13:"A", #C#/Db
	14:"R", #D
	15:"A", #D#/Eb
	16:"S", #E
	17:"A", #F
	18:"A", #F#/Gb
	19:"U", #G
	20:"A", #G#/Ab
	21:"h", #A
	22:"A", #A#/Bb
	23:"A", #B
	24:"i", #C
	25:"A", #C#/Db
	26:"k", #D
	27:"A", #D#/Eb
	28:"B", #E
	29:"A", #F
	30:"A", #F#/Gb
	31:"C", #G
	32:"A", #G#/Ab
	33:"E", #A
	34:"A", #A#/Bb
	35:"A", #B
}

chromatic = {
	0:"B", #C
	1:"C", #C#/Db
	2:"E", #D
	3:"J", #D#/Eb
	4:"K", #E
	5:"M", #F
	6:"R", #F#/Gb
	7:"S", #G
	8:"U", #G#/Ab
	9:"h", #A
	10:"i", #A#/Bb
	11:"k", #B
}

hexatonic = {
	0:"B", #C
	1:"A", #C#/Db
	2:"A", #D
	3:"C", #D#/Eb
	4:"A", #E
	5:"E", #F
	6:"J", #F#/Gb
	7:"K", #G
	8:"A", #G#/Ab
	9:"A", #A
	10:"M", #A#/Bb
	11:"A", #B
	12:"R", #C
	13:"A", #C#/Db
	14:"A", #D
	15:"S", #D#/Eb
	16:"A", #E
	17:"U", #F
	18:"h", #F#/Gb
	19:"i", #G
	20:"A", #G#/Ab
	21:"A", #A
	22:"k", #A#/Bb
	23:"A", #B
}

major = {
	0:"B", #C
	1:"A", #C#/Db
	2:"C", #D
	3:"A", #D#/Eb
	4:"E", #E
	5:"J", #F
	6:"A", #F#/Gb
	7:"K", #G
	8:"A", #G#/Ab
	9:"M", #A
	10:"A", #A#/Bb
	11:"R", #B
	12:"S", #C
	13:"A", #C#/Db
	14:"U", #D
	15:"A", #D#/Eb
	16:"h", #E
	17:"i", #F
	18:"A", #F#/Gb
	19:"k", #G
	20:"A", #G#/Ab
	21:"B", #A
	22:"A", #A#/Bb
	23:"C", #B
}

minor = {
	0:"B", #C
	1:"A", #C#/Db
	2:"C", #D
	3:"E", #D#/Eb
	4:"A", #E
	5:"J", #F
	6:"A", #F#/Gb
	7:"K", #G
	8:"M", #G#/Ab
	9:"A", #A
	10:"R", #A#/Bb
	11:"A", #B
	12:"S", #C
	13:"A", #C#/Db
	14:"U", #D
	15:"h", #D#/Eb
	16:"A", #E
	17:"i", #F
	18:"A", #F#/Gb
	19:"k", #G
	20:"B", #G#/Ab
	21:"A", #A
	22:"C", #A#/Bb
	23:"A", #B
}

hirajoshi = {
	0:"B", #C
	1:"C", #C#/Db
	2:"A", #D
	3:"A", #D#/Eb
	4:"A", #E
	5:"E", #F
	6:"J", #F#/Gb
	7:"A", #G
	8:"A", #G#/Ab
	9:"A", #A
	10:"K", #A#/Bb
	11:"A", #B
	12:"M", #C
	13:"R", #C#/Db
	14:"A", #D
	15:"A", #D#/Eb
	16:"A", #E
	17:"S", #F
	18:"U", #F#/Gb
	19:"A", #G
	20:"A", #G#/Ab
	21:"A", #A
	22:"h", #A#/Bb
	23:"A", #B
	24:"i", #C
	25:"k", #C#/Db
	26:"A", #D
	27:"A", #D#/Eb
	28:"A", #E
	29:"B", #F
	30:"A", #F#/Gb
	31:"A", #G
	32:"C", #G#/Ab
	33:"A", #A
	34:"E", #A#/Bb
	35:"A", #B
}

phrygian = {
	0:"B", #C
	1:"C", #C#/Db
	2:"A", #D
	3:"A", #D#/Eb
	4:"E", #E
	5:"J", #F
	6:"A", #F#/Gb
	7:"K", #G
	8:"M", #G#/Ab
	9:"A", #A
	10:"R", #A#/Bb
	11:"A", #B
	12:"S", #C
	13:"U", #C#/Db
	14:"A", #D
	15:"A", #D#/Eb
	16:"h", #E
	17:"i", #F
	18:"A", #F#/Gb
	19:"k", #G
	20:"B", #G#/Ab
	21:"A", #A
	22:"C", #A#/Bb
	23:"A", #B
}

scaleDict = {
	1:pentatonicMinor,
	2:pentatonicMajor,
	3:chromatic,
	4:hexatonic,
	5:major,
	6:minor,
	7:hirajoshi,
	8:phrygian,
}
 
def ShawzinConversion(scale, currentNote, secondsPast, ticksPerBeat, tempo):
	noteNumber = 0
	if(len(currentNote) >= 2):
		noteNumber = currentNote[1]
	ticksSinceLast = currentNote[len(currentNote) - 1]
	secondsSinceLast = mido.tick2second(ticksSinceLast, ticksPerBeat, tempo)
	return([noteConversion(scale, noteNumber) + timeConversion(secondsPast + secondsSinceLast), secondsSinceLast])

def noteConversion(scale, noteNumber):
	return scaleDict[scale][noteNumber%scaleModulo[scale - 1]]

def timeConversion(seconds):
	return(base64[int(seconds/secondsPerMeasure)%64] + base64[int((seconds%4)/secondsPerTick)%64])
	
#60 = C, +1 = +half step, -1 = -half step
noteDict = {
	0:"C",
	1:"C#/Db",
	2:"D",
	3:"D#/Eb",
	4:"E",
	5:"F",
	6:"F#/Gb",
	7:"G",
	8:"G#/Ab",
	9:"A",
	10:"A#/Bb",
	11:"B",
}

def identifyNote(note):
	return noteDict[note%12]

#certain simultaneous notes can be combined
chordDict = {
	#No Fret
	("B", "C"):"D",
	("C", "B"):"D",
	("B", "E"):"F",
	("E", "B"):"F",
	("C", "E"):"G",
	("E", "C"):"G",
	("D", "E"):"H",
	("E", "D"):"H",
	("F", "C"):"H",
	("C", "F"):"H",
	("G", "B"):"H",
	("B", "G"):"H",

	#Sky Fret
	("J", "K"):"L",
	("K", "J"):"L",
	("J", "M"):"N",
	("M", "J"):"N",
	("K", "M"):"O",
	("M", "K"):"O",
	("L", "M"):"P",
	("M", "L"):"P",
	("N", "K"):"P",
	("K", "N"):"P",
	("O", "J"):"P",
	("J", "O"):"P",

	#Earth Fret
	("R", "S"):"T",
	("S", "R"):"T",
	("R", "U"):"V",
	("U", "R"):"V",
	("S", "U"):"W",
	("U", "S"):"W",
	("T", "U"):"X",
	("U", "T"):"X",
	("V", "S"):"X",
	("S", "V"):"X",
	("W", "R"):"X",
	("R", "W"):"X",
	
	#Sky+Earth -> Sky/Earth Fret
	("J", "R"):"Z",
	("R", "J"):"Z",
	("K", "S"):"a",
	("S", "K"):"a",
	("L", "T"):"b",
	("T", "L"):"b",
	("M", "U"):"c",
	("U", "M"):"c",
	("N", "V"):"d",
	("V", "N"):"d",
	("O", "W"):"e",
	("W", "O"):"e",
	("P", "X"):"f",
	("X", "P"):"f",
	
	#Sky/Earth Fret
	("Z", "a"):"b",
	("a", "Z"):"b",
	("Z", "c"):"d",
	("c", "Z"):"d",
	("a", "c"):"e",
	("c", "a"):"e",
	("b", "c"):"f",
	("c", "b"):"f",
	("d", "a"):"f",
	("a", "d"):"f",
	("e", "Z"):"f",
	("Z", "e"):"f",
	
	#Water Fret
	("h", "i"):"j",
	("i", "h"):"j",
	("h", "k"):"l",
	("k", "h"):"l",
	("i", "k"):"m",
	("k", "i"):"m",
	("j", "k"):"n",
	("k", "j"):"n",
	("l", "i"):"n",
	("i", "l"):"n",
	("m", "h"):"n",
	("h", "m"):"n",

	#Sky/Earth + Water -> Sky/Earth/Water Fret
	("Z", "h"):"5",
	("h", "Z"):"5",
	("a", "i"):"6",
	("i", "a"):"6",
	("b", "j"):"7",
	("j", "b"):"7",
	("c", "k"):"8",
	("k", "c"):"8",
	("d", "l"):"9",
	("l", "d"):"9",
	("e", "m"):"+",
	("m", "e"):"+",
	("f", "n"):"/",
	("n", "f"):"/",
	
	#Sky+Water -> Sky/Water Fret
	("J", "h"):"p",
	("h", "j"):"p",
	("K", "i"):"q",
	("i", "K"):"q",
	("L", "j"):"r",
	("j", "L"):"r",
	("M", "k"):"s",
	("k", "M"):"s",
	("N", "l"):"t",
	("l", "N"):"t",
	("O", "m"):"u",
	("m", "O"):"u",
	("P", "n"):"v",
	("n", "P"):"v",
	
	#Sky/Water Fret
	("p", "q"):"r",
	("q", "p"):"r",
	("p", "s"):"t",
	("s", "p"):"t",
	("q", "s"):"u",
	("s", "q"):"u",
	("r", "s"):"v",
	("s", "r"):"v",
	("t", "q"):"v",
	("q", "t"):"v",
	("u", "p"):"v",
	("p", "u"):"v",
	
	#Sky/Water + Earth -> Sky/Earth/Water Fret
	("p", "R"):"5",
	("R", "p"):"5",
	("q", "S"):"6",
	("S", "q"):"6",
	("r", "T"):"7",
	("T", "r"):"7",
	("s", "U"):"8",
	("U", "s"):"8",
	("t", "V"):"9",
	("V", "t"):"9",
	("u", "W"):"+",
	("W", "u"):"+",
	("v", "X"):"/",
	("X", "v"):"/",
	
	#Earth+Water -> Earth/Water Fret
	("R", "h"):"x",
	("h", "R"):"x",
	("S", "i"):"y",
	("i", "S"):"y",
	("T", "j"):"z",
	("j", "T"):"z",
	("U", "k"):"0",
	("k", "U"):"0",
	("V", "l"):"1",
	("l", "V"):"1",
	("W", "m"):"2",
	("m", "W"):"2",
	("X", "n"):"3",
	("n", "X"):"3",
	
	#Earth/Water Fret	
	("x", "y"):"z",
	("y", "x"):"z",
	("x", "0"):"1",
	("0", "x"):"1",
	("y", "0"):"2",
	("0", "y"):"2",
	("z", "0"):"3",
	("0", "z"):"3",
	("1", "y"):"3",
	("y", "1"):"3",
	("2", "x"):"3",
	("x", "2"):"3",
	
	#Earth/Water + Sky -> Sky/Earth/Water Fret
	("x", "J"):"5",
	("J", "x"):"5",
	("y", "K"):"6",
	("K", "y"):"6",
	("z", "L"):"7",
	("L", "z"):"7",
	("0", "M"):"8",
	("M", "0"):"8",
	("1", "N"):"9",
	("N", "1"):"9",
	("2", "O"):"+",
	("O", "2"):"+",
	("3", "P"):"/",
	("P", "3"):"/",
	
	#Sky/Earth/Water Fret
	("5", "6"):"7",
	("6", "5"):"7",
	("5", "8"):"9",
	("8", "5"):"9",
	("6", "8"):"+",
	("8", "6"):"+",
	("7", "8"):"/",
	("8", "7"):"/",
	("9", "6"):"/",
	("6", "9"):"/",
	("+", "5"):"/",
	("5", "+"):"/"
}

def condenser(outputString):
	newOutputString = []
	for counter in range(0, len(outputString) - 1):
		if(outputString[counter] != "AAA" and len(outputString[counter]) == 3 and len(outputString[counter + 1]) == 3):
			if(outputString[counter][1:3] == outputString[counter + 1][1:3]):
				original = outputString[counter][0]
				outputString[counter] = chordDict.get((outputString[counter][0], outputString[counter + 1][0]), outputString[counter][0]) + outputString[counter][1:3]
				if(original != outputString[counter][0]):
					outputString[counter + 1] = "AAA"
		if(outputString[counter] != "AAA"):
			newOutputString.append(outputString[counter])
	if(outputString[len(outputString) - 1] != "AAA"):
			newOutputString.append(outputString[len(outputString) - 1])
	return(newOutputString)
	
def offsetNote(note, offset):
	return(note[0] + base64[base64.index(str(note[1])) - base64.index(str(offset))] + note[2])
	