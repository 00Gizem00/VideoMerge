from moviepy.editor import *

clip1 = VideoFileClip("video_list/video1.mp4")
clip2 = VideoFileClip("video_list/video2.mp4")

final_clip = concatenate_videoclips([clip1, clip2], method="compose")

final_clip.write_videofile(
    "combined2_video.mp4",
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
)
