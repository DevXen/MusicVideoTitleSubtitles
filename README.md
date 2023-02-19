# Music Video Title Subtitle Generator

Music Video Title Subtitle Generator is a command-line tool for creating subtitle files for music videos. It generates a `.srt` subtitle file with the same name as the input video file.

## Usage
python music_video_subtitle_generator.py [-h] [-d DIRECTORY] [-s] [-t TIME] [-p]


## Arguments

| Short | Long | Description |
| --- | --- | --- |
| -h | --help | Show the help message and exit. |
| -d | --directory | The directory path to search for video files. Default is the current directory. |
| -s | --subdirs | Include subdirectories in the search. |
| -t | --time | The length of time in seconds that the subtitle should be displayed. Default is 10 seconds. This argument also accepts the value "full" to display the subtitle for the entire duration of the video. |
| -p | --prompt | Use user prompts instead of command-line arguments. |

## Examples

Search for video files in the current directory and generate subtitles with 10 seconds display time:

python MusicVideoSubtitleGenerator.py (No command line options, it will promot you for the options on run)


Search for video files in the `videos` directory and generate subtitles with 5 seconds display time:

python music_video_subtitle_generator.py -d videos -t 5


Search for video files in the current directory and all subdirectories, and generate subtitles with 15 seconds display time:

python music_video_subtitle_generator.py -s -t 15


Use user prompts to search for video files and generate subtitles with 20 seconds display time:

python music_video_subtitle_generator.py -t 20


Use user prompts to search for video files and generate subtitles with 20 seconds display time and show only at the end of the video:

python music_video_subtitle_generator.py -t 20 -p end
