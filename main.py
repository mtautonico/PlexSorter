from pymkv import MKVFile, MKVTrack
import os
import json

with open("settings.json", "r") as s:
    data = s.read()
settings = json.loads(data)

# Test to see if mkvmerge is present in the directory of the script. (Not using verify_mkvmerge()
# because it's fucking dogshit,)
try:
    output_file = MKVFile()
    audio = MKVTrack(f'test.mp4', 1, language="eng", default_track=True)
    print("mkvmerge Loaded!")
except:
    print("mkvmerge Not Found!")
    exit()

# Checks if an input folder is present. If not, it creates it.
if "input" not in os.listdir():
    if settings['debug_mode']:
        print("Created Input folder")
    os.mkdir(os.getcwd() + "\input")
else:
    if settings['debug_mode']:
        print("Input folder exists")
    pass

# Checks if an output folder is present. If not, it creates it.
if "output" not in os.listdir():
    if settings['debug_mode']:
        print("Created Output folder")
    os.mkdir(os.getcwd() + "\output")
else:
    if settings['debug_mode']:
        print("Output folder exists")
    pass
print("-" * 20)

while True:
    main_menu_selection = int(input("Make A Selection:\n1) Single File\n2) Entire Directory\n3) Exit\n"))
    # Single File
    if main_menu_selection == 1:
        output_file = MKVFile()
        inputFolderContents = os.listdir(os.getcwd() + "\input")
        for i in range(len(inputFolderContents)):
            if inputFolderContents[i].endswith(".mp4"):
                audio = MKVTrack(f'input/{inputFolderContents[i]}', 1, language="jpn", default_track=True)
                output_file.add_track(audio)
                if settings['debug_mode']:
                    print(f"Added {inputFolderContents[i]} to MKV")
        for i in range(len(inputFolderContents)):
            if inputFolderContents[i].endswith(".ass"):
                output_file.add_track(
                    MKVTrack(f'input/{inputFolderContents[i]}', 2, language="jpn", default_track=True))
                if settings['debug_mode']:
                    print(f"Added {inputFolderContents[i]} (Subtitle) to MKV")
    # Entire Directory
    elif main_menu_selection == 2:
        pass
    # Exit
    elif main_menu_selection == 3:
        exit()
    # Invalid Selection
    else:
        print("Invalid Selection")
        print("-" * 20)
        continue
