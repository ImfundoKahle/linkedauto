<div align="center">
  <img src="logo.png" alt="LinkedAuto Logo" width="200">
  <h1>LinkedAuto</h1>
  <p>🤖 A powerful Python automation tool for LinkedIn connection requests</p>
  
  [![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
  [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/xeloxa/linkedauto/pulls)
</div>

## ✨ Features

- 🔐 **Automatic Login** - Seamless LinkedIn login via console or browser
- 🔒 **2FA Support** - Works with Two-Factor Authentication enabled accounts
- 📝 **Customizable Messages** - Personalize your connection requests with custom notes
- 🔍 **Smart Search** - Find and connect with profiles based on your keywords
- ⏱️ **Rate Limiting** - Weekly connection limit control to stay within LinkedIn's limits
- 🌈 **Beautiful Output** - Colored console output and comprehensive logging
- 🖥️ **Headless Mode** - Run in the background without browser UI
- 🔄 **Auto-Updating** - Automatic ChromeDriver management
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🌐 **Multi-Language** - Supports English and Turkish

## 📸 Screenshot

![LinkedAuto in Action](screenshot.jpeg)

## 🚀 Getting Started

### Prerequisites

- 🐍 Python 3.7 or higher
- 🌐 Chrome browser installed
- 🔑 LinkedIn account

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/xeloxa/linkedauto.git
   cd linkedauto
   ```

2. **Set up a virtual environment**
   ```bash
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🚦 Usage

1. **Run the script**
   ```bash
   python linkedAuto.py
   ```

2. **Follow the on-screen instructions** to log in and start automating your LinkedIn connections.

---

## 🔒 Program Operation and Security

This tool operates using the official LinkedIn web interface with the following security measures in place:

### 🔐 Secure Authentication
- **🔑 Password Security**: Your credentials are never stored or transmitted externally. They are securely entered in each session.
- **🔒 2FA Support**: Fully compatible with Two-Factor Authentication for enhanced security.
- **🔄 Session Management**: Each session is fresh and all resources are properly cleaned up after use.

### 🛡️ Data Privacy
- **💻 Local Processing**: Everything runs on your local machine - no data is sent to external servers.
- **🧹 Automatic Cleanup**: All cookies and cache are cleared when the session ends.
- **📝 Minimal Logging**: Only essential operational logs are kept for debugging.

### ⚙️ Technical Implementation
- **🤖 Selenium WebDriver**: Industry-standard automation framework for reliable browser control.
- **🌐 Chrome Integration**: Seamlessly works with your existing Chrome installation.
- **🚨 Error Handling**: Graceful error recovery and resource cleanup in all scenarios.

## 🚨 Common Issues

- **⚠️ Chrome Version Mismatch**
  - *Solution*: Update Chrome to the latest version or let `webdriver-manager` handle the driver installation.

- **🔑 Login Problems with 2FA**
  - *Solution*: Be ready to enter your 2FA code when prompted during login.

- **⛔ Connection Limits Reached**
  - *Solution*: LinkedIn enforces weekly connection limits. Wait a few days before trying again.

## 🗺️ Roadmap

- [ ] 📥 Manage incoming connection requests
- [ ] 📊 Analytics dashboard for connection statistics
- [ ] 🌍 Support for additional languages
- [ ] 🤖 AI-powered connection message generation

## 📜 License

This project is licensed under the [MIT License](LICENSE).

## 👥 Contributing

Contributions are what make the open-source community an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Important Notice

> **Warning**: This tool is provided for **educational purposes only**. Please respect LinkedIn's Terms of Service. The developers assume **no responsibility** for any consequences resulting from the use of this tool. Use at your own risk and discretion.

---

<div align="center">
  Made with ❤️ by xeloxa
</div>