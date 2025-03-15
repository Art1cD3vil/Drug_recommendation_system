# Drug Recommendation System

This project is a **Medical Drug Recommendation System** that utilizes **MRI scans and DNA sequences** to predict tumor types and suggest personalized treatments.

## 📌 Features
- **MRI Upload & Tumor Prediction** (Using a trained CNN model)
- **DNA Sequence Analysis** (Detects mutations and suggests treatments)
- **Full-Stack Implementation** (Frontend: React, Backend: FastAPI)

---

## 🚀 Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Art1cD3vil/Drug_recommendation_system.git
```

### **2️⃣ Navigate to Project Directory**
```bash
cd Drug_recommendation_system
```

---

## 🖥️ **Backend Setup (FastAPI)**

### **3️⃣ Navigate to Backend Folder**
```bash
cd backend
```

### **4️⃣ Create a Virtual Environment** (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### **5️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **6️⃣ Run the Backend Server**
```bash
uvicorn app:app --reload
```
> The API will be available at: **http://localhost:8000**

---

## 🌐 **Frontend Setup (React)**

### **7️⃣ Navigate to Frontend Folder**
```bash
cd ../frontend
```

### **8️⃣ Install Dependencies**
```bash
npm install
```

### **9️⃣ Start the React Frontend**
```bash
npm start
```
> The frontend will run on: **http://localhost:3000**

---

## 🔥 **Testing the Application**

### **🔹 Upload MRI & Get Tumor Prediction**
- Go to **http://localhost:3000**
- Upload an MRI image file
- Get a predicted tumor type

### **🔹 Analyze DNA Sequence**
- Enter a DNA sequence (minimum 126 bases)
- Get mutation analysis and recommended treatments

---

## 📂 **Project Structure**
```
Drug_recommendation_system/
│-- backend/       # FastAPI Backend
│   ├── app.py     # Main API Logic
│   ├── uploads/   # MRI Uploads Folder
│   ├── model/     # Trained Model (Not Included)
│   ├── requirements.txt
│
│-- frontend/      # React Frontend
│   ├── src/       # React Components
│   ├── public/
│   ├── package.json
│
│-- README.md      # This Guide
```

---

## 🔧 **Common Issues & Fixes**

### ❌ `ModuleNotFoundError: No module named 'fastapi'`
- **Solution:** Run `pip install fastapi` inside the virtual environment

### ❌ `npm: command not found`
- **Solution:** Install [Node.js](https://nodejs.org/) and restart the terminal

---

## 📌 **Contributing**
Feel free to fork this repo, create a feature branch, and submit a pull request!

**💡 Happy Coding! 🚀**

