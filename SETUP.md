# Cropperview Setup Guide

This guide will help you set up Cropperview after cloning the repository.

## Quick Setup

### Option 1: Automatic Setup (Recommended)
1. **Download Dependencies**: Double-click `download_dependencies.bat` or run `download_dependencies.ps1`
2. **Start Cropperview**: Double-click `RUN_cropperview.bat`

### Option 2: Manual Setup
If the automatic download doesn't work, follow these steps:

#### 1. Download HandBrake CLI
- Go to: https://github.com/HandBrake/HandBrake/releases
- Download the latest `HandBrakeCLI-*.exe` file
- Rename it to `HandBrakeCLI.exe`
- Place it in the Cropperview directory

#### 2. Download Superview CLI
- Go to: https://github.com/niek/superview/releases
- Download the latest `superview-cli.exe` file
- Place it in the Cropperview directory

#### 3. Start Cropperview
- Double-click `RUN_cropperview.bat`

## Requirements

- **Windows 10/11** (64-bit)
- **Python 3.6 or higher** (included with most Windows installations)
- **PowerShell** (included with Windows 10/11)

## File Structure After Setup

```
CropperView/
├── cropperview.py                   # Main application
├── RUN_cropperview.bat              # Launcher (no command prompt)
├── download_dependencies.bat        # Dependency downloader
├── download_dependencies.ps1        # PowerShell downloader
├── HandBrakeCLI.exe                # HandBrake CLI (downloaded)
├── superview-cli.exe               # Superview CLI (downloaded)
├── input_videos/                   # Place your videos here
├── output_videos/                  # Processed videos appear here
├── settings.json                   # Your settings (created automatically)
├── README.md                       # Full documentation
└── SETUP.md                        # This file
```

## Troubleshooting

### "Python is not recognized"
- Install Python from https://python.org
- Make sure to check "Add Python to PATH" during installation

### "PowerShell execution policy error"
- Run PowerShell as Administrator
- Execute: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### "Dependencies not found"
- Check that `HandBrakeCLI.exe` and `superview-cli.exe` are in the directory
- Try running the download script again
- Download manually if automatic download fails

### "Permission denied"
- Run the batch files as Administrator
- Check Windows Defender/antivirus isn't blocking the executables

## First Run

1. **Select Input Folder**: Click "Browse Folder" and select a folder with video files
2. **Or Select Individual Files**: Click "Select Files" to choose specific video files
3. **Configure Options**: Set your preferred crop values and processing options
4. **Start Processing**: Click "Start Processing" to begin

The program will remember your settings for next time!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the processing log in the application
3. Ensure all files are in the correct locations
4. Check the main README.md for detailed documentation 