import os
import subprocess


klasor = input("Klasör yolunu girin: ")


print("Klasördeki dosyalar:")
dosyalar = os.listdir(klasor)
for i, dosya in enumerate(dosyalar, start=1):
    print(f"{i}. {dosya}")


secilenler = input("Seçmek istediğiniz dosyaların numaralarını aralarında boşluk bırakarak girin (örn: 1 3 5): ")
secilenler = [int(index) for index in secilenler.split()]


secilen_dosyalar = [dosyalar[index - 1] for index in secilenler]


birlesmis_dosya = 'birlesmis_dosya.mp4'


with open('concat_list.txt', 'w') as f:
    for dosya in secilen_dosyalar:
        dosya_yolu = os.path.join(klasor, dosya)
        f.write(f"file '{dosya_yolu}'" + '\n')


ffmpeg_cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'concat_list.txt', '-c', 'copy', birlesmis_dosya]
process = subprocess.run(ffmpeg_cmd, stderr=subprocess.PIPE)

# Hataları log dosyasına yaz
with open('ffmpeg_error.log', 'a') as f:
    f.write(process.stderr.decode())


os.remove('concat_list.txt')

print(f"Videolar birleştirildi ve '{birlesmis_dosya}' adında bir dosya oluşturuldu.")

