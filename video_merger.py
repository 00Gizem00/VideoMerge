import os
from moviepy.editor import *


klasor = input("Birleştirelecek videoların klasör yolunu girin: ")


print("Klasördeki dosyalar:")
dosyalar = os.listdir(klasor)
for i, dosya in enumerate(dosyalar, start=1):
    print(f"{i}. {dosya}")


secilenler = input("Seçmek istediğiniz dosyaların numaralarını aralarında boşluk bırakarak girin (örn: 1 3 5): ")
secilenler = [int(index) for index in secilenler.split()]


secilen_dosyalar = [dosyalar[index - 1] for index in secilenler]

birlesmis_dosya = 'birlesmis_dosya.mp4'
where_output_folder = os.path.dirname(birlesmis_dosya)

# Log dosyası
with open('ffmpeg_error.log', 'a') as f:
    f.write("")

video_clips = []
for dosya in secilen_dosyalar:
    dosya_yolu = os.path.join(klasor, dosya)
    video_clips.append(VideoFileClip(dosya_yolu))


try:
    final_clip = concatenate_videoclips(video_clips, method="compose")
    final_clip.write_videofile(birlesmis_dosya, )
    print(f"Videolar birleştirildi ve '{birlesmis_dosya}' adında bir dosya oluşturuldu. Dosyanın yer aldığı klasör: '{where_output_folder}'")
except Exception as e:
    with open('ffmpeg_error.log', 'a') as f:
        f.write(str(e) + "\n")
    print("Bir hata oluştu. Detaylar 'ffmpeg_error.log' dosyasında bulunabilir.")

