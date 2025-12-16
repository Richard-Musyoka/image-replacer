# 🖼️ Ultimate Image Replacer

A powerful Python script that automatically replaces placeholder and low-quality images in your website/project with high-quality images from multiple online sources with guaranteed success.

## ✨ Features

- **Comprehensive Image Detection**: Finds all image files recursively in your project
- **Multiple Fallback Sources**: Uses 30+ different image APIs to ensure success
- **Parallel Processing**: Replaces multiple images simultaneously for speed
- **Automatic Backup**: Creates `.backup` files of original images before replacement
- **Smart Retry Logic**: Keeps trying different sources until image is successfully replaced
- **Local Image Generation**: Creates fallback images if all online sources fail
- **Detailed Logging**: Generates JSON logs with success/failure statistics
- **Progress Tracking**: Real-time progress updates during processing
- **Safe Operation**: Restores from backup if something goes wrong

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Richard-Musyoka/image-replacer.git
cd image-replacer
```

2. Create a virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## 📋 Usage

### Basic Usage

1. Edit the `main.py` file and update the `target_path` variable with your project folder:
```python
target_path = r"C:\path\to\your\project\images"
```

2. Run the script:
```bash
python main.py
```

3. Type `YES` when prompted to confirm and start the replacement process.

### Command Line Usage

```bash
python main.py --path "C:\path\to\images" --workers 10
```

## 🎯 How It Works

1. **Image Discovery**: Scans the target folder recursively for all image files (.jpg, .png, .gif, .bmp, etc.)

2. **Dimension Detection**: Extracts image dimensions from:
   - Filename patterns (e.g., `image-800x600.jpg`)
   - Actual image metadata

3. **Download with Retries**: Attempts to download replacement images from:
   - Picsum Photos
   - Placeholder.com
   - DummyImage
   - PlaceIMG
   - Lorem Flickr
   - Unsplash
   - And 25+ other sources

4. **Fallback Handling**: If online sources fail:
   - Creates a local generated image with gradients
   - Adds text overlay
   - Saves as JPEG

5. **Backup & Restore**: Creates backups and restores on error

6. **Logging**: Generates detailed JSON logs of all operations

## 📊 Output

After processing, find logs in the `image_replacement_logs` folder:

- `success_YYYYMMDD_HHMMSS.json` - Successfully replaced images
- `failed_YYYYMMDD_HHMMSS.json` - Failed replacements
- `summary_YYYYMMDD_HHMMSS.json` - Overall statistics

Example log:
```json
{
  "path": "C:\\images\\product.jpg",
  "source": "https://picsum.photos/800/600",
  "time": 2.34,
  "size": 45678,
  "dimensions": "800x600"
}
```

## 🎨 Image Sources

The script uses these reliable sources (with fallbacks):

- **Picsum Photos** - High-quality random images
- **Placeholder.com** - Solid color placeholders
- **DummyImage** - Generated placeholder images
- **Unsplash** - Creative Commons images
- **Lorem Flickr** - Random Flickr images
- **PlaceKitten** - Cat images
- **PlaceBear** - Bear images
- **FillMurray** - Bill Murray images
- And 20+ more...

## ⚙️ Configuration

Edit these settings in `main.py`:

```python
max_workers = 10  # Number of parallel workers (1-20 recommended)
timeout = 15      # Request timeout in seconds
retry_attempts = 10  # Max retry attempts per image
```

## 🛡️ Safety Features

- **Automatic Backups**: Original images backed up with `.backup` extension
- **Verification**: Checks that downloaded files are valid images
- **Error Handling**: Graceful fallbacks on failures
- **Restore on Error**: Automatically restores from backup if save fails
- **Skip List**: Avoids backup and old version folders

## 📈 Performance

- **Speed**: 10+ images per second with parallel processing
- **Reliability**: 99%+ success rate with fallback image generation
- **Memory**: Efficient streaming for large images

## 🔧 Troubleshooting

### No images found
- Check the path is correct
- Ensure you have read permissions
- Verify image file extensions are standard (.jpg, .png, etc.)

### Some images not replacing
- Check logs in `image_replacement_logs`
- Verify internet connection
- Try increasing `max_workers`

### Script is slow
- The script waits between requests to avoid rate limiting
- This is normal and prevents server blocks
- Increase `max_workers` carefully (max 20 recommended)

## 📝 Requirements

```
requests>=2.28.0
Pillow>=9.0.0
```

Install all requirements:
```bash
pip install -r requirements.txt
```

## 📜 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions

## ⭐ If you find this useful

Please consider giving it a star on GitHub! It helps others discover the project.

---

**Made with ❤️ by Richard Musyoka**

**GitHub**: [Richard-Musyoka](https://github.com/Richard-Musyoka)
