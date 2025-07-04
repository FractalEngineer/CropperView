# Cropperview

A comprehensive GUI application for processing video files with cropping, superview, and combining capabilities using HandBrake and Superview CLI.

## Quick Start

1. **Clone the repository**
2. **Download dependencies**: Run `download_dependencies.bat` or `download_dependencies.ps1`
3. **Start Cropperview**: Double-click `RUN_cropperview.bat`

For detailed setup instructions, see [SETUP.md](SETUP.md).

## Features

- **File Selection**: Browse and select input folders containing video files
- **Automatic Detection**: Automatically scans for video files when folder is selected and on startup
- **Multiple File Support**: Automatically detects multiple video files and offers to combine them
- **Video Cropping**: Crop videos with customizable dimensions (default: 0:0:144:148)
- **Superview Processing**: Apply Niek's Superview effect to videos
- **Output Management**: Flexible output folder selection with option to use same folder as input
- **Progress Tracking**: Real-time progress bar and detailed processing log with timestamps
- **Settings Persistence**: Remembers your last used settings and input folder
- **Clean Interface**: No command prompt windows - runs as a standalone GUI application

## Requirements

- **Windows 10/11** (64-bit)
- **Python 3.6 or higher** (included with most Windows installations)
- **HandBrakeCLI.exe** (downloaded automatically or manually)
- **superview-cli.exe** (downloaded automatically or manually)

## Installation

### Automatic Setup (Recommended)
1. Clone this repository
2. Run `download_dependencies.bat` to download required executables
3. Double-click `RUN_cropperview.bat` to start

### Manual Setup
If automatic download fails:
1. Download HandBrake CLI from https://github.com/HandBrake/HandBrake/releases
2. Download Superview CLI from https://github.com/niek/superview/releases
3. Place both executables in the project directory
4. Run `RUN_cropperview.bat`

See [SETUP.md](SETUP.md) for detailed instructions.

## Usage

### 1. Input Setup
- Click "Browse Folder" to select your input folder containing video files
- Or click "Select Files" to choose individual video files
- Files are automatically detected when folder is selected
- On startup, if a previous input folder exists, files are automatically scanned
- Supported formats: MP4, AVI, MOV, MKV, WMV, FLV, WebM, M4V, TS

### 2. Output Settings
- Choose whether to use the same folder as input or select a different output folder
- Check "Use same folder as input" to automatically set output to input folder

### 3. Processing Options
- **Combine Videos**: When multiple files are detected, choose whether to combine them into one file
- **Crop Videos**: Enable/disable video cropping with custom dimensions
- **Crop Values**: Format is `top:bottom:left:right` (default: 0:0:144:148)
- **Apply Superview**: Enable/disable Superview processing
- **GPU Acceleration**: Enable hardware acceleration for faster processing
  - **HandBrake Encoder**: Choose between CPU (x264/x265) or GPU encoders (NVIDIA NVENC, Intel QSV)
  - **Superview Encoder**: Select encoder for Superview processing

### 4. Processing
- Click "Start Processing" to begin
- Monitor progress in the log window with real-time timestamps
- Files are processed in this order:
  1. Combine videos (if enabled and multiple files)
  2. Crop videos (if enabled)
  3. Apply Superview (if enabled)

### 5. Output Files
Files are automatically renamed with suffixes indicating the processing steps:
- `-combined`: Applied when videos are combined
- `-cropped`: Applied when cropping is performed
- `-superview`: Applied when Superview is applied

Example: `video-combined-cropped-superview.mp4`

## File Structure

```
CropperView/
├── cropperview.py                   # Main GUI application
├── RUN_cropperview.bat              # Launcher (no command prompt)
├── download_dependencies.bat        # Dependency downloader (batch)
├── download_dependencies.ps1        # Dependency downloader (PowerShell)
├── HandBrakeCLI.exe                # HandBrake command line tool (downloaded)
├── superview-cli.exe               # Superview processing tool (downloaded)
├── input_videos/                   # Default input folder
├── output_videos/                  # Default output folder
├── settings.json                   # Saved settings (created automatically)
├── README.md                       # This file
├── SETUP.md                        # Setup guide
└── .gitignore                      # Git ignore file
```

