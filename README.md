# 📂 Mini File Storage & Sharing System  

A **Flask + SQLite** based project that lets users upload files and instantly generate a **short link** for sharing & downloading.  
Uploaded files have an **expiry time (1 day)** and are tracked with a download counter.  

🔗 **Input:** File Upload → Short Download Link  
📥 **Output:** Secure Download with Expiry & Tracking  

---

## ✨ Features
- 📌 Upload any allowed file type (configurable)  
- ⏳ Automatic **1-day expiry** for security  
- 🔐 Secure short-code based links  
- 📊 **Download counter** for tracking usage  
- 🗂️ Metadata stored in **SQLite database**  
- 🎨 Simple and clean UI (HTML + CSS)  

---

## ⚙️ Tech Stack
- **Backend**: Flask (Python)  
- **Database**: SQLite  
- **Frontend**: HTML, CSS (Jinja2 Templates)  
- **Storage**: Local filesystem (`/uploads` folder)  

---

## 🚀 Project Structure
mini_file_storage/
│── app.py # Flask entry point
│── requirements.txt # Dependencies
│── config.py # Config (UPLOAD_FOLDER, file limits)
│── database.db # SQLite DB (auto-created)
│── /uploads/ # Uploaded files (auto-created)
│── /templates/ # HTML templates
│ ├── index.html # Upload form
│ ├── success.html # After upload (short link)
│ ├── download.html # Download page
│ └── error.html # Error (expired/not found)
│── /static/ # Static assets
│ └── style.css # Styling
│── .gitignore # Ignore cache, db, uploads
│── README.md # Project documentation


---

## 🛠️ Setup & Installation
1. Clone the repo  
   ```bash
   git clone https://github.com/<your-username>/mini-file-storage.git
   cd mini-file-storage
🎯 Future Improvements

⬆️ File size limits per user

☁️ Cloud storage integration (AWS S3 / GCP)

🔑 User authentication & private sharing

⏳ Configurable expiry (hours/days)

📊 Advanced analytics

🤝 Contributing

Pull requests are welcome!
If you’d like to add features or fix bugs, feel free to fork & PR.
