import os
from moviepy.editor import *

def klasor_input():
    klasor = input("Birleştirelecek videoların klasör yolunu girin: ")
    if not os.path.isdir(klasor):
        print("Hata: Klasör bulunamadı.")
        return klasor_input()
    return klasor

def video_dosyalarini_goruntule(klasor):
    print("Klasördeki dosyalar:")
    dosyalar = os.listdir(klasor)
    for i, dosya in enumerate(dosyalar, start=1):
        print(f"{i}. {dosya}")
    return dosyalar

def secilen_dosyalari_al(dosyalar):
    secilenler = input("Seçmek istediğiniz dosyaların numaralarını aralarında boşluk bırakarak girin (örn: 1 3 5): ")
    # if not secilenler.replace(" ", "").isdigit():
    #     print("Hata: Lütfen sadece sayıları ve boşlukları kullanın.")
    #     return secilen_dosyalari_al(dosyalar)
    secilenler = [int(index) for index in secilenler.split()]
    secilen_dosyalar = [dosyalar[index - 1] for index in secilenler]
    return secilen_dosyalar

def birlestirme_dosyasi_ismi():
    birlesmis_dosya = input("Birleştirme işlemi sonucu oluşacak dosyanın ismini girin: ") + ".mp4"
    return birlesmis_dosya


def video_birlestir(klasor, secilen_dosyalar, birlesmis_dosya):

    video_clips = []
    for dosya in secilen_dosyalar:
        dosya_yolu = os.path.join(klasor, dosya)
        video_clips.append(VideoFileClip(dosya_yolu))

    try:
        final_clip = concatenate_videoclips(video_clips, method="compose")
        final_clip.write_videofile(birlesmis_dosya)
        where_output_folder = os.path.dirname(os.path.abspath(birlesmis_dosya))
        print(f"Videolar birleştirildi ve '{birlesmis_dosya}' adında bir dosya oluşturuldu. Dosyanın yer aldığı klasör: '{where_output_folder}'")
    except Exception as e:
        with open('ffmpeg_error.log', 'a') as f:
            f.write(str(e) + "\n")
        print("Bir hata oluştu. Detaylar 'ffmpeg_error.log' dosyasında bulunabilir.")

def main():
    klasor = klasor_input()
    dosyalar = video_dosyalarini_goruntule(klasor)
    secilen_dosyalar = secilen_dosyalari_al(dosyalar)
    birlesmis_dosya = birlestirme_dosyasi_ismi()
    video_birlestir(klasor, secilen_dosyalar, birlesmis_dosya)


if __name__ == "__main__":
    main()