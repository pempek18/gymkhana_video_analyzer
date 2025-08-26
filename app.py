import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
import threading
import time
import os
from pathlib import Path

class GymkhanaVideoAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gymkhana Video Analyzer")
        self.root.geometry("1400x1000")
        
        # Video variables
        self.video1_path = None
        self.video2_path = None
        self.video1_cap = None
        self.video2_cap = None
        self.video1_fps = 0
        self.video2_fps = 0
        self.video1_total_frames = 0
        self.video2_total_frames = 0
        self.video1_duration = 0
        self.video2_duration = 0
        
        # Playback variables
        self.current_frame = 0
        self.is_playing = False
        self.sync_offset = 0  # Time offset between videos
        self.shadow_opacity = 0.5
        
        # Export variables
        self.is_exporting = False
        self.export_progress = 0
        
        # GUI setup
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top control panel
        self.setup_control_panel(main_frame)
        
        # Video display area
        self.setup_video_display(main_frame)
        
        # Export controls
        self.setup_export_controls(main_frame)
        
        # Timeline and controls
        self.setup_timeline_controls(main_frame)
        
    def setup_control_panel(self, parent):
        control_frame = ttk.LabelFrame(parent, text="Video Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Video upload buttons
        upload_frame = ttk.Frame(control_frame)
        upload_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(upload_frame, text="Upload Video 1 (Main)", 
                  command=self.upload_video1).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(upload_frame, text="Upload Video 2 (Shadow)", 
                  command=self.upload_video2).pack(side=tk.LEFT, padx=(0, 10))
        
        # Video info labels
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(fill=tk.X)
        
        self.video1_info = ttk.Label(info_frame, text="Video 1: Not loaded")
        self.video1_info.pack(side=tk.LEFT, padx=(0, 20))
        
        self.video2_info = ttk.Label(info_frame, text="Video 2: Not loaded")
        self.video2_info.pack(side=tk.LEFT)
        
        # Playback controls
        playback_frame = ttk.Frame(control_frame)
        playback_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(playback_frame, text="⏮", command=self.first_frame, width=3).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(playback_frame, text="⏯", command=self.play_pause, width=3).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(playback_frame, text="⏭", command=self.last_frame, width=3).pack(side=tk.LEFT, padx=(0, 5))
        
        # Sync offset control
        ttk.Label(playback_frame, text="Sync Offset (s):").pack(side=tk.LEFT, padx=(20, 5))
        self.offset_var = tk.DoubleVar(value=0.0)
        
        # Create validation command
        vcmd = (self.root.register(self.validate_sync_offset), '%P')
        
        offset_spin = ttk.Spinbox(playback_frame, from_=-60, to=60, increment=0.1, 
                                 textvariable=self.offset_var, width=8, format="%.1f",
                                 validate='key', validatecommand=vcmd)
        offset_spin.pack(side=tk.LEFT, padx=(0, 10))
        offset_spin.bind('<KeyRelease>', self.update_sync_offset)
        offset_spin.bind('<FocusOut>', self.update_sync_offset)  # Update when focus is lost
        offset_spin.bind('<Return>', self.update_sync_offset)    # Update when Enter is pressed
        offset_spin.bind('<ButtonRelease-1>', self.update_sync_offset)  # Update when using arrows
        
        # Shadow opacity control
        ttk.Label(playback_frame, text="Shadow Opacity:").pack(side=tk.LEFT, padx=(20, 5))
        self.opacity_var = tk.DoubleVar(value=0.5)
        opacity_scale = ttk.Scale(playback_frame, from_=0.0, to=1.0, 
                                 variable=self.opacity_var, orient=tk.HORIZONTAL, length=100)
        opacity_scale.pack(side=tk.LEFT, padx=(0, 10))
        opacity_scale.bind('<ButtonRelease-1>', self.update_shadow_opacity)
        
    def setup_video_display(self, parent):
        video_frame = ttk.LabelFrame(parent, text="Video Comparison", padding=10)
        video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Video display area
        display_frame = ttk.Frame(video_frame)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Main video display
        self.video1_canvas = tk.Canvas(display_frame, bg="black", width=640, height=360)
        self.video1_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Shadow video display
        self.video2_canvas = tk.Canvas(display_frame, bg="black", width=640, height=360)
        self.video2_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Labels for video displays
        ttk.Label(display_frame, text="Main Video", anchor="center").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Label(display_frame, text="Shadow Video", anchor="center").pack(side=tk.RIGHT, padx=(5, 0))
        
    def setup_export_controls(self, parent):
        export_frame = ttk.LabelFrame(parent, text="Export Shadow Video", padding=10)
        export_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Time range inputs
        time_range_frame = ttk.Frame(export_frame)
        time_range_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(time_range_frame, text="Start Time (s):").pack(side=tk.LEFT, padx=(0, 5))
        self.start_time_var = tk.DoubleVar(value=0.0)
        start_time_spin = ttk.Spinbox(time_range_frame, from_=0.0, to=999.0, increment=0.1,
                                     textvariable=self.start_time_var, width=8)
        start_time_spin.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(time_range_frame, text="End Time (s):").pack(side=tk.LEFT, padx=(0, 5))
        self.end_time_var = tk.DoubleVar(value=10.0)
        end_time_spin = ttk.Spinbox(time_range_frame, from_=0.1, to=999.0, increment=0.1,
                                   textvariable=self.end_time_var, width=8)
        end_time_spin.pack(side=tk.LEFT, padx=(0, 20))
        
        # Export button and progress
        export_controls_frame = ttk.Frame(export_frame)
        export_controls_frame.pack(fill=tk.X)
        
        self.export_button = ttk.Button(export_controls_frame, text="Export Shadow Video", 
                                       command=self.export_shadow_video)
        self.export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_progress_bar = ttk.Progressbar(export_controls_frame, mode='determinate', length=200)
        self.export_progress_bar.pack(side=tk.LEFT, padx=(0, 10))
        
        self.export_status_label = ttk.Label(export_controls_frame, text="Ready to export")
        self.export_status_label.pack(side=tk.LEFT)
        
        # Quick time range buttons
        quick_range_frame = ttk.Frame(export_frame)
        quick_range_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(quick_range_frame, text="Quick Ranges:").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(quick_range_frame, text="0-10s", command=lambda: self.set_time_range(0, 10)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_range_frame, text="10-30s", command=lambda: self.set_time_range(10, 30)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_range_frame, text="30-60s", command=lambda: self.set_time_range(30, 60)).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(quick_range_frame, text="Current Position ±5s", command=self.set_current_range).pack(side=tk.LEFT, padx=(0, 5))
        
    def setup_timeline_controls(self, parent):
        timeline_frame = ttk.LabelFrame(parent, text="Timeline & Synchronization", padding=10)
        timeline_frame.pack(fill=tk.X)
        
        # Timeline slider
        self.timeline_var = tk.DoubleVar()
        self.timeline_slider = ttk.Scale(timeline_frame, from_=0, to=100, 
                                        variable=self.timeline_var, orient=tk.HORIZONTAL)
        self.timeline_slider.pack(fill=tk.X, pady=(0, 10))
        self.timeline_slider.bind('<ButtonRelease-1>', self.seek_to_position)
        
        # Time display and frame info
        time_frame = ttk.Frame(timeline_frame)
        time_frame.pack(fill=tk.X)
        
        self.time_label = ttk.Label(time_frame, text="Time: 00:00 / 00:00")
        self.time_label.pack(side=tk.LEFT)
        
        self.frame_label = ttk.Label(time_frame, text="Frame: 0 / 0")
        self.frame_label.pack(side=tk.RIGHT)
        
        # Speed control
        speed_frame = ttk.Frame(timeline_frame)
        speed_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(speed_frame, text="Playback Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_combo = ttk.Combobox(speed_frame, textvariable=self.speed_var, 
                                  values=[0.25, 0.5, 1.0, 1.5, 2.0], width=8, state="readonly")
        speed_combo.pack(side=tk.LEFT, padx=(5, 0))
        speed_combo.bind('<<ComboboxSelected>>', self.update_playback_speed)
        
    def upload_video1(self):
        file_path = filedialog.askopenfilename(
            title="Select Main Video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        if file_path:
            self.load_video(file_path, 1)
            
    def upload_video2(self):
        file_path = filedialog.askopenfilename(
            title="Select Shadow Video",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")]
        )
        if file_path:
            self.load_video(file_path, 2)
            
    def load_video(self, file_path, video_num):
        try:
            cap = cv2.VideoCapture(file_path)
            if not cap.isOpened():
                messagebox.showerror("Error", f"Could not open video {video_num}")
                return
                
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration = total_frames / fps if fps > 0 else 0
            
            if video_num == 1:
                if self.video1_cap:
                    self.video1_cap.release()
                self.video1_cap = cap
                self.video1_path = file_path
                self.video1_fps = fps
                self.video1_total_frames = total_frames
                self.video1_duration = duration
                self.video1_info.config(text=f"Video 1: {Path(file_path).name} ({duration:.1f}s)")
            else:
                if self.video2_cap:
                    self.video2_cap.release()
                self.video2_cap = cap
                self.video2_path = file_path
                self.video2_fps = fps
                self.video2_total_frames = total_frames
                self.video2_duration = duration
                self.video2_info.config(text=f"Video 2: {Path(file_path).name} ({duration:.1f}s)")
                
            # Update timeline if both videos are loaded
            if self.video1_cap and self.video2_cap:
                self.update_timeline()
                self.display_current_frame()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading video: {str(e)}")
            
    def update_timeline(self):
        if not (self.video1_cap and self.video2_cap):
            return
            
        # Use the longer video duration for timeline
        max_duration = max(self.video1_duration, self.video2_duration)
        self.timeline_slider.config(to=max_duration)
        
    def display_current_frame(self):
        if not (self.video1_cap and self.video2_cap):
            return
            
        # Calculate frame numbers for both videos
        time1 = self.current_frame / self.video1_fps
        time2 = time1 + self.sync_offset
        
        frame1 = int(time1 * self.video1_fps)
        frame2 = int(time2 * self.video2_fps)
        
        # Ensure frame numbers are within bounds
        frame1 = max(0, min(frame1, self.video1_total_frames - 1))
        frame2 = max(0, min(frame2, self.video2_total_frames - 1))
        
        # Read frames
        self.video1_cap.set(cv2.CAP_PROP_POS_FRAMES, frame1)
        self.video2_cap.set(cv2.CAP_PROP_POS_FRAMES, frame2)
        
        ret1, frame1_img = self.video1_cap.read()
        ret2, frame2_img = self.video2_cap.read()
        
        if ret1 and ret2:
            # Resize frames to fit canvas
            frame1_img = cv2.resize(frame1_img, (640, 360))
            frame2_img = cv2.resize(frame2_img, (640, 360))
            
            # Convert BGR to RGB
            frame1_rgb = cv2.cvtColor(frame1_img, cv2.COLOR_BGR2RGB)
            frame2_rgb = cv2.cvtColor(frame2_img, cv2.COLOR_BGR2RGB)
            
            # Create shadow effect by blending frames
            shadow_frame = cv2.addWeighted(frame1_rgb, 1 - self.shadow_opacity, 
                                         frame2_rgb, self.shadow_opacity, 0)
            
            # Convert to PIL Image and then to PhotoImage
            pil_img1 = Image.fromarray(frame1_rgb)
            pil_shadow = Image.fromarray(shadow_frame)
            
            self.photo1 = ImageTk.PhotoImage(pil_img1)
            self.photo_shadow = ImageTk.PhotoImage(pil_shadow)
            
            # Display on canvases
            self.video1_canvas.create_image(320, 180, image=self.photo1, anchor=tk.CENTER)
            self.video2_canvas.create_image(320, 180, image=self.photo_shadow, anchor=tk.CENTER)
            
        # Update time and frame labels
        current_time = self.current_frame / self.video1_fps
        max_time = max(self.video1_duration, self.video2_duration)
        
        self.time_label.config(text=f"Time: {current_time:.1f}s / {max_time:.1f}s")
        self.frame_label.config(text=f"Frame: {frame1} / {self.video1_total_frames}")
        
    def play_pause(self):
        if not (self.video1_cap and self.video2_cap):
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_video()
            
    def play_video(self):
        if not self.is_playing:
            return
            
        # Calculate delay based on speed
        delay = 1.0 / (self.video1_fps * self.speed_var.get())
        
        # Update frame
        self.current_frame += 1
        if self.current_frame >= self.video1_total_frames:
            self.current_frame = 0
            
        # Update timeline slider
        self.timeline_var.set(self.current_frame / self.video1_fps)
        
        # Display frame
        self.display_current_frame()
        
        # Schedule next frame
        self.root.after(int(delay * 1000), self.play_video)
        
    def first_frame(self):
        self.current_frame = 0
        self.timeline_var.set(0)
        self.display_current_frame()
        
    def last_frame(self):
        if self.video1_cap:
            self.current_frame = self.video1_total_frames - 1
            self.timeline_var.set(self.video1_duration)
            self.display_current_frame()
            
    def seek_to_position(self, event=None):
        if not (self.video1_cap and self.video2_cap):
            return
            
        time_pos = self.timeline_var.get()
        self.current_frame = int(time_pos * self.video1_fps)
        self.display_current_frame()
        
    def update_sync_offset(self, event=None):
        """Update sync offset with error handling"""
        try:
            # Get the current value and validate it
            value = self.offset_var.get()
            if isinstance(value, (int, float)):
                self.sync_offset = value
                self.display_current_frame()
            else:
                # If the value is not a number, try to convert it
                try:
                    self.sync_offset = float(value)
                    self.display_current_frame()
                except (ValueError, TypeError):
                    # If conversion fails, reset to previous valid value
                    self.offset_var.set(self.sync_offset)
        except Exception as e:
            # If any error occurs, reset to previous valid value
            print(f"Sync offset error: {e}")
            self.offset_var.set(self.sync_offset)
    
    def validate_sync_offset(self, P):
        """Validate sync offset input to prevent invalid characters"""
        if P == "":  # Allow empty string
            return True
        if P == "-":  # Allow minus sign
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False
        
    def update_shadow_opacity(self, event=None):
        self.shadow_opacity = self.opacity_var.get()
        self.display_current_frame()
        
    def update_playback_speed(self, event=None):
        # Speed will be applied on next play
        pass
        
    def on_closing(self):
        if self.video1_cap:
            self.video1_cap.release()
        if self.video2_cap:
            self.video2_cap.release()
        self.root.destroy()

    def set_time_range(self, start, end):
        """Set the export time range"""
        self.start_time_var.set(start)
        self.end_time_var.set(end)
        
    def set_current_range(self):
        """Set export range around current position"""
        if self.video1_cap:
            current_time = self.current_frame / self.video1_fps
            start_time = max(0, current_time - 5)
            end_time = min(self.video1_duration, current_time + 5)
            self.set_time_range(start_time, end_time)
        
    def export_shadow_video(self):
        """Export the shadow video (blended video) for the specified time range"""
        if not (self.video1_cap and self.video2_cap):
            messagebox.showerror("Error", "Please load both videos first")
            return
            
        start_time = self.start_time_var.get()
        end_time = self.end_time_var.get()
        
        if start_time >= end_time:
            messagebox.showerror("Error", "Start time must be less than end time")
            return
            
        if end_time > self.video1_duration:
            messagebox.showerror("Error", f"End time exceeds video duration ({self.video1_duration:.1f}s)")
            return
            
        # Ask for output file
        output_path = filedialog.asksaveasfilename(
            title="Save Shadow Video As",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*")]
        )
        
        if not output_path:
            return
            
        # Start export in separate thread
        self.is_exporting = True
        self.export_button.config(state='disabled')
        self.export_status_label.config(text="Exporting...")
        self.export_progress_bar['value'] = 0
        
        export_thread = threading.Thread(target=self._export_video_thread, 
                                       args=(output_path, start_time, end_time))
        export_thread.daemon = True
        export_thread.start()
        
    def _export_video_thread(self, output_path, start_time, end_time):
        """Export video in separate thread to avoid GUI freezing"""
        try:
            # Calculate frame ranges
            start_frame1 = int(start_time * self.video1_fps)
            end_frame1 = int(end_time * self.video1_fps)
            
            start_frame2 = int((start_time + self.sync_offset) * self.video2_fps)
            end_frame2 = int((end_time + self.sync_offset) * self.video2_fps)
            
            # Ensure frame numbers are within bounds
            start_frame1 = max(0, min(start_frame1, self.video1_total_frames - 1))
            end_frame1 = max(0, min(end_frame1, self.video1_total_frames - 1))
            start_frame2 = max(0, min(start_frame2, self.video2_total_frames - 1))
            end_frame2 = max(0, min(end_frame2, self.video2_total_frames - 1))
            
            # Get video properties
            width = int(self.video1_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(self.video1_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, self.video1_fps, (width, height))
            
            total_frames = end_frame1 - start_frame1
            current_frame = 0
            
            # Export frames
            for frame_num in range(start_frame1, end_frame1):
                # Read frame from video 1
                self.video1_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
                ret1, frame1 = self.video1_cap.read()
                
                if not ret1:
                    continue
                    
                # Calculate corresponding frame in video 2
                frame2_num = start_frame2 + (frame_num - start_frame1)
                if frame2_num < self.video2_total_frames:
                    self.video2_cap.set(cv2.CAP_PROP_POS_FRAMES, frame2_num)
                    ret2, frame2 = self.video2_cap.read()
                    
                    if ret2:
                        # Resize frame2 to match frame1 dimensions
                        frame2 = cv2.resize(frame2, (width, height))
                        
                        # Create shadow effect
                        shadow_frame = cv2.addWeighted(frame1, 1 - self.shadow_opacity, 
                                                     frame2, self.shadow_opacity, 0)
                        
                        # Write frame
                        out.write(shadow_frame)
                    else:
                        # If video 2 frame can't be read, use only video 1
                        out.write(frame1)
                else:
                    # If video 2 frame is out of bounds, use only video 1
                    out.write(frame1)
                
                # Update progress
                current_frame += 1
                progress = (current_frame / total_frames) * 100
                
                # Update GUI (must be done in main thread)
                self.root.after(0, self._update_export_progress, progress)
                
            # Clean up
            out.release()
            
            # Export complete
            self.root.after(0, self._export_complete, output_path)
            
        except Exception as e:
            self.root.after(0, self._export_error, str(e))
            
    def _update_export_progress(self, progress):
        """Update export progress bar"""
        self.export_progress_bar['value'] = progress
        self.export_status_label.config(text=f"Exporting... {progress:.1f}%")
        
    def _export_complete(self, output_path):
        """Handle export completion"""
        self.is_exporting = False
        self.export_button.config(state='normal')
        self.export_status_label.config(text="Export complete!")
        self.export_progress_bar['value'] = 100
        
        messagebox.showinfo("Export Complete", 
                          f"Shadow video exported successfully!\nSaved to: {output_path}")
        
    def _export_error(self, error_msg):
        """Handle export error"""
        self.is_exporting = False
        self.export_button.config(state='normal')
        self.export_status_label.config(text="Export failed")
        self.export_progress_bar['value'] = 0
        
        messagebox.showerror("Export Error", f"Failed to export video: {error_msg}")

def main():
    root = tk.Tk()
    app = GymkhanaVideoAnalyzer(root)
    
    # Set up closing handler
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()
