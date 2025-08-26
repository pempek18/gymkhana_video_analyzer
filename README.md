# Gymkhana Video Analyzer

A professional video analysis tool designed specifically for comparing motorcycle gymkhana videos. This application allows you to upload two videos and analyze them side-by-side with advanced synchronization and shadow overlay capabilities.

## Features

- **Dual Video Upload**: Upload two separate gymkhana videos for comparison
- **Side-by-Side Display**: View both videos simultaneously in separate panels
- **Timeline Synchronization**: Precise control over video timing with adjustable sync offset
- **Shadow Overlay**: Create a shadow effect by blending the second video over the first
- **Adjustable Shadow Opacity**: Control the intensity of the shadow effect (0.0 to 1.0)
- **Playback Controls**: Play, pause, seek to first/last frame, and adjust playback speed
- **Professional Timeline**: Visual timeline slider for easy navigation through videos
- **Frame-by-Frame Analysis**: Detailed frame and time information display
- **Video Export**: Export shadow videos (blended videos) from specific time ranges
- **Quick Time Ranges**: Predefined export ranges and current position ±5s option

## Installation

### Prerequisites
- Python 3.7 or higher
- Windows 10/11 (tested on Windows 10)

### Setup
1. Clone or download this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application
1. Run the main application:
   ```bash
   python app.py
   ```

### Loading Videos
1. Click "Upload Video 1 (Main)" to select your primary gymkhana video
2. Click "Upload Video 2 (Shadow)" to select your comparison video
3. Both videos will be loaded and displayed side-by-side

### Video Synchronization
- **Sync Offset**: Adjust the timing offset between videos (in seconds)
  - Positive values: Second video plays ahead of first video
  - Negative values: Second video plays behind first video
  - Range: -60 to +60 seconds

### Shadow Effect
- **Shadow Opacity**: Control how much the second video overlays the first
  - 0.0: No shadow effect (only first video visible)
  - 0.5: Equal blend of both videos
  - 1.0: Only second video visible

### Video Export
- **Time Range Selection**: Specify start and end times for export (in seconds)
- **Quick Ranges**: Use predefined ranges (0-10s, 10-30s, 30-60s)
- **Current Position**: Export ±5 seconds around current playback position
- **Export Format**: Save as MP4 or AVI with original video quality
- **Progress Tracking**: Real-time export progress with status updates

### Playback Controls
- **⏮ First Frame**: Jump to the beginning of the video
- **⏯ Play/Pause**: Start or stop video playback
- **⏭ Last Frame**: Jump to the end of the video
- **Timeline Slider**: Drag to navigate to any position in the video
- **Playback Speed**: Choose from 0.25x, 0.5x, 1.0x, 1.5x, or 2.0x

### Analysis Workflow
1. Load both videos
2. Adjust sync offset to align key moments
3. Use shadow opacity to highlight differences
4. Navigate through the timeline to analyze specific sections
5. Use playback speed controls for detailed frame-by-frame analysis
6. Export specific time ranges for further analysis or sharing

### Export Workflow
1. **Set Time Range**: Use spinboxes or quick range buttons
2. **Adjust Settings**: Ensure sync offset and shadow opacity are set correctly
3. **Export**: Click "Export Shadow Video" and choose output location
4. **Monitor Progress**: Watch progress bar and status updates
5. **Save Result**: Exported video maintains synchronization and shadow effects

## Supported Video Formats
- MP4
- AVI
- MOV
- MKV
- And other formats supported by OpenCV

## Technical Details

### Architecture
- **GUI Framework**: Tkinter with ttk widgets for modern appearance
- **Video Processing**: OpenCV for video capture and frame manipulation
- **Image Processing**: PIL/Pillow for image conversion and display
- **Synchronization**: Frame-accurate timing with configurable offsets
- **Export System**: Multi-threaded video export with progress tracking

### Performance
- Optimized for real-time video playback
- Efficient memory management for large video files
- Responsive GUI with smooth timeline navigation
- Background video export to prevent GUI freezing

## Use Cases

### Gymkhana Training
- Compare your runs with reference videos
- Analyze technique differences frame-by-frame
- Study line choices and timing
- Export key sections for detailed review

### Competition Analysis
- Review competitor performances
- Identify key differences in approach
- Plan strategy improvements
- Create comparison clips for team analysis

### Coaching and Instruction
- Provide visual feedback to students
- Demonstrate proper technique
- Track progress over time
- Export training examples for offline study

### Content Creation
- Create highlight reels with shadow effects
- Export synchronized comparison videos
- Generate training materials with overlays
- Share analysis results with team members

## Troubleshooting

### Common Issues
1. **Video won't load**: Ensure video format is supported and file isn't corrupted
2. **Poor performance**: Close other applications to free up system resources
3. **Sync issues**: Use the sync offset to fine-tune video alignment
4. **Export fails**: Check available disk space and ensure output directory is writable

### System Requirements
- Minimum 4GB RAM
- Dedicated graphics card recommended for HD videos
- Sufficient storage space for video files and exports
- Multi-core processor recommended for video export

## Contributing

This application is designed for gymkhana enthusiasts and motorsport professionals. Feel free to suggest improvements or report issues.

## License

This project is open source and available under the MIT License.

---

**Note**: This application is specifically designed for gymkhana video analysis and may not be suitable for other types of video comparison tasks.
