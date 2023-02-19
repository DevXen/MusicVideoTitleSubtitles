# Music Video Title Subtitle Generator

### Description:
MusicVideoTitleSubtitles is a command-line program that creates subtitle files for video files in a specified directory. Subtitles are generated with the video file name and can be positioned at the start, end, or both ends of the video file. The program uses FFmpeg to get the duration of the video file and generate the subtitle file. The subtitle file is saved in the same directory as the video file with the same name and a ".srt" extension.

### Requirements

* [Python 3](https://www.python.org/downloads/)
* ffprobe executable (part of [FFmpeg](https://ffmpeg.org/)) in your system's PATH.

### Usage:
`python MusicVideoSubtitleGenerator.py [-h] [-d DIRECTORY] [-s] [-t TIME] [-p POSITION]`

* The program requires a directory path to scan for video files. The user can provide the directory path as a command line argument or through a prompt. Additional options can be set through command line arguments or prompts.
* For any options not set, it will ask you for them when the program is run.
* Each user prompt has a default you can just press enter to set.
* If you set a command line argument, it will skip that user prompt when the program is run. you can skip all the user prompts by setting all the command line arguments.


### User Prompts:
If the user does not provide command line arguments, the program will prompt the user for the required information.

## Command Line Arguments:

| Short | Long | Description |
| --- | --- | --- |
| `-h` | `--help` | Show the help file, and command line arguments and exit. |
| `-d` | `--directory` | Specify the directory path where video files are located. If not specified, the current working directory will be used. If the directory path contains spaces, it should be enclosed in quotes. |
| `-s` | `--subdirs` | Optional flag to scan subdirectories for video files. If specified, the program will search for video files in all subdirectories of the specified directory. |
| `-t` | `--time` | Optional argument to specify the subtitle display time in seconds or 'full'. If not specified, the default subtitle display time is 10 seconds. If 'full' is specified, the subtitle will be displayed for the full duration of the video file.  |
| `-p` | `--position` | Optional argument to specify the subtitle position. The options are 'start', 'end', or 'both'. If not specified, the default subtitle position is 'both'. |

### Command line argument examples


#### Use the prompts to enter the directory path and to choose options for scanning subdirectories, subtitle display time, and subtitle position.

* `python MusicVideoSubtitleGenerator.py`

#### Set a directory to run on:
* `python MusicVideoTitleSubtitles.py -d "C:\My Videos"`

#### Search for video files in the videos directory and generate subtitles with 5 seconds display time:

* `python MusicVideoSubtitleGenerator.py -d videos -t 5`


#### Search for video files in the current directory and all subdirectories, and generate subtitles with 15 seconds display time:

* `python MusicVideoSubtitleGenerator.py -s -t 15`


#### Use user prompts to search for video files and generate subtitles with 20 seconds display time:

* `python MusicVideoSubtitleGenerator.py -t 20`


#### Use user prompts to search for video files and generate subtitles with 20 seconds display time and show only at the end of the video:

* `python MusicVideoSubtitleGenerator.py -t 20 -p end`


#### This will scan the /path/to/videos directory and its subdirectories for video files. Subtitle files will be created with subtitles at the beginning of the video and will be displayed for 20 seconds.

* `python MusicVideoTitleSubtitles.py -d /path/to/videos -s -t 20 -p start`

##### Generate subtitles for all video files in the directory "C:\My Videos" and its subdirectories with a display time of 5 seconds and subtitles positioned at the start of the video files.

* `python MusicVideoTitleSubtitles.py -d "C:\My Videos" -s -t 5 -p start`

#### Generate subtitles for all video files in the current directory with a display time of 15 seconds and subtitles positioned at the end of the video files.

* `python MusicVideoTitleSubtitles.py -t 15 -p end`





### Notes:
* The program only supports video files with the following extensions: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, and `.flv`.
* The program uses `ffprobe` to get the duration of the video file.
* If a subtitle file already exists for a video file, the program will skip creating a new subtitle file for that video file.
* The program does not currently support advanced subtitle features such as styling or multi-language support.




# License

This project is licensed under the GPLv3 License. See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.
