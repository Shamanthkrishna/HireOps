# HireOps Launcher Files 🚀

## Quick Start Options

### Option 1: Full Launcher (Recommended)
**File:** `🚀_Launch_HireOps.bat`
- **Best for:** First-time users and regular use
- **Features:**
  - Automatic environment setup
  - Health checks and error handling
  - Server status monitoring
  - Opens browser automatically
  - Creates logs for debugging
  - ASCII art welcome screen

### Option 2: Simple Launcher  
**File:** `Start_HireOps.bat`
- **Best for:** Regular users who want a clean interface
- **Features:**
  - Clean, professional output
  - Basic error checking
  - Automatic browser opening
  - Server status display

### Option 3: Quick Start
**File:** `Quick_Start.bat`
- **Best for:** Advanced users who want minimal output
- **Features:**
  - Fastest startup
  - Minimal console output
  - Assumes environment is already set up

### Option 4: Desktop Shortcut
**File:** `Create_Desktop_Shortcut.bat`
- **Purpose:** Creates a desktop shortcut for easy access
- **Run once:** Creates "HireOps" icon on your desktop

## How to Use

### First Time Setup:
1. **Double-click** `🚀_Launch_HireOps.bat`
2. Wait for automatic setup and installation
3. HireOps will open in your browser automatically
4. Create your admin account and start using the system

### Regular Use:
- **Desktop:** Use the desktop shortcut (after running Create_Desktop_Shortcut.bat)
- **Quick:** Double-click `Quick_Start.bat`
- **Full:** Double-click `🚀_Launch_HireOps.bat` for detailed status

## What Happens When You Launch:

1. **Environment Check** - Verifies Python and virtual environment
2. **Dependency Installation** - Installs required packages (first run only)
3. **Server Start** - Launches the HireOps web server
4. **Browser Opening** - Automatically opens http://127.0.0.1:8000
5. **Status Display** - Shows server information and helpful links

## Troubleshooting

### Server Already Running
- If you see "Server appears to be already running", either:
  - Use the existing server (browser will open automatically)
  - Close any Python processes and try again

### Environment Issues
- The full launcher will attempt to create and set up the environment automatically
- If issues persist, ensure Python is installed and accessible

### Browser Doesn't Open
- Manually navigate to: http://127.0.0.1:8000
- Check if your default browser is set correctly
- Try a different browser if needed

## Access URLs

Once running, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Main App** | http://127.0.0.1:8000 | Landing page and registration |
| **Dashboard** | http://127.0.0.1:8000/dashboard | Main recruitment interface |
| **API Docs** | http://127.0.0.1:8000/docs | Interactive API documentation |

## Features Included

✅ **Modern Favicon** - Professional HireOps icon in browser tabs  
✅ **Automatic Browser Opening** - No need to manually navigate  
✅ **Error Handling** - Clear error messages and solutions  
✅ **Environment Setup** - Automatic virtual environment management  
✅ **Server Monitoring** - Checks if server is ready before opening browser  
✅ **Multiple Launcher Options** - Choose the right launcher for your needs  
✅ **Desktop Shortcut** - Easy desktop access  
✅ **Logging** - Server logs saved for debugging  

## Tips for Best Experience

💡 **Keep the server window open** - Closing it stops HireOps  
💡 **Use the desktop shortcut** - Most convenient for daily use  
💡 **Check the logs** - Located in `logs/server.log` if you need to debug  
💡 **First-time setup** - Use the full launcher for automatic environment setup  
💡 **Multiple browsers** - You can open HireOps in multiple browser tabs/windows  

---

**Need help?** All launcher files include built-in help and error messages to guide you through any issues!