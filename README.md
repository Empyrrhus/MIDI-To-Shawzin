# MIDI-to-Shawzin

MIDI-to-Shawzin is a program that converts .mid files to text, importable by Warframe's Shawzin feature.

# Usage

Download the executable, then drag a MIDI file on top of it.

Alternatively, you can clone and run the program from command line:
```
>pip install -r requirements.txt
>python midiToShawzin [MIDI file]
```

The program will ask you to enter a scale for the MIDI file. You can find a <a href="https://www.scales-chords.com/scalefinder.php">scale finder</a> online if needed. For details on how the Shawzin input/output system works, see my notes <a href="https://www.reddit.com/r/Warframe/comments/cxbxoc/shawzin_song_recording_syntax/">here</a>. The program will then output a .txt file for every instrument track in the MIDI file. If any of the notes in the MIDI are out of scale, you can check the appropriate "DEBUG" text file. These notes will be marked with "(Ignored)", and will not be converted.
```
(Ignored)	Note #1	 Note C#/Db4 at 0m3.015625s
```

# Using the Shawzin
To use the Shawzin, you need to buy one from the Warframe market.

<p align="center">
    <img src="https://i.imgur.com/Bxe3WwP.png" alt="Warframe market">
</p>

Next, you need to equip the Shawzin emote. (Menu > Arsenal > Emotes > Add Emotes Item > Shawzin)

<p align="center">
    <img src="https://i.imgur.com/eidLiAy.png" alt="Warframe market">
</p>

Use the Shawzin emote and open Songs > Load Song to Memory. Then, copy and paste the output from the output text file into the text box, then select "OK".

<p align="center">
    <img src="https://i.imgur.com/x7RPBIk.png" alt="Warframe market">
</p>
