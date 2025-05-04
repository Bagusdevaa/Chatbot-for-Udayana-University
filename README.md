# Chatbot Udayana dengan RAG dan LangChain

## Deskripsi Proyek
Proyek ini adalah implementasi chatbot informasi Universitas Udayana dengan menggunakan teknologi RAG (Retrieval Augmented Generation) dan LangChain. Chatbot ini dapat menjawab pertanyaan pengguna berdasarkan dataset informasi Universitas Udayana yang telah disediakan.

## Teknologi yang Digunakan
- **Flask**: Framework web Python untuk backend
- **LangChain**: Framework untuk membuat aplikasi AI dengan model bahasa besar (LLM)
- **OpenAI API**: Untuk model LLM dan embeddings
- **Chroma DB**: Vector database untuk menyimpan embeddings dokumen
- **RAG (Retrieval Augmented Generation)**: Metode untuk memperkaya output LLM dengan informasi dari dataset

## Struktur Proyek
```
chatbot-udayana/
│
├── app/
│   ├── __init__.py          # Inisialisasi aplikasi Flask
│   ├── routes.py            # Definisi rute-rute API
│   ├── RAG/
│   │   ├── __init__.py      # Modul RAG initialization
│   │   ├── document_loader.py  # Untuk loading dan processing dataset
│   │   ├── embeddings.py    # Konfigurasi model embedding
│   │   ├── retriever.py     # Modul retriever untuk mencari konteks relevan
│   │   └── llm.py           # Integrasi dengan OpenAI API
│   └── utils.py             # Fungsi-fungsi utilitas
│
├── static/
│   ├── css/
│   │   └── style.css        # File CSS untuk styling
│   ├── js/
│   │   └── script.js        # File JavaScript untuk interaksi frontend
│   └── img/
│       ├── logo-1.svg       # Aset gambar
│       ├── logo-2.svg
│       └── gambar1.png
│
├── templates/
│   └── index.html           # Halaman utama chatbot
│
├── data/
│   ├── dataset.txt          # Dataset informasi Universitas Udayana
│   ├── raw/                 # Folder untuk data mentah (jika diperlukan)
│   ├── processed/           # Data yang sudah diproses untuk RAG
│   │   └── embeddings/      # Untuk menyimpan vector embeddings
│   └── vector_store/        # Vector database (menggunakan Chroma)
│
├── requirements.txt         # Dependensi package
├── .env                     # File untuk environment variables (OPENAI_API_KEY, dll)
├── .env.example             # Template untuk .env file
├── config.py                # Konfigurasi aplikasi
└── run.py                   # Script untuk menjalankan aplikasi
```

## Cara Kerja RAG (Retrieval Augmented Generation)
1. **Pemrosesan Dataset**: 
   - Dataset informasi Universitas Udayana dipecah menjadi bagian-bagian kecil (chunks)
   - Setiap chunk diubah menjadi vektor embeddings menggunakan model embeddings dari OpenAI
   - Embeddings disimpan dalam vector database (Chroma DB)

2. **Proses Tanya Jawab**:
   - Pengguna mengirimkan pertanyaan melalui antarmuka web
   - Pertanyaan pengguna diubah menjadi embeddings
   - Sistem mencari dokumen yang paling relevan dengan pertanyaan pengguna menggunakan similarity search
   - Dokumen yang relevan digunakan sebagai konteks untuk model LLM
   - Model LLM (OpenAI GPT) menghasilkan jawaban berdasarkan konteks yang disediakan
   - Jawaban dikirimkan kembali ke pengguna

## Persiapan dan Instalasi

### Prasyarat
- Python 3.8+ terinstal
- Akun OpenAI dan API key
- Pip (Python package manager)

### Langkah-langkah Instalasi
1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd chatbot-udayana
   ```

2. **Buat dan aktifkan virtual environment**
   ```bash
   python -m venv venv
   # Untuk Windows
   venv\Scripts\activate
   # Untuk macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependensi**
   ```bash
   pip install -r requirements.txt
   ```

4. **Siapkan file .env**
   - Salin file `.env.example` menjadi `.env`
   - Isi API key OpenAI Anda di file `.env`
   ```bash
   cp .env.example .env
   # Edit file .env dan tambahkan OPENAI_API_KEY
   ```

5. **Jalankan aplikasi**
   ```bash
   python run.py
   ```

6. **Akses aplikasi**
   - Buka browser dan kunjungi `http://localhost:5000`

## Pengembangan Lanjutan
- Menambahkan lebih banyak data ke dataset untuk meningkatkan pengetahuan chatbot
- Mengimplementasikan caching untuk mengurangi penggunaan API
- Mengoptimalkan parameter seperti chunk size dan retriever settings
- Menambahkan otentikasi dan pencatatan percakapan
- Meningkatkan UI/UX antarmuka pengguna

## Catatan Penting
- Pastikan API key OpenAI disimpan dengan aman dan tidak dibagikan
- Aplikasi ini dirancang sebagai implementasi edukasi, bukan untuk produksi
- Penggunaan API OpenAI menimbulkan biaya, pantau penggunaan Anda

## Lisensi
Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE).