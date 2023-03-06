# Version 1.7

import os
import subprocess
import argparse
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('MusicVideoTitleSubtitles.log', encoding='utf-8')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(message)s', datefmt='%m-%d-%Y %H:%M:%S')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

width = os.get_terminal_size().columns
linewidth = width/2 % 2
is_divisible = linewidth == 0
if is_divisible:
    alignlinenum = 0
    titlelinenum = 0
else:
    alignlinenum = 1
    titlelinenum = -3


created_count = 0
deleted_count = 0
skipped_count = 0

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
directory = '.' if args.default else args.directory or input("Enter directory path [default is current directory]: ") or '.'
scan_subdirs = True if args.subdirs or args.default else input("Scan subdirectories? [Y/n]: ").lower() in ['y', '']
#subtitle_display_time = '10' if args.default else args.time or input("Enter subtitle display time in seconds, or 'full' [default is 10]: ").lower()
if args.time:
    subtitle_display_time = args.time
else: 
    subtitle_display_time = '10'

subtitle_display_timews = '10' if args.default else args.time or input("Enter subtitle display time in seconds, or 'full' [default is 10]: ").lower()

if subtitle_display_time not in ['f', 'full']:
    try:
        subtitle_display_time = int(subtitle_display_time)
    except ValueError:
        subtitle_display_time = 10
subtitle_position = 'both' if args.default else args.position or input("Enter subtitle position, 'start', 'end', or 'both' (default is 'both'): ").lower()
subtitle_position = 'start' if subtitle_position in ['s', 'start'] else 'end' if subtitle_position in ['e', 'end'] else 'both'

# remove existing subtitle files if requested
if args.remove:
    print("\n\n\033[1;90m " + '=' * (width-2) + "\033[0;0m")
    print("\033[1;90m|" + " " * (width//2-8) + "\033[0;0m\033[91mDELETING FILES:\033[1;90m" + " " * (width//2-9+alignlinenum) + "|\033[0;0m")
    print("\033[1;90m|" + " " * (width//2-9) + "=================" + " " * (width//2-10+alignlinenum) + "|\033[0;0m")
    print("\033[1;90m| " + ' ' * (width-3) + "|\033[0;0m")
    
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            srt_filename = os.path.splitext(filepath)[0] + ".srt"
            # check if file is a subtitle file
            ext = os.path.splitext(filename)[1].lower()
            if ext == ".srt":
                deleted_count += 1
                # remove existing subtitle file
                os.remove(os.path.join(dirpath, filename))
                if deleted_count == 1:
                    justaplaceholder="here"
                else:
                    print("\033[1;91m " + '-' * (width-2) + "\033[0;0m")
                print(f"\033[1;90m| \033[0;0m\033[91mDELETED\033[1;90m: {filename}\033[1;90m" + " " * (width-(len(filename))-12) + "|\033[0;0m")
                logger.info(f"DELETED: {srt_filename}" + "\n" + " " + "-" * 198)
    print("\033[1;90m " + '=' * (width-2) + "\033[0;0m")
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
                skipped_count += 1
                if skipped_count == 1:
                    print("\n\n\033[1;90m " + '=' * (width-2) + "\033[0;0m")
                    print("\033[1;90m|" + " " * (width//2-8) + "\033[0;0m\033[93mSKIPPING FILES\033[90m:" + " " * (width//2-9+alignlinenum) + "|\033[0;0m")
                    print("\033[1;90m|" + " " * (width//2-9) + "=================" + " " * (width//2-10+alignlinenum) + "|\033[0;0m")
                    print("\033[1;90m| " + ' ' * (width-3) + "|\033[0;0m")
                else: 
                    print("\033[1;93m " + '-' * (width-2) + "\033[0;0m")
                print(f"\033[1;90m| \033[0;0m\033[93mSKIPPING:\033[1;90m {subtitle_filename} " + " " * (width-(len(subtitle_filename))-14) + "|\033[0;0m")
                logger.info(f"SKIPPING: {srt_filename} (Already Exists)" + "\n" + " " + "-" * 198)
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
            created_count += 1
            if created_count == 1:
                width = os.get_terminal_size().columns
                print("\n\n\033[1;90m " + '=' * (width-2) + "\033[0;0m")
                print("\033[1;90m|" + " " * (width//2-8) + "\033[0;0m\033[36mCREATING FILES:\033[1;90m" + " " * (width//2-9+alignlinenum) + "|\033[0;0m")
                print("\033[1;90m|" + " " * (width//2-9) + "=================" + " " * (width//2-10+alignlinenum) + "|\033[0;0m")
                print("\033[1;90m| " + ' ' * (width-3) + "|\033[0;0m")

            else:
                print("\033[0;36m " + '-' * (width-2) + "\033[0;0m")			
            print(f"\033[1;90m| \033[0;0m\033[36mCREATED\033[1;90m: {subtitle_filename}\033[1;90m" + " " * (width-(len(subtitle_filename))-12) + "|\033[0;0m")

            logger.info(f"CREATED: {srt_filename}" + "\n" + " " + "-" * 198)



print("\033[1;90m " + '=' * (width-2) + "\033[0;0m")
print("\n\n\n\033[1;90m " + '=' * (width-2) + "\033[0;0m")
print("\033[1;90m|" + " " * (width//2-6) + "\033[0;0m\033[36mFILE STATS:\033[1;90m" + " " * (width//2-7+alignlinenum) + "|\033[0;0m")
print("\033[1;90m|" + " " * (width//2-7) + "=============" + " " * (width//2-8+alignlinenum) + "|\033[0;0m")
print("\033[1;90m| " + ' ' * (width-3) + "|\033[0;0m")
print(f"\033[1;90m|" + ' ' * (width//2-40) + f" \033[0;0m\033[36m{created_count} \033[1;90mSubtitle Files \033[0;36mCreated.\033[1;90m |\033[93m {skipped_count} \033[1;90mSubtitle files \033[0;93mskipped.\033[1;90m |\033[91m {deleted_count} \033[1;90mSubtitle Files \033[0;91mDeleted.\033[1;90m" + " " * (width//2-41-(len(str(created_count)))-(len(str(skipped_count)))-(len(str(deleted_count)))+alignlinenum) +"|\033[0;0m")
print("\033[1;90m " + '=' * (width-2) + "\033[0;0m")

