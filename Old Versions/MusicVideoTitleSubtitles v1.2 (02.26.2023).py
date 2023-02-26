# Version 1.2

import os
import subprocess
import argparse
import logging

# initialize logging
logging.basicConfig(filename='MusicVideoTitleSubtitles.log',level=logging.INFO,format='%(asctime)s.%(msecs)03d - %(message)s',datefmt='%m-%d-%Y %H:%M:%S',)
width = os.get_terminal_size().columns

# function to convert time in seconds to subtitle timestamp format
def to_timestamp(seconds):
    """Converts seconds to SRT timestamp format."""
    return f"{str(int(seconds//60)).zfill(2)}:{str(int(seconds%60)).zfill(2)},{str(int((seconds%1)*1000)).zfill(3)}"

# parse command line arguments
parser = argparse.ArgumentParser(description='Create subtitles for video files in a directory.')
parser.add_argument('-d', '--directory', help='directory path (default is current directory)')
parser.add_argument('-s', '--subdirs', action='store_true', help='scan subdirectories')
parser.add_argument('-t', '--time', help='subtitle display time in seconds, or \'full\' (default is 10)')
parser.add_argument('-p', '--position', choices=['start', 'end', 'both'], help='subtitle position (default is both)')
parser.add_argument('-r', '--remove', action='store_true', help='remove existing subtitle files')
parser.add_argument('-df', '--default', action='store_true', help='skip user prompts and use defaults')

args = parser.parse_args()

# set defaults
directory = '.' if args.default else args.directory or input("Enter directory path (default is current directory): ") or '.'
scan_subdirs = True if args.subdirs or args.default else input("Scan subdirectories? (Y/n, default is Y): ").lower() in ['y', '']
subtitle_display_time = 'full' if args.default else args.time or input("Enter subtitle display time in seconds, or 'full' (default is 10): ").lower()
if subtitle_display_time not in ['f', 'full']:
    try:
        subtitle_display_time = int(subtitle_display_time)
    except ValueError:
        subtitle_display_time = 10
subtitle_position = 'both' if args.default else args.position or input("Enter subtitle position, 'start', 'end', or 'both' (default is 'both'): ").lower()
subtitle_position = 'start' if subtitle_position in ['s', 'start'] else 'end' if subtitle_position in ['e', 'end'] else 'both'

# remove existing subtitle files if requested
if args.remove:
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            srt_filename = os.path.splitext(filepath)[0] + ".srt"

            # check if file is a subtitle file
            ext = os.path.splitext(filename)[1].lower()
            if ext == ".srt":
                # remove existing subtitle file
                os.remove(os.path.join(dirpath, filename))
                print(f"\033[91mDELETED: {filename}\033[0;0m")
                print("\033[1;90m " + '-' * (width-2) + "\033[0;0m")
                logging.warning(f"DELETED: {srt_filename}" + "\n" + " " + "-" * 198)
# loop through files in directory (and subdirectories if selected)

for dirpath, dirnames, filenames in os.walk(directory):
    for filename in filenames:
        # check if file is a video file
        ext = os.path.splitext(filename)[1].lower()
        if ext in (".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"):
            # generate subtitle file name
            subtitle_filename = os.path.splitext(filename)[0] + ".srt"

            # check if subtitle file already exists, and skip creating it if it does
            if os.path.exists(os.path.join(dirpath, subtitle_filename)):
                filepath = os.path.join(dirpath, filename)
                srt_filename = os.path.splitext(filepath)[0] + ".srt"
                print(f"\033[95mSKIPPING: {filename} (Already Exists.)\033[0;0m")
                print("\033[1;90m " + '-' * (width-2) + "\033[0;0m")
                logging.warning(f"SKIPPING: {srt_filename} (Already Exists)" + "\n" + " " + "-" * 198)
                continue

            # get video duration using ffprobe
            command = ["ffprobe", "-v", "error", "-show_entries",
                       "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", os.path.join(dirpath, filename)]
            result = subprocess.run(command, capture_output=True, text=True)
            duration = float(result.stdout.strip())

            # create subtitle file
            with open(os.path.join(dirpath, subtitle_filename), "w", encoding='utf-8') as f:
                f.write("1\n")
                if subtitle_display_time == 'full':
                    f.write(f"{to_timestamp(0)} --> {to_timestamp(duration)}\n")
                elif subtitle_position == 'start':
                    f.write(f"{to_timestamp(0)} --> {to_timestamp(subtitle_display_time)}\n")
                elif subtitle_position == 'end':
                    f.write(f"{to_timestamp(duration-subtitle_display_time)} --> {to_timestamp(duration)}\n")
                else:
                    f.write(f"{to_timestamp(0)} --> {to_timestamp(subtitle_display_time)}\n")
                    f.write("2\n")
                    f.write(f"{to_timestamp(duration-subtitle_display_time)} --> {to_timestamp(duration)}\n")
                f.write(f"{os.path.splitext(filename)[0]}\n\n")

            filepath = os.path.join(dirpath, filename)
            srt_filename = os.path.splitext(filepath)[0] + ".srt"

            print(f"\033[36mCREATED: {subtitle_filename}")
            print("\033[1;90m " + '-' * (width-2) + "\033[0;0m")
            logging.warning(f"CREATED: {srt_filename}" + "\n" + " " + "-" * 198)

    # check if scan subdirectories option is selected
    if not scan_subdirs:
        break