## 📌 Introduction

**AIT Brute Force Tool** is an open-source Python-based tool designed for security testing and password auditing.  
It automates brute-force attacks using **ChromeDriver**, making it useful for penetration testing and cybersecurity research.  

⚠️ **Disclaimer:** This tool is intended for **educational and security research purposes only**.  
Unauthorized use against systems you do not own is **illegal**. Proceed responsibly.  

---

## 🛠️ Requirements

### 1️⃣ ChromeDriver  
ChromeDriver is required for browser automation. Download the appropriate version based on your Chrome browser:  

- **Version 133 and later:** [Download here](https://googlechromelabs.github.io/chrome-for-testing/)  
- **Version 114 and earlier:** [Download here](https://sites.google.com/chromium.org/driver/downloads)  

📌 **Tip:** Ensure ChromeDriver is accessible in your system **PATH**.  

### 2️⃣ Python  
Install the latest **stable version** of Python:  

- 📥 [Download Python](https://www.python.org/downloads/)  

Verify installation with:

```sh
python --version
```
or

```sh
python3 --version
```

---

## 🚀 Installation & Setup

### 1️⃣ Fork & Clone the Repository

```sh
git clone https://github.com/yourusername/ait-brute-force-tool.git
```

```sh
cd ait-brute-force-tool
```

### 2️⃣ Set Up ChromeDriver  

- Download the correct ChromeDriver version (based on your browser).  
- Extract it and move it to a directory in your system **PATH**.  

---

## 📌 Usage

### Running the Tool  

To start the tool, run:

```sh
python main.py
```
or

```sh
python3 main.py
```


### How It Works  
The script automates browser interaction using **ChromeDriver**.  
Follow on-screen prompts and wait for the process to complete.  

---

## 🔧 Troubleshooting  

### ❌ ChromeDriver Version Mismatch  
If you encounter an error like:  

> This version of ChromeDriver only supports Chrome version X  

Check that:  
- Your ChromeDriver version matches your **Chrome browser version**.  
- Your Chrome is up to date, or downgrade Chrome to match the driver.  

### ❌ Python Not Found  
If you see **"command not found"**, ensure **Python is installed and added to your system PATH**.  

---

## 📢 Changelog

See the latest updates and improvements in the [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License 

This project is open-source and licensed under the **MIT License**.
