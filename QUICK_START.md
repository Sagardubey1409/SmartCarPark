# 🚀 Quick Start Guide - Smart Parking System

## Step 1: Install Dependencies

First, make sure you have all required packages installed:

```bash
pip install -r requirements.txt
```

**Note:** If you encounter any issues, you can install packages individually:
```bash
pip install opencv-python easyocr flask flask-socketio flask-cors qrcode[pil] pillow requests python-socketio python-dotenv imutils numpy
```

## Step 2: Configure (Optional)

The system works with default settings, but you can customize it:

1. Copy the example config file:
   ```bash
   # On Windows (PowerShell)
   Copy-Item config.env.example .env
   
   # On Linux/Mac
   cp config.env.example .env
   ```

2. Edit `.env` file with your settings (optional):
   - `UPI_ID` - Your UPI ID for payments
   - `CAMERA_INDEX` - Camera device index (default: 0)
   - `TOTAL_SLOTS` - Number of parking slots (default: 15)
   - `RATE_PER_MIN` - Parking rate per minute (default: 1)

## Step 3: Run the System

### Option 1: Using the Launcher (Easiest) ⭐

```bash
python run_all.py
```

This will:
- Start the plate detection system (nesm.py)
- Start the web server (app.py)
- Automatically open the dashboard in your browser

### Option 2: Manual Start (Two Terminals)

**Terminal 1 - Start Plate Detection:**
```bash
python nesm.py
```

**Terminal 2 - Start Web Server:**
```bash
python app.py
```

### Option 3: Web Server Only (No Camera)

If you only want to test the web interface:
```bash
python app.py
```

Then open: http://localhost:5000/

## Step 4: Using the System

### For Plate Detection:
1. A camera window will open showing the live feed
2. Press **'c'** key to activate plate detection
3. Point camera at a license plate
4. System will automatically:
   - Detect the plate
   - Log entry/exit
   - Update the dashboard

### For Web Dashboard:
1. Open your browser to: **http://localhost:5000/**
2. You'll see:
   - Real-time parking logs
   - Slot occupancy map
   - Statistics
   - Payment QR codes

### Keyboard Controls:
- **'c'** - Activate plate detection
- **'q'** - Quit the application

## 🌐 Web Interface URLs

- **Dashboard**: http://localhost:5000/
- **QR Payment Page**: http://localhost:5000/qr
- **API Stats**: http://localhost:5000/api/stats
- **API Logs**: http://localhost:5000/api/logs

## 🔧 Troubleshooting

### Camera Not Working?
```python
# Edit nesm.py or config.py
# Change camera index (try 0, 1, 2, etc.)
CAMERA_INDEX=1
```

### Port Already in Use?
```python
# Edit app.py or config.py
# Change port number
FLASK_PORT=5001
```

### Database Errors?
- Make sure no other instance is running
- Check if `parking.db` file exists
- Try deleting `parking.db` to recreate it (⚠️ This will delete all data)

### Plate Detection Not Working?
- Ensure good lighting
- Make sure plate is clearly visible
- Try adjusting `DETECTION_CONFIDENCE` in config (lower = more sensitive)

### Import Errors?
```bash
# Make sure you're in the correct directory
cd C:\Users\SAGAR DUBEY\OneDrive\Documents\smcar

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📝 System Requirements

- **Python**: 3.8 or higher
- **Camera**: Webcam or USB camera
- **RAM**: At least 4GB recommended
- **Storage**: ~500MB for dependencies

## 🎯 What's New in the Upgrade?

✅ **Type Safety** - Full type hints throughout  
✅ **Better Error Handling** - Comprehensive error handling  
✅ **Configuration Management** - Easy .env file configuration  
✅ **Improved Logging** - Better logging with file rotation  
✅ **Security** - Input validation and path protection  
✅ **Code Quality** - Modern Python practices  

## 🆘 Need Help?

1. Check the logs in console output
2. Check `smart_parking.log` file (if configured)
3. Verify all dependencies are installed
4. Make sure camera permissions are granted

---

**Happy Parking! 🚗**

