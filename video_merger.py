import argparse
import subprocess
import os
import glob

def get_parser():
    parser = argparse.ArgumentParser(description='Select and merge video files from a directory.')
    parser.add_argument('-d', '--directory', type=str, required=True, help='Directory path of video files')
    parser.add_argument('-v', '--videos', nargs='+', help='Names of video files to be merged')
    parser.add_argument('-r', '--resolution', type=str, help='Target resolution (e.g., 1920x1080)')
    parser.add_argument('-o', '--output', type=str, default='merged_video.mp4', help='Name of the merged video file')
    return parser

def list_videos(directory):
    if os.path.isdir(directory):
        print(f"Video files in {directory}:")
        videos = []
        for extension in ('*.mp4', '*.avi', '*.mkv'):
            for filepath in glob.glob(os.path.join(directory, extension)):
                videos.append(filepath)
                print(os.path.basename(filepath))
        return videos
    else:
        print(f"{directory} is not a valid directory path.")


def merge_videos(directory, video_names, resolution, output_filename):
    log_file = open('ffmpeg.log', 'a') 
    try:
        converted_files = []
        for video in video_names:
            input_path = os.path.join(directory, video)
            output_path = os.path.join(directory, f"{video}_converted.mp4")
            cmd = ['ffmpeg', '-i', input_path, '-vf', f'scale={resolution}', '-c:a', 'copy', output_path]
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log_file.write(process.stdout)
            converted_files.append(output_path)
        
        
        with open('video_list.txt', 'w') as f:
            for file_path in converted_files:
                f.write(f"file '{file_path}'\n")
        
        # ffmpeg commandinin de terminalde duzenlenebilir olmasi gerekiyor. burayi da argparse ile duzenleyebiliriz.
        concat_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video_list.txt', '-c', 'copy', output_filename]
        process = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_file.write(process.stdout)

        where_outputfile = os.path.dirname(os.path.abspath(output_filename))

        print(f"Videos have been successfully merged into {output_filename} and path: {where_outputfile}")
    finally:
        log_file.close()
        os.remove('video_list.txt')
        for file_path in converted_files:
            os.remove(file_path)

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.videos and args.resolution:
        merge_videos(args.directory, args.videos, args.resolution, args.output)
    else:
        list_videos(args.directory)
