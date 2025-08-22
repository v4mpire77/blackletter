# Enhanced OCR Setup Guide

This guide explains how to set up real OCR capabilities for the Blackletter contract analysis system.

## Current Status

The system now supports both:
1. **Simulated OCR** (default) - Uses mock contract text for testing
2. **Enhanced OCR** (optional) - Uses pytesseract and pdfplumber for real PDF text extraction

## Check OCR Status

Visit `http://localhost:8000/ocr-status` to see current OCR capabilities.

## Installing Tesseract OCR

### Windows Installation

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

2. **Install Tesseract:**
   - Run the installer as Administrator
   - Install to the default path: `C:\Program Files\Tesseract-OCR`
   - Make sure to check "Add to PATH" during installation

3. **Verify Installation:**
   ```powershell
   tesseract --version
   ```

4. **Set Environment Variable (if needed):**
   If Tesseract is not in PATH, set the environment variable:
   ```powershell
   $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
   ```

### macOS Installation

```bash
# Using Homebrew
brew install tesseract

# Or using MacPorts
sudo port install tesseract
```

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# CentOS/RHEL
sudo yum install tesseract

# Fedora
sudo dnf install tesseract
```

## Python Dependencies

The following packages are already included in `requirements.txt`:

```
pdfplumber==0.10.3    # PDF text extraction
pytesseract==0.3.10   # Python wrapper for Tesseract
pillow==10.4.0        # Image processing
```

To install them:
```powershell
cd backend
pip install -r requirements.txt
```

## Usage

Once Tesseract is installed:

1. **Check Status:**
   - Visit `http://localhost:8000/ocr-status`
   - Should show `"tesseract_configured": true`

2. **Upload PDF Files:**
   - Go to `http://localhost:3001/upload`
   - Upload actual PDF files for real OCR processing
   - The system will automatically use enhanced OCR when available

3. **Fallback Behavior:**
   - If Tesseract is not installed, the system falls back to simulation
   - No functionality is lost - you can still test the full workflow

## Features

### Enhanced OCR Capabilities:
- **Real PDF text extraction** using pdfplumber
- **OCR for scanned documents** using pytesseract
- **Automatic fallback** to OCR when text extraction yields poor results
- **Async processing** to prevent blocking
- **Cross-platform support** (Windows, macOS, Linux)

### Smart Processing:
- Extracts text directly from PDF when available
- Uses OCR only when text content is insufficient (< 50 characters)
- Handles both text-based and image-based PDFs
- Processes documents page by page

## Troubleshooting

### Common Issues:

1. **"tesseract not found" error:**
   - Ensure Tesseract is installed and in PATH
   - Set TESSERACT_CMD environment variable to full path

2. **Permission errors:**
   - Run the installer as Administrator (Windows)
   - Check file permissions for Tesseract directory

3. **Import errors:**
   - Ensure all Python dependencies are installed: `pip install -r requirements.txt`
   - Check that you're using the correct virtual environment

### Testing:

1. **Test Tesseract directly:**
   ```powershell
   tesseract --version
   ```

2. **Test Python integration:**
   ```python
   import pytesseract
   print(pytesseract.get_tesseract_version())
   ```

3. **Check OCR status endpoint:**
   ```powershell
   (Invoke-WebRequest -Uri "http://localhost:8000/ocr-status" -UseBasicParsing).Content
   ```

## Development Notes

- The enhanced OCR processor is in `backend/app/core/ocr_enhanced.py`
- Platform detection automatically configures Tesseract paths
- Error handling ensures graceful fallback to simulation
- Async processing prevents UI blocking during OCR operations
