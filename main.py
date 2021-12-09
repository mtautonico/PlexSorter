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
        input_name = ""
        for i in range(len(inputFolderContents)):
            # Finds the Video file in the input folder
            if inputFolderContents[i].endswith(".mp4"):
                output_file = MKVFile()
                # The fact that I have to do this is fucking stupid.
                video = MKVTrack(f'input/{inputFolderContents[i]}')
                output_file.add_track(video)
                audio = MKVTrack(f'input/{inputFolderContents[i]}', 1, language="jpn", default_track=True)
                output_file.add_track(audio)
                # Name of the video file
                input_name = inputFolderContents[i][:-4]
                # Prints to console if the video was added if debug mode is on.
                if settings['debug_mode']:
                    print(f"Added {inputFolderContents[i]} to MKV")
                # Adds subtitle file to output file
                output_file.add_track(MKVTrack(f'input/{input_name}.ass', language="jpn", default_track=True))
                # Prints to console if the subtitle was added if debug mode is on.
                if settings['debug_mode']:
                    print(f"Added {input_name} (Subtitles) to MKV")
        output_file.mux(f'output/{input_name}.mkv')
        print("")
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