## Technical Details

### Processing Pipeline
1. **File Detection**: Recursively scans input folder for video files
2. **Combination**: Uses HandBrake to combine multiple videos if requested
3. **Cropping**: Uses HandBrake with custom crop parameters
4. **Superview**: Uses superview-cli.exe to apply Superview effect
5. **Cleanup**: Removes temporary files and moves final output to destination

### Temporary Files
- All processing uses a temporary folder within the output directory
- Temporary files are automatically cleaned up after processing
- If processing fails, temporary files may remain for debugging

### Error Handling
- Comprehensive error messages in the log window with timestamps
- Graceful handling of missing files or invalid parameters
- Settings are saved automatically when the program closes

### Auto-Scanning
- Automatically scans for video files when input folder is selected
- On startup, if a previous input folder exists, automatically scans for files
- No manual scan button needed - everything happens automatically

## Troubleshooting

### Common Issues

1. **"HandBrake failed" error**
   - Ensure HandBrakeCLI.exe is in the same directory as the script
   - Check that input video files are not corrupted

2. **"Superview failed" error**
   - Ensure superview-cli.exe is in the same directory as the script
   - Verify input video format is supported

3. **No video files detected**
   - Check that the input folder contains video files
   - Verify file extensions are supported (.mp4, .avi, etc.)

4. **Permission errors**
   - Ensure you have write permissions to the output folder
   - Try running as administrator if needed

5. **Dependencies not found**
   - Run `download_dependencies.bat` to download required files
   - Check that executables are in the project directory

### Performance Tips

- For large video files, processing may take significant time
- The GUI remains responsive during processing (runs in background thread)
- Monitor the progress bar and log for current status
- Real-time logging shows exactly what's happening during processing

## Advanced Usage

### Custom Crop Values
The crop format is `top:bottom:left:right` where:
- `top`: Pixels to crop from the top
- `bottom`: Pixels to crop from the bottom
- `left`: Pixels to crop from the left
- `right`: Pixels to crop from the right

### GPU Acceleration
Enable hardware acceleration for significantly faster processing:

#### HandBrake Encoders:
- **x264/x265**: CPU-based encoding (default, compatible with all systems)
- **h264_nvenc/hevc_nvenc**: NVIDIA GPU acceleration (requires NVIDIA GPU)
- **h264_qsv/hevc_qsv**: Intel Quick Sync acceleration (requires Intel CPU with QSV)

#### Superview Encoders:
- **libx264/libx265**: CPU-based encoding (default)
- **h264_nvenc/hevc_nvenc**: NVIDIA GPU acceleration
- **h264_qsv/hevc_qsv**: Intel Quick Sync acceleration

#### Performance Tips:
- GPU acceleration can provide 2-5x faster encoding
- NVIDIA NVENC is generally the fastest option
- Intel QSV provides good performance with lower power consumption
- CPU encoding provides the best quality but is slower

### Batch Processing
- Place multiple video files in the input folder
- Use the combine option to merge them into a single file
- Or process them individually by unchecking the combine option

### Settings Persistence
The program automatically saves your settings to `settings.json`:
- Input/output folder paths
- Processing options (crop, superview, combine)
- Crop values
- On next startup, automatically loads previous settings and scans for files

## Development

### Repository Structure
- Large executables are excluded from git via `.gitignore`
- Dependencies are downloaded automatically via scripts
- Clean separation between source code and binary dependencies

### Contributing
1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project uses HandBrake and Superview CLI tools. Please ensure you comply with their respective licenses.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the processing log for detailed error messages with timestamps
3. Ensure all required files are present in the project directory
4. Check [SETUP.md](SETUP.md) for setup issues 