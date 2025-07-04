import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import subprocess
import threading
import json
from pathlib import Path
import shutil
import time
import winsound

class CropperviewGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cropperview")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Get the directory where this script is located
        self.script_dir = Path(__file__).parent.absolute()
        
        # Variables
        self.input_files = []
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.use_same_output = tk.BooleanVar(value=False)
        self.combine_videos = tk.BooleanVar(value=True)
        self.enable_crop = tk.BooleanVar(value=True)
        self.enable_superview = tk.BooleanVar(value=True)
        self.crop_values = tk.StringVar(value="0:0:144:148")
        
        # Default paths
        self.input_folder.set("input_videos")
        self.output_folder.set("output_videos")
        
        self.setup_ui()
        self.load_settings()
        
        # Auto-scan on startup if input folder exists
        self.auto_scan_on_startup()
        
    def auto_scan_on_startup(self):
        """Automatically scan for files on startup if input folder exists"""
        input_path = Path(self.input_folder.get())
        if input_path.exists():
            self.log_message("Auto-scanning for video files on startup...")
            self.scan_video_files()
    
    def setup_ui(self):
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Cropperview", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Input Section
        input_frame = ttk.LabelFrame(main_frame, text="Input Files", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="Input Folder:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        input_entry = ttk.Entry(input_frame, textvariable=self.input_folder, width=50)
        input_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(input_frame, text="Browse Folder", command=self.browse_input_folder).grid(row=0, column=2)
        
        # Add file selection button
        ttk.Button(input_frame, text="Select Files", command=self.browse_input_files).grid(row=1, column=2, pady=(5, 0))
        
        # File list
        file_frame = ttk.LabelFrame(main_frame, text="Detected Video Files", padding="10")
        file_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        file_frame.columnconfigure(0, weight=1)
        file_frame.rowconfigure(0, weight=1)
        
        self.file_listbox = tk.Listbox(file_frame, height=6)
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for file list
        file_scrollbar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        file_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        # Output Section
        output_frame = ttk.LabelFrame(main_frame, text="Output Settings", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        # Same output folder checkbox
        same_output_check = ttk.Checkbutton(output_frame, text="Use same folder as input", 
                                          variable=self.use_same_output, command=self.toggle_output_folder)
        same_output_check.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(output_frame, text="Output Folder:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5))
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder, width=50)
        self.output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_folder)
        self.output_browse_btn.grid(row=1, column=2)
        
        # Processing Options
        options_frame = ttk.LabelFrame(main_frame, text="Processing Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Combine videos option
        combine_check = ttk.Checkbutton(options_frame, text="Combine multiple videos (if detected)", 
                                      variable=self.combine_videos)
        combine_check.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Crop option with inline text box
        crop_frame = ttk.Frame(options_frame)
        crop_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        crop_check = ttk.Checkbutton(crop_frame, text="Crop videos", variable=self.enable_crop)
        crop_check.pack(side=tk.LEFT)
        
        ttk.Label(crop_frame, text="Crop (top:bottom:left:right):").pack(side=tk.LEFT, padx=(20, 5))
        crop_entry = ttk.Entry(crop_frame, textvariable=self.crop_values, width=15)
        crop_entry.pack(side=tk.LEFT)
        
        # Superview option
        superview_check = ttk.Checkbutton(options_frame, text="Apply Superview", variable=self.enable_superview)
        superview_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # Process button
        process_btn = ttk.Button(main_frame, text="Start Processing", command=self.start_processing)
        process_btn.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        # Progress and log
        log_frame = ttk.LabelFrame(main_frame, text="Processing Log", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure main frame grid weights
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
    def toggle_output_folder(self):
        if self.use_same_output.get():
            self.output_entry.config(state='disabled')
            self.output_browse_btn.config(state='disabled')
            self.output_folder.set(self.input_folder.get())
        else:
            self.output_entry.config(state='normal')
            self.output_browse_btn.config(state='normal')
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            if self.use_same_output.get():
                self.output_folder.set(folder)
            # Automatically scan for video files when folder is selected
            self.scan_video_files()
    
    def browse_input_files(self):
        """Browse for individual video files"""
        video_extensions = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"),
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi"),
            ("MOV files", "*.mov"),
            ("MKV files", "*.mkv"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=video_extensions
        )
        
        if files:
            self.input_files = list(files)
            # Update file listbox
            self.file_listbox.delete(0, tk.END)
            for file_path in self.input_files:
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
            
            # Set input folder to the directory of the first file
            if self.input_files:
                first_file_dir = str(Path(self.input_files[0]).parent)
                self.input_folder.set(first_file_dir)
                if self.use_same_output.get():
                    self.output_folder.set(first_file_dir)
            
            self.log_message(f"Selected {len(self.input_files)} video file(s)")
            
            # Show combine option if multiple files
            if len(self.input_files) > 1:
                self.log_message("Multiple files detected. You can choose to combine them or process separately.")
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def scan_video_files(self):
        self.log_message("Scanning for video files...")
        input_path = Path(self.input_folder.get())
        
        if not input_path.exists():
            messagebox.showerror("Error", f"Input folder does not exist: {input_path}")
            return
        
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v'}
        self.input_files = []
        
        for file_path in input_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in video_extensions:
                self.input_files.append(str(file_path))
        
        # Update file listbox
        self.file_listbox.delete(0, tk.END)
        for file_path in self.input_files:
            self.file_listbox.insert(tk.END, os.path.basename(file_path))
        
        self.log_message(f"Found {len(self.input_files)} video file(s)")
        
        # Show combine option if multiple files
        if len(self.input_files) > 1:
            self.log_message("Multiple files detected. You can choose to combine them or process separately.")
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def start_processing(self):
        if not self.input_files:
            messagebox.showerror("Error", "No video files found. Please select an input folder or files first.")
            return
        
        # Start processing in a separate thread
        processing_thread = threading.Thread(target=self.process_videos)
        processing_thread.daemon = True
        processing_thread.start()
    
    def process_videos(self):
        try:
            self.progress_var.set(0)
            self.log_message("Starting video processing...")
            
            # Create output directory
            output_path = Path(self.output_folder.get())
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Create temp directory
            temp_path = output_path / "temp"
            temp_path.mkdir(exist_ok=True)
            
            total_steps = len(self.input_files)
            if self.combine_videos.get() and len(self.input_files) > 1:
                total_steps += 1  # Extra step for combining
            
            current_step = 0
            
            # Step 1: Combine videos if requested
            combined_file = None
            if self.combine_videos.get() and len(self.input_files) > 1:
                self.log_message("Combining videos...")
                combined_file = self.combine_videos_handbrake(temp_path)
                current_step += 1
                self.progress_var.set((current_step / total_steps) * 100)
            
            # Step 2: Process each file (or combined file)
            files_to_process = [combined_file] if combined_file else self.input_files
            
            for i, file_path in enumerate(files_to_process):
                self.log_message(f"Processing file {i+1}/{len(files_to_process)}: {os.path.basename(file_path)}")
                
                current_file = file_path
                
                # Step 2a: Crop if enabled
                if self.enable_crop.get():
                    self.log_message("Cropping video...")
                    current_file = self.crop_video(current_file, temp_path)
                
                # Step 2b: Apply superview if enabled
                if self.enable_superview.get():
                    self.log_message("Applying Superview...")
                    current_file = self.apply_superview(current_file, temp_path)
                
                # Move final file to output directory
                final_name = self.generate_output_name(file_path)
                final_path = output_path / final_name
                shutil.move(current_file, final_path)
                self.log_message(f"Final file saved: {final_name}")
                
                current_step += 1
                self.progress_var.set((current_step / total_steps) * 100)
            
            # Clean up temp directory
            if temp_path.exists():
                shutil.rmtree(temp_path)
            
            self.log_message("Processing completed successfully!")
            
            # Play completion chime
            try:
                winsound.MessageBeep(winsound.MB_ICONASTERISK)
            except:
                # Fallback if winsound fails
                pass
            
            messagebox.showinfo("Success", "Video processing completed successfully!")
            
        except Exception as e:
            self.log_message(f"Error during processing: {str(e)}")
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
    
    def combine_videos_handbrake(self, temp_path):
        # Create a file list for HandBrake
        file_list_path = temp_path / "file_list.txt"
        with open(file_list_path, 'w') as f:
            for file_path in self.input_files:
                f.write(f"file '{file_path}'\n")
        
        output_file = temp_path / "combined.mp4"
        
        # Use HandBrake to combine videos - use full path to executable
        handbrake_path = self.script_dir / "HandBrakeCLI.exe"
        
        # Check if executable exists
        if not handbrake_path.exists():
            raise FileNotFoundError(f"HandBrake executable not found at: {handbrake_path}")
        
        cmd = [
            str(handbrake_path),
            "--input-list", str(file_list_path),
            "--output", str(output_file),
            "--format", "mp4",
            "--encoder", "x264",
            "--quality", "20"
        ]
        
        self.log_message(f"Running HandBrake command: {' '.join(cmd)}")
        self.log_message(f"Working directory: {os.getcwd()}")
        self.log_message(f"HandBrake path exists: {handbrake_path.exists()}")
        
        try:
            # Use Popen for real-time output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, cwd=str(self.script_dir), bufsize=1, universal_newlines=True)
            
            for line in process.stdout:
                if line.strip():
                    self.log_message(f"HandBrake: {line.strip()}")
            
            process.wait()
            
            if process.returncode != 0:
                raise Exception(f"HandBrake failed with return code {process.returncode}")
                
        except FileNotFoundError as e:
            raise Exception(f"HandBrake executable not found: {e}")
        except Exception as e:
            raise Exception(f"HandBrake failed: {e}")
        
        return str(output_file)
    
    def crop_video(self, input_file, temp_path):
        input_path = Path(input_file)
        output_file = temp_path / f"{input_path.stem}-cropped{input_path.suffix}"
        
        # Parse crop values (top:bottom:left:right format)
        crop_parts = self.crop_values.get().split(':')
        if len(crop_parts) != 4:
            raise ValueError("Crop values must be in format top:bottom:left:right")
        
        top, bottom, left, right = map(int, crop_parts)
        
        # Use HandBrake for cropping - use full path to executable
        handbrake_path = self.script_dir / "HandBrakeCLI.exe"
        
        # Check if executable exists
        if not handbrake_path.exists():
            raise FileNotFoundError(f"HandBrake executable not found at: {handbrake_path}")
        
        cmd = [
            str(handbrake_path),
            "--input", str(input_file),
            "--output", str(output_file),
            "--format", "mp4",
            "--encoder", "x264",
            "--quality", "20",
            "--crop", f"{top}:{bottom}:{left}:{right}"
        ]
        
        self.log_message(f"Running crop command: {' '.join(cmd)}")
        self.log_message(f"Working directory: {os.getcwd()}")
        self.log_message(f"HandBrake path exists: {handbrake_path.exists()}")
        
        try:
            # Use Popen for real-time output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, cwd=str(self.script_dir), bufsize=1, universal_newlines=True)
            
            for line in process.stdout:
                if line.strip():
                    self.log_message(f"Crop: {line.strip()}")
            
            process.wait()
            
            if process.returncode != 0:
                raise Exception(f"Crop failed with return code {process.returncode}")
                
        except FileNotFoundError as e:
            raise Exception(f"HandBrake executable not found: {e}")
        except Exception as e:
            raise Exception(f"Crop failed: {e}")
        
        return str(output_file)
    
    def apply_superview(self, input_file, temp_path):
        input_path = Path(input_file)
        output_file = temp_path / f"{input_path.stem}-superview{input_path.suffix}"
        
        # Use superview-cli - use full path to executable
        superview_path = self.script_dir / "superview-cli.exe"
        
        # Check if executable exists
        if not superview_path.exists():
            raise FileNotFoundError(f"Superview executable not found at: {superview_path}")
        
        cmd = [
            str(superview_path),
            "/i", str(input_file),
            "/o", str(output_file)
        ]
        
        self.log_message(f"Running Superview command: {' '.join(cmd)}")
        self.log_message(f"Working directory: {os.getcwd()}")
        self.log_message(f"Superview path exists: {superview_path.exists()}")
        
        try:
            # Use Popen for real-time output
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, cwd=str(self.script_dir), bufsize=1, universal_newlines=True)
            
            for line in process.stdout:
                if line.strip():
                    self.log_message(f"Superview: {line.strip()}")
            
            process.wait()
            
            if process.returncode != 0:
                raise Exception(f"Superview failed with return code {process.returncode}")
                
        except FileNotFoundError as e:
            raise Exception(f"Superview executable not found: {e}")
        except Exception as e:
            raise Exception(f"Superview failed: {e}")
        
        return str(output_file)
    
    def generate_output_name(self, input_file):
        input_path = Path(input_file)
        base_name = input_path.stem
        
        # Add suffixes based on processing steps
        if self.combine_videos.get() and len(self.input_files) > 1:
            base_name += "-combined"
        
        if self.enable_crop.get():
            base_name += "-cropped"
        
        if self.enable_superview.get():
            base_name += "-superview"
        
        return f"{base_name}{input_path.suffix}"
    
    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    settings = json.load(f)
                    
                self.input_folder.set(settings.get("input_folder", "input_videos"))
                self.output_folder.set(settings.get("output_folder", "output_videos"))
                self.crop_values.set(settings.get("crop_values", "0:0:144:148"))
                self.enable_crop.set(settings.get("enable_crop", True))
                self.enable_superview.set(settings.get("enable_superview", True))
                self.combine_videos.set(settings.get("combine_videos", True))
        except Exception as e:
            self.log_message(f"Could not load settings: {e}")
    
    def save_settings(self):
        try:
            settings = {
                "input_folder": self.input_folder.get(),
                "output_folder": self.output_folder.get(),
                "crop_values": self.crop_values.get(),
                "enable_crop": self.enable_crop.get(),
                "enable_superview": self.enable_superview.get(),
                "combine_videos": self.combine_videos.get()
            }
            
            with open("settings.json", "w") as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            self.log_message(f"Could not save settings: {e}")

def main():
    root = tk.Tk()
    app = CropperviewGUI(root)
    
    # Save settings when closing
    def on_closing():
        app.save_settings()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 