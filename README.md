# PlexSorter

Simple script that merges anime subtitles and video files into a single file for use with Plex. 

# Requirements

mkvmerge is required and not included. You can download it from [here](https://mkvtoolnix.download/downloads.html) for your operating system.

---

`requirements.txt` lists off all the dependencies needed to run the script. This can be installed using:
```
pip install -r requirements.txt
```
# Debug mode

For debug mode, create a file named `settings.json` in the same directory as `main.py` with the following information:
```json
{"debug_mode": true}
```