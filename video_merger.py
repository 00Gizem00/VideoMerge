from multiprocessing import process
import subprocess
import os

# arparse veya click modulunde python etc. yazmadan klasor dizilimi nasil aliniyor kullanicidan bulamadim ya da yazdiktan sonra.
# glob modulune bir bakalim.
def option_input():
    print("[1] Video Birleştirme\n")
    print("[0] Çıkış\n")
    option = input("Seçenek: ")
    if option not in ["0", "1"]:
        print("Hata: Geçersiz seçenek.")
        return option_input()
    if option == "0":
        exit()
    if option == "1":
        return 
    return klasor


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
    if len(secilenler) < 3:
        print("Hata: En az iki dosya seçmelisiniz.")
        return secilen_dosyalari_al(dosyalar)
    if not secilenler.replace(" ", "").isdigit():
        print("Hata: Lütfen sadece sayı giriniz.")
        return secilen_dosyalari_al(dosyalar)
    secilenler = [int(index) for index in secilenler.split()]
    secilen_dosyalar = [dosyalar[index - 1] for index in secilenler]
    return secilen_dosyalar

def hedef_cozunurluk_input():
    hedef_cozunurluk = input("Hedef çözünürlüğü girin (örn: 1920x1080): ")
    if not hedef_cozunurluk.replace("x", "").isdigit():
        print("Hata: Geçersiz çözünürlük.")
        return hedef_cozunurluk_input()
    return hedef_cozunurluk

# command input ta alinabilir ffmpeg icin. birlestirirken efekt vb. eklemek icin 
# yine birlestirilecek dosya ismi de alinabilir. yapmistim zaten moviepy kullandigimda. bunda da olabilir.
def videoları_birlestir(klasor, secilen_dosyalar, hedef_cozunurluk):
    log_file = open('ffmpeg.log', 'a')  # Log dosyasını aç
    try:
        for video in secilen_dosyalar:
            video_path = os.path.join(klasor, video)
            output_video = f"{video}_converted.mp4"
            cmd = ['ffmpeg', '-i', video_path, '-vf', f'scale={hedef_cozunurluk}', '-c:a', 'copy', output_video]

            
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            log_file.write(process.stdout)  # Çıktıyı log dosyasına yaz

        
        with open('video_list.txt', 'w') as f:
            for video in secilen_dosyalar:
                f.write(f"file '{video}_converted.mp4'\n")

        concat_cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'video_list.txt', '-c', 'copy', 'birlesmis_video.mp4']
        process = subprocess.run(concat_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        log_file.write(process.stdout)

        # İşlenmiş videoları temizle
        os.remove('video_list.txt')
        for video in secilen_dosyalar:
            os.remove(f'{video}_converted.mp4')

        print("Videolar birleştirildi ve 'birlesmis_video.mp4' adında bir dosya oluşturuldu.")
    finally:
        log_file.close()


if __name__ == '__main__':
    option = option_input()
    klasor = klasor_input()
    dosyalar = video_dosyalarini_goruntule(klasor)
    secilen_dosyalar = secilen_dosyalari_al(dosyalar)
    hedef_cozunurluk = hedef_cozunurluk_input()
    videoları_birlestir(klasor, secilen_dosyalar, hedef_cozunurluk)