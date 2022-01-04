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


def get_dir(dialog_title):
    app = wx.App(None)
    style = wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST | wx.STAY_ON_TOP
    dlg = wx.DirDialog(None, dialog_title, "",
                       style=style)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
    else:
        path = None
    dlg.Destroy()
    return path


debug_mode = False

# The debug mode relies on settings.json, but im too lazy to make it not be that way
try:
    with open("settings.json", "r") as s:
        settings = json.loads(s.read())
except:
    settings = {"debug_mode": False}

if settings['debug_mode']:
    debug_mode = True
else:
    debug_mode = False

# Test to see if mkvmerge is present in the directory of the script. (Not using verify_mkvmerge()
# because it's fucking dogshit,)
try:
    output_file = MKVFile()
    audio = MKVTrack(f'test.mp4', 1, language="eng", default_track=True)
    print("mkvmerge Loaded!")
except:
    input(
        "mkvmerge Not Found! Please Download at https://www.fosshub.com/MKVToolNix.html and place executable in the "
        "same directory as PlexSorter Press any key to quit...")
    exit()

# Checks if an input folder is present. If not, it creates it.
print("-" * 20)

while True:
    # Single File
    try:
        main_menu_selection = int(input("Make A Selection:\n1) Single File\n2) Entire Directory\n3) Exit\n"))
        if main_menu_selection == 1:
            output_file = MKVFile()
            series_name = input("Series Name: ")
            episode_number = input("Episode Number: ")
            season_number = input("Season Number: ")
            # Opens the file dialog and gets the path of the video.
            print("File Selector may be behind other windows!")
            video_path = get_path("*.mp4;*.mkv;*.avi;*.mov")
            if debug_mode:
                print(f'Video path: {video_path}')
            if debug_mode:
                print(f'Show Name: {series_name}')
            # Returns to main menu out if the user doesn't select a video.
            if video_path is None:
                print("No video selected!")
                continue
            # Opens the file dialog and gets the path of the subtitles.
            subtitle_path = get_path("*.srt;*.sub;*.txt;*.ass;*.ssa")
            if debug_mode:
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
            output_dir = get_dir("Select Output Directory")
            if debug_mode:
                print(f'Output directory: {output_dir}')
            # Returns to main menu out if the user doesn't select a directory.
            if output_dir is None:
                print("No directory selected!")
                continue
            output_file.mux(
                f'{output_dir}\\{series_name} - S{season_number.zfill(2)}E{episode_number.zfill(2)}.mkv')
            print("")
        # Entire Directory
        elif main_menu_selection == 2:
            output_file = MKVFile()
            series_name = input("Series Name: ")
            season_number = input("Season Number: ")
            print("File Selector may be behind other windows!")
            input_dir = get_dir("Select Input Directory")
            if debug_mode:
                print(f'Input directory: {input_dir}')
            output_dir = get_dir("Select Output Directory")
            if debug_mode:
                print(f'Output directory: {output_dir}')
            # Prints the selected directory's contents.
            if debug_mode:
                print(os.listdir(input_dir))
            episodes = []
            fileformats = []
            # Fetches the file formats and adds them to a list.
            for i in range(2):
                fileformats.append(os.listdir(input_dir)[i][-4:])
            # Removes the file extension from the file names to make my life easier.
            for show in os.listdir(input_dir):
                episodes.append(show[:-4])
            fixed_episodes = list(dict.fromkeys(episodes))
            for i in fixed_episodes:  # Todo: Its being funny and only doing episode 1 only, fix it pls thx <3
                output_file = MKVFile()
                episode_number = i.split("Episode")[-1]
                # Adds the video and audio to the output file.
                output_file.add_track(MKVTrack(f'{input_dir}\\{i}{fileformats[1]}'))
                output_file.add_track(
                    MKVTrack(f'{input_dir}\\{i}{fileformats[1]}', 1, language="jpn", default_track=True))
                # Adds the subtitles to the output file.
                output_file.add_track(MKVTrack(f'{input_dir}\\{i}{fileformats[0]}', language="jpn", default_track=True))
                output_file.mux(
                    f'{output_dir}\\{series_name} - S{season_number.zfill(2)}E{episode_number[1:].zfill(2)}.mkv')
            print("")
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
