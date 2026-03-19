import os
import shutil
import random

# --- KONFIGURASI ---
# 1. Folder tempat kamu mengekstrak LFW mentah (yang isinya ribuan folder nama orang)
source_dir = "./dataset/lfw/raw" 

# 2. Folder tujuan (Sesuaikan dengan Config di script training kamu)
train_dir = "./dataset/train_face_set"
val_dir = "./dataset/test_face_set"

# 3. Aturan Main
min_images = 4      # Minimal orangnya harus punya 5 foto, kalau kurang buang!
split_ratio = 0.8   # 80% Train, 20% Val

# --- EKSEKUSI ---
print("Memulai proses seleksi dan split dataset LFW...")

# Bikin folder utama kalau belum ada
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

total_orang = 0
total_train_foto = 0
total_val_foto = 0

# Cek satu-satu folder nama orang di dalam LFW
for person_name in os.listdir(source_dir):
    person_path = os.path.join(source_dir, person_name)
    
    # Pastikan itu folder, bukan file nyasar
    if not os.path.isdir(person_path): 
        continue

    # Kumpulkan semua gambar di folder orang tersebut
    images = [f for f in os.listdir(person_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    # JURUS SELEKSI: Cuma ambil yang fotonya banyak!
    if len(images) >= min_images:
        total_orang += 1
        
        # Acak urutan fotonya biar pembagiannya random
        random.seed(42) # Biar kalau di-run ulang, acakannya tetap sama
        random.shuffle(images)
        
        # Hitung batas 80%
        train_count = int(len(images) * split_ratio)
        
        train_imgs = images[:train_count]
        val_imgs = images[train_count:]
        
        # Bikin folder nama orang tersebut di folder Train dan Val
        os.makedirs(os.path.join(train_dir, person_name), exist_ok=True)
        os.makedirs(os.path.join(val_dir, person_name), exist_ok=True)
        
        # Copy foto ke kandangnya masing-masing
        for img in train_imgs:
            shutil.copy(os.path.join(person_path, img), os.path.join(train_dir, person_name, img))
            total_train_foto += 1
            
        for img in val_imgs:
            shutil.copy(os.path.join(person_path, img), os.path.join(val_dir, person_name, img))
            total_val_foto += 1

print("-" * 40)
print("✅ PROSES SELESAI!")
print(f"Total Orang yang Lolos Seleksi : {total_orang} tokoh")
print(f"Total Foto Training (80%)      : {total_train_foto} foto")
print(f"Total Foto Validation (20%)    : {total_val_foto} foto")
print("-" * 40)