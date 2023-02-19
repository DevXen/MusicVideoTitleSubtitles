# Version 1.0

import os
import subprocess
import argparse

# function to convert time in seconds to subtitle timestamp format
def to_timestamp(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

# parse command line arguments
parser = argparse.ArgumentParser(description='Create subtitles for video files in a directory.')
parser.add_argument('-d', '--directory', help='directory path (default is current directory)')
parser.add_argument('-s', '--subdirs', action='store_true', help='scan subdirectories')
parser.add_argument('-t', '--time', help='subtitle display time in seconds, or \'full\' (default is 10)')
parser.add_argument('-p', '--position', choices=['start', 'end', 'both'], help='subtitle position (default is both)')

args = parser.parse_args()

# get directory path from user input or command line argument, default to current directory
directory = args.directory or input("Enter directory path (default is current directory): ") or "."

# get option to scan subdirectories from command line argument or user input
if args.subdirs:
    scan_subdirs = True
else:
    scan_subdirs = input("Scan subdirectories? (Y/n, default is Y): ").lower() in ["y", ""]

# get subtitle display time option from command line argument or user input
if args.time:
    subtitle_display_time = args.time
else:
    subtitle_display_time = input("Enter subtitle display time in seconds, or 'full' (default is 10): ").lower()

if subtitle_display_time in ['f', 'full']:
    subtitle_display_time = 'full'
else:
    try:
        subtitle_display_time = int(subtitle_display_time)
    except ValueError:
        subtitle_display_time = 10

# get subtitle position option from command line argument or user input
if args.position:
    subtitle_position = args.position
else:
    subtitle_position = input("Enter subtitle position, 'start', 'end', or 'both' (default is 'both'): ").lower()

if subtitle_position in ['s', 'start']:
    subtitle_position = 'start'
elif subtitle_position in ['e', 'end']:
    subtitle_position = 'end'
else:
    subtitle_position = 'both'

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
                print(f"Skipping subtitle file creation for {filename}, subtitle file already exists.")
                continue

            # get video duration using ffprobe
            command = ["ffprobe", "-v", "error", "-show_entries",
                       "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", os.path.join(dirpath, filename)]
            result = subprocess.run(command, capture_output=True, text=True)
            duration = float(result.stdout.strip())

            # create subtitle file
            with open(os.path.join(dirpath, subtitle_filename), "w") as f:
                if subtitle_position == 'start':
                    # write subtitle for first 10 seconds
                    f.write("1\n")
                    f.write(f"{to_timestamp(0)} --> {to_timestamp(subtitle_display_time)}\n")
                    f.write(f"{os.path.splitext(filename)[0]}\n")
                    f.write("\n")
                elif subtitle_position == 'end':
                    # write subtitle for last 10 seconds
                    f.write("1\n")
                    f.write(f"{to_timestamp(duration-subtitle_display_time)} --> {to_timestamp(duration)}\n")
                    f.write(f"{os.path.splitext(filename)[0]}\n")
                    f.write("\n")
                else:
                    # write subtitle for first 10 seconds
                    f.write("1\n")
                    f.write(f"{to_timestamp(0)} --> {to_timestamp(subtitle_display_time)}\n")
                    f.write(f"{os.path.splitext(filename)[0]}\n")
                    f.write("\n")

                    # write subtitle for last 10 seconds
                    f.write("2\n")
                    f.write(f"{to_timestamp(duration-subtitle_display_time)} --> {to_timestamp(duration)}\n")
                    f.write(f"{os.path.splitext(filename)[0]}\n")
                    f.write("\n")

            print(f"Subtitle file created for {filename}: {subtitle_filename}")

    # check if scan subdirectories option is selected
    if not scan_subdirs:
        break
