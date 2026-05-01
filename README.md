# Air Quality Analysis Dashboard

Dashboard interaktif ini dibuat menggunakan **Streamlit** untuk menganalisis dan memvisualisasikan dataset kualitas udara (Beijing Multi-Site Air-Quality Data). Proyek ini merupakan bagian dari tugas akhir kelas Belajar Analisis Data dengan Python di Dicoding.

##  Setup Environment & Menjalankan Dashboard Secara Lokal

Berikut adalah instruksi lengkap untuk melakukan *setup environment*, menginstal *library*, dan menjalankan *dashboard* ini di komputer lokal Anda:

### 1. Persiapan Direktori
Pastikan Anda sudah mengekstrak file *submission* (atau *clone repository* ini) dan berada di dalam folder utama proyek (folder yang berisi file `requirements.txt`). Buka Terminal atau Command Prompt (CMD) di folder tersebut.

### 2. Setup Virtual Environment
Sangat disarankan untuk menggunakan *virtual environment* agar instalasi *library* tidak mengganggu sistem Python bawaan komputer Anda. Jalankan perintah berikut di Terminal/CMD:
```bash
python -m venv venv
```
#### Aktivasi Virtual Environment:
```venv\Scripts\activate```

### 3. Install Library (Requirements)
```pip install -r requirements.txt```

### 4. Menjalankan Dashboard
```cd dashboard```

```streamlit run dashboard.py```

