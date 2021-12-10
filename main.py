from pymkv import MKVFile, MKVTrack
import os
import json
import wx


def get_path(wildcard):
    app = wx.App(None)
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.STAY_ON_TOP
    dialog = wx.FileDialog(None, 'Open', wildcard=wildcard, style=style)
    if dialog.ShowModal() == wx.ID_OK:
        path = dialog.GetPath()
    else:
        path = None
    dialog.Destroy()
    return path


def get_dir():
    app = wx.App(None)
    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.STAY_ON_TOP
    dlg = wx.DirDialog(None, "Choose input directory", "",
                       style=style)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    else:
        path = None
    dlg.Destroy()
    return path


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
    # Single File
    try:
        main_menu_selection = int(input("Make A Selection:\n1) Single File\n2) Entire Directory\n3) Exit\n"))
        if main_menu_selection == 1:
            output_file = MKVFile()
            episode_number = input("Episode Number: ")
            season_number = input("Season Number: ")
            # Opens the file dialog and gets the path of the video.
            print("File Selector may be behind other windows!")
            video_path = get_path("*.mp4;*.mkv;*.avi;*.mov")
            if settings['debug_mode']:
                print(f'Video path: {video_path}')
            input_name = video_path.split("\\")[-1].split("Episode")[0]
            if settings['debug_mode']:
                print(f'Show Name: {input_name}')
            # Returns to main menu out if the user doesn't select a video.
            if video_path is None:
                print("No video selected!")
                continue
            # Opens the file dialog and gets the path of the subtitles.
            subtitle_path = get_path("*.srt;*.sub;*.txt;*.ass;*.ssa")
            if settings['debug_mode']:
                print(f'Subtitle path: {subtitle_path}')
            # Returns to main menu out if the user doesn't select a subtitle.
            if subtitle_path is None:
                print("No subtitle selected!")
                continue
            # The fact that I have to do this is fucking stupid.
            video = MKVTrack(video_path)
            output_file.add_track(video)
            audio = MKVTrack(video_path, 1, language="jpn", default_track=True)
            output_file.add_track(audio)
            # Adds subtitle file to output file
            output_file.add_track(MKVTrack(subtitle_path, language="jpn", default_track=True))
            # Opens directory selection dialog to specify where the file should be saved.
            output_dir = get_dir()
            if settings['debug_mode']:
                print(f'Output directory: {output_dir}')
            # Returns to main menu out if the user doesn't select a directory.
            if output_dir is None:
                print("No directory selected!")
                continue
            output_file.mux(
                f'{output_dir}\\{input_name} - S{season_number.zfill(2)}E{episode_number.zfill(2)}.mkv')
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
            print("")
            continue
    except ValueError:
        print("Invalid Selection")
        print("-" * 20)
        print("")
        continue
