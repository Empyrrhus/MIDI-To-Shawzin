# MIDI-to-Shawzin

MIDI-to-Shawzin is a program that converts .mid files to text, which can be imported into  Warframe's Shawzin feature.

# Usage
<a href="https://github.com/Empyrrhus/MIDI-To-Shawzin/releases/">Download</a> the executable, then drag a MIDI file onto "Midi to Shawzin.exe". The output files will be in the same folder as the MIDI file.

Alternatively, if you don't want to download an exe file, you can clone the repository and run the program from command line:
```
>pip install -r requirements.txt
>python midiToShawzin [MIDI file]
```

The program will ask you to enter a scale for the MIDI file. You can find a <a href="https://www.scales-chords.com/scalefinder.php">scale finder</a> online if needed. In particular, you want your song to be in the key of C. For details on how the Shawzin input/output system works, see my notes <a href="https://www.reddit.com/r/Warframe/comments/cxbxoc/shawzin_song_recording_syntax/">here</a>. The program will output a .txt file for every instrument track in the MIDI file. If any of the notes in the MIDI are out of scale, you can check the appropriate "DEBUG" text file. These notes will be marked with "(Ignored)", and will skipped.
```
(Ignored)	Note #1	 Note C#/Db4 at 0m3.015625s
```
The program will also prompt for a playback speed. You can extend the length limit of a song by increasing the playback speed and selecting "Slow Playback" on the shawzin song menu.

If the MIDI track reaches either the note limit (1666) or time limit (256s, or 4m16s), the track will be broken up into multiple lines, each separately importable.

The shawzin has a limited range (12 notes). Notes that are too high or too low will loop around to the other end and play octaves instead. Adjust your MIDI file accordingly in your MIDI editor. **The shawzin's first and lowest note (no frets, string 1) is treated as C3**.

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

# Additional Details
**The shawzin works best when playing only one or a few notes at a time; please edit your MIDI files to reflect this.**

Most shawzins emulate the sound of a shamisen, while the Nelumbo shawzin has the sound of an acoustic guitar. Normal shawzins have a strong, striking sound, but when many notes are played simultaneously or in rapid succession, the notes' reverb can end up increasing into an undesirable droning sound. The quieter Nelumbo does not have this problem. Compare <a href="https://www.youtube.com/watch?v=e8aWlp_e81w">this</a> to <a href="https://www.youtube.com/watch?v=xvvfW5P7sRw">this</a>.

Warframe occasionally has a bug, typically after a long enough gameplay session, where pasting from clipboard does not work. Changing your display mode (Menu > Options > Graphics > Display Mode) then changing it back fixes this.

There is also a bug where the shawzin no longer emits audio after staying in the emote for an extended period of time. Simply exit then re-enter the emote to fix this.

If your song is over 1666 notes but under 4m16s, and you wish to keep the missing time in subsequent parts as silence rather than having it be removed, you should use "-keepOffset" as a command line argument.
