# MIDI-to-Shawzin

MIDI-to-Shawzin is a program that converts .mid files to text, which can be imported into  Warframe's Shawzin feature.

# Usage
<a href="https://github.com/Empyrrhus/MIDI-To-Shawzin/releases/">Download</a> the executable, then drag a MIDI file onto "Midi to Shawzin.exe". The output files will be in the same folder as the MIDI file.

Alternatively, if you don't want to download an exe file, you can clone the repository and run the program from command line:
```
>pip install -r requirements.txt
>python midiToShawzin [MIDI file]
```

The program will ask you to enter a scale for the MIDI file. You can find a <a href="https://www.scales-chords.com/scalefinder.php">scale finder</a> online if needed. For details on how the Shawzin input/output system works, see my notes <a href="https://www.reddit.com/r/Warframe/comments/cxbxoc/shawzin_song_recording_syntax/">here</a>. The program will output a .txt file for every instrument track in the MIDI file. If any of the notes in the MIDI are out of scale, you can check the appropriate "DEBUG" text file. These notes will be marked with "(Ignored)", and will skipped.
```
(Ignored)	Note #1	 Note C#/Db4 at 0m3.015625s
```
If the MIDI track reaches either the note limit (~107) or time limit (256s, or 4m16s), the track will be broken up into multiple lines, each seperately playable. Song parts broken up due to note limit will retain their timing; if different players start playing all the different parts simultaneously, the song should continue from person to person seamlessly.

The shawzin has a limited range (1-3 octaves). Notes that are too high or too low will loop around to the other end and play octaves instead. Adjust your MIDI file accordingly in your MIDI editor. The shawzin's first and lowest note (no frets, string 1) is treated as C5.

In theory, you can double the song length time limit by doubling the speed of the MIDI file and selecting "Slow Playback" in bottom right corner of the Shawzin song menu.

# How to Use the Shawzin
To use the Shawzin, you need to buy one from the Warframe in-game market (Menu > Market). Currently, they range from 40-60p.

<p align="center">
    <img src="https://i.imgur.com/Bxe3WwP.png" alt="Warframe market">
</p>

Next, you need to equip the Shawzin emote. (Menu > Arsenal > Emotes > Add Emotes Item > Shawzin)

<p align="center">
    <img src="https://i.imgur.com/eidLiAy.png" alt="Warframe market">
</p>

Use the Shawzin emote and open Songs. If you like, you can enable "Auto Play" at the bottom right. Select "Load Song To Memory", then copy and paste the output from the output .txt file into the text box, then select "OK".

<p align="center">
    <img src="https://i.imgur.com/x7RPBIk.png" alt="Warframe market">
</p>
