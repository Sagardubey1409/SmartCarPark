# Smart Parking System

A comprehensive number plate detection and parking management system with real-time monitoring, UPI payments, and modern web interface.

## 🚀 Features

### Core Functionality
- **Real-time Number Plate Detection** - Uses EasyOCR for accurate plate recognition
- **Automatic Slot Management** - Assigns and tracks parking slots (A1-A15)
- **UPI QR Code Payments** - Generates dynamic QR codes for parking fees
- **Live Dashboard** - Real-time updates with WebSocket technology
- **SMS Payment Confirmation** - Webhook integration for payment verification

### Modern UI/UX
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Dark Theme** - Modern dark interface with smooth animations
- **Real-time Statistics** - Live updates of parking metrics
- **Interactive Slot Map** - Visual representation of parking slots
- **Notification System** - Toast notifications for all events

### Technical Features
- **Database Management** - SQLite with automatic schema updates
- **Error Handling** - Comprehensive error handling and logging
- **Rate Limiting** - API protection against abuse
- **Process Monitoring** - Automatic restart and health monitoring
- **Configuration Management** - Environment-based configuration

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam or camera device
- Modern web browser
- Internet connection (for CDN resources)

## 🛠️ Installation

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd smart-parking-system

# Or download and extract the ZIP file
```

### 2. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or install manually
pip install opencv-python easyocr flask flask-socketio qrcode[pil] requests python-socketio
```

### 3. Configuration (Optional)
```bash
# Copy configuration template
cp config.env.example .env

# Edit configuration as needed
# nano .env
```

## 🚀 Quick Start

### Method 1: Using the Launcher (Recommended)
```bash
python run_all.py
```

### Method 2: Manual Start
```bash
# Terminal 1: Start plate detection
python nesm.py

# Terminal 2: Start web server
python app.py
```

### Method 3: Using the Simple Launcher
```bash
python runn_this.py
```

## 🌐 Web Interface

Once started, the system will automatically open:
- **Dashboard**: http://localhost:5000/
- **QR Payment**: http://localhost:5000/qr

## 📱 Usage

### For Operators
1. **Start the System**: Run `python run_all.py`
2. **Detect Plates**: Press 'c' in the camera window to detect plates
3. **Monitor Dashboard**: Watch real-time updates on the web dashboard
4. **Process Payments**: Use the QR payment interface for exits

### For Customers
1. **Entry**: Drive to the entrance, system detects your plate automatically
2. **Parking**: System assigns you a slot (A1-A15)
3. **Exit**: Drive to exit, system generates QR code for payment
4. **Payment**: Scan QR code with UPI app and pay
5. **Confirmation**: System confirms payment and allows exit

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
# Database
DB_NAME=parking.db
RATE_PER_MIN=1
TOTAL_SLOTS=15

# Web Server
SECRET_KEY=your-secret-key
FLASK_ENV=development

# SMS Gateway (Optional)
TRACCAR_TOKEN=your-token-here

# UPI Payment
UPI_ID=your-upi-id@bank
PAYEE_NAME=ParkingLot
```

### Customization
- **Parking Rate**: Modify `RATE_PER_MIN` in `db_manager.py`
- **Total Slots**: Change `TOTAL_SLOTS` in `db_manager.py`
- **UPI Details**: Update UPI ID in `generate_upi_qr()` function
- **SMS Integration**: Configure webhook token for payment confirmation

## 📊 API Endpoints

### REST API
- `GET /api/stats` - Get parking statistics
- `GET /api/logs` - Get all parking logs
- `GET /api/exit_info/<plate>` - Get exit information
- `POST /api/confirm_exit` - Confirm payment and exit
- `POST /api/plate_detected` - Report plate detection

### WebSocket Events
- `logs_update` - Real-time log updates
- `slots_update` - Slot status updates
- `plate_detected` - New plate detection
- `payment_confirmed` - Payment confirmation

## 🗂️ File Structure

```
smart-parking-system/
├── app.py                 # Main Flask application
├── nesm.py                # Plate detection system
├── db_manager.py          # Database operations
├── run_all.py            # System launcher
├── runn_this.py          # Simple launcher
├── requirements.txt      # Python dependencies
├── config.env.example    # Configuration template
├── templates/
│   ├── dashb.html        # Main dashboard
│   └── qr.html          # QR payment page
├── static/
│   └── sounds/           # Audio notifications
├── IMAGES/               # Generated QR codes
├── detections/           # Captured plate images
└── parking.db           # SQLite database
```

## 🔍 Troubleshooting

### Common Issues

**Camera not detected:**
```bash
# Check camera permissions
# Try different camera index in nesm.py
cap = cv2.VideoCapture(1)  # Try 0, 1, 2, etc.
```

**Database locked:**
```bash
# Stop all processes and restart
# Check for multiple instances running
```

**Plate detection not working:**
```bash
# Ensure good lighting
# Check camera focus
# Verify plate is clearly visible
```

**Web interface not loading:**
```bash
# Check if port 5000 is available
# Try different port in app.py
app.run(port=5001)
```

### Logs
- System logs: `smart_parking.log`
- Flask logs: Console output
- Detection logs: Console output

## 🚀 Advanced Features

### SMS Payment Integration
1. Set up SMS gateway webhook
2. Configure `TRACCAR_TOKEN` in environment
3. SMS format: "INR 40.00 received via UPI from abc@okicici. Ref: MH12AB1234"

### Custom UPI Integration
1. Modify `generate_upi_qr()` function
2. Update UPI ID and payee name
3. Test with different UPI apps

### Database Backup
```bash
# Backup database
cp parking.db parking_backup_$(date +%Y%m%d).db

# Restore database
cp parking_backup_20240101.db parking.db
```

## 📈 Performance Optimization

### For Better Detection
- Use good lighting conditions
- Ensure camera is stable
- Keep plates clean and visible
- Use higher resolution camera

### For Better Performance
- Close unnecessary applications
- Use SSD storage for database
- Ensure stable internet connection
- Monitor system resources

## 🔒 Security Considerations

- Change default SECRET_KEY in production
- Use HTTPS in production
- Implement proper authentication
- Regular database backups
- Monitor system logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review system logs
3. Create an issue with detailed information
4. Include system specifications and error messages

## 🎯 Roadmap

- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Multi-camera support
- [ ] Cloud database integration
- [ ] Machine learning improvements
- [ ] Multi-language support
- [ ] Advanced reporting features
- [ ] Integration with parking sensors

---

**Made with ❤️ for smart parking solutions**

