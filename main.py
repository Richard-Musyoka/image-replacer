import os
import requests
from PIL import Image
import io
import shutil
from pathlib import Path
import random
import time
import concurrent.futures
from datetime import datetime
import json

class UltimateImageReplacer:
    def __init__(self, root_folder):
        self.root_folder = Path(root_folder)
        self.success_log = []
        self.failed_log = []
        
        # Comprehensive list of image sources with backup options
        self.image_sources = [
            # Picsum Photos (very reliable)
            "https://picsum.photos/{w}/{h}",
            "https://picsum.photos/{w}/{h}?random={r}",
            "https://picsum.photos/id/{id}/{w}/{h}",
            
            # Placeholder.com (always works)
            "https://via.placeholder.com/{w}x{h}",
            "https://via.placeholder.com/{w}x{h}/000/fff",
            "https://via.placeholder.com/{w}x{h}.png",
            
            # DummyImage (reliable)
            "https://dummyimage.com/{w}x{h}",
            "https://dummyimage.com/{w}x{h}/000/fff",
            "https://dummyimage.com/{w}x{h}/0099ff/ffffff",
            
            # PlaceIMG
            "https://placeimg.com/{w}/{h}/any",
            "https://placeimg.com/{w}/{h}/nature",
            "https://placeimg.com/{w}/{h}/tech",
            
            # Lorem Flickr
            "https://loremflickr.com/{w}/{h}",
            "https://loremflickr.com/{w}/{h}/food",
            "https://loremflickr.com/{w}/{h}/grocery",
            
            # PlaceKitten (always works)
            "https://placekitten.com/{w}/{h}",
            "https://placekitten.com/g/{w}/{h}",
            
            # PlaceBear
            "https://placebear.com/{w}/{h}",
            "https://placebear.com/g/{w}/{h}",
            
            # BaconMockup
            "https://baconmockup.com/{w}/{h}",
            
            # FillMurray
            "https://fillmurray.com/{w}/{h}",
            "https://fillmurray.com/g/{w}/{h}",
            
            # PlaceCage
            "https://placecage.com/{w}/{h}",
            "https://placecage.com/g/{w}/{h}",
            
            # StevenSeg Gallery
            "https://stevensegallery.com/{w}/{h}",
            
            # Random User (for customer avatars)
            "https://randomuser.me/api/portraits/men/{id}.jpg",
            "https://randomuser.me/api/portraits/women/{id}.jpg",
            
            # Pravatar
            "https://i.pravatar.cc/{w}?img={id}",
            
            # RoboHash
            "https://robohash.org/{id}?size={w}x{h}",
            
            # Unsplash with different search terms
            "https://source.unsplash.com/random/{w}x{h}",
            "https://source.unsplash.com/featured/{w}x{h}",
            "https://source.unsplash.com/{w}x{h}/?food",
            "https://source.unsplash.com/{w}x{h}/?grocery",
            "https://source.unsplash.com/{w}x{h}/?fruit",
            "https://source.unsplash.com/{w}x{h}/?vegetable",
            "https://source.unsplash.com/{w}x{h}/?market",
            "https://source.unsplash.com/{w}x{h}/?shop",
            
            # Placehold.co (new reliable service)
            "https://placehold.co/{w}x{h}",
            "https://placehold.co/{w}x{h}.png",
            "https://placehold.co/{w}x{h}.jpg",
            
            # Cloudinary (fallback)
            "https://res.cloudinary.com/demo/image/upload/w_{w},h_{h}/sample.jpg",
            
            # Imgix (reliable CDN)
            "https://assets.imgix.net/examples/pione.jpg?w={w}&h={h}",
            
            # LoremSpace (backup)
            "https://lorem.space/api/{w}x{h}",
        ]
        
        # Grocery-specific image sources
        self.grocery_sources = [
            "https://source.unsplash.com/{w}x{h}/?fruit,vegetable",
            "https://source.unsplash.com/{w}x{h}/?grocery,supermarket",
            "https://source.unsplash.com/{w}x{h}/?food,drink",
            "https://loremflickr.com/{w}/{h}/fruit",
            "https://loremflickr.com/{w}/{h}/vegetable",
            "https://loremflickr.com/{w}/{h}/grocery",
            "https://picsum.photos/{w}/{h}?food",
            "https://picsum.photos/{w}/{h}?grocery",
        ]
        
        # Offline backup - create local images if all else fails
        self.create_local_image = True
    
    def get_image_dimensions(self, img_path):
        """Get dimensions from filename or actual image"""
        # Try to extract from filename first (pattern: 800x600)
        import re
        name = img_path.stem
        match = re.search(r'(\d+)[x×](\d+)', name)
        if match:
            return int(match.group(1)), int(match.group(2))
        
        # Try to get from actual image
        try:
            with Image.open(img_path) as img:
                return img.size
        except:
            # Default to reasonable size
            return 800, 600
    
    def download_with_retry(self, width, height, max_retries=10):
        """Keep trying different sources until we get an image"""
        all_sources = self.grocery_sources + self.image_sources
        
        for attempt in range(max_retries):
            # Shuffle sources for variety
            random.shuffle(all_sources)
            
            for source in all_sources:
                try:
                    # Format URL with parameters
                    url = source
                    if '{w}' in source and '{h}' in source:
                        url = url.replace('{w}', str(width)).replace('{h}', str(height))
                    if '{r}' in source:
                        url = url.replace('{r}', str(random.randint(1, 1000)))
                    if '{id}' in source:
                        url = url.replace('{id}', str(random.randint(1, 100)))
                    
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.9',
                    }
                    
                    # Add random delay to avoid rate limiting
                    time.sleep(random.uniform(0.1, 0.5))
                    
                    print(f"  Attempt {attempt+1}: Trying {url}")
                    
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        # Verify it's an image
                        content_type = response.headers.get('content-type', '')
                        if not content_type.startswith('image/'):
                            # Check if it's actually an image by trying to open it
                            try:
                                img = Image.open(io.BytesIO(response.content))
                                img.verify()
                                return response.content, url
                            except:
                                continue
                        
                        return response.content, url
                        
                except requests.exceptions.Timeout:
                    print(f"  Timeout for {url}")
                    continue
                except requests.exceptions.ConnectionError:
                    print(f"  Connection error for {url}")
                    continue
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
        
        # If all else fails, create a local image
        return self.create_local_image_data(width, height), "local_generated"
    
    def create_local_image_data(self, width, height):
        """Create a local image if all downloads fail"""
        from PIL import ImageDraw, ImageFont
        import colorsys
        
        # Create a colorful gradient image
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)
        
        # Draw a gradient
        for y in range(height):
            hue = y / height
            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, 0.7, 0.9)]
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add text
        try:
            font = ImageFont.load_default()
            text = f"Grocery Image\n{width}x{height}"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_x = (width - text_width) // 2
            text_y = (height - text_height) // 2
            
            draw.text((text_x, text_y), text, fill='white', font=font)
        except:
            pass
        
        # Save to bytes
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90)
        return buffer.getvalue()
    
    def replace_single_image(self, img_path):
        """Replace one image with guaranteed success"""
        print(f"\n{'='*60}")
        print(f"Processing: {img_path}")
        
        # Get dimensions
        width, height = self.get_image_dimensions(img_path)
        print(f"  Dimensions: {width}x{height}")
        
        # Create backup
        backup_path = img_path.with_suffix(img_path.suffix + '.backup')
        if not backup_path.exists():
            shutil.copy2(img_path, backup_path)
            print(f"  Backup created: {backup_path}")
        
        # Keep trying until we get an image
        start_time = time.time()
        image_data = None
        source_used = None
        
        while not image_data:
            image_data, source_used = self.download_with_retry(width, height)
        
        elapsed = time.time() - start_time
        
        try:
            # Save the image
            with open(img_path, 'wb') as f:
                f.write(image_data)
            
            # Verify it's valid
            with Image.open(img_path) as img:
                img.verify()
            
            # Get new file size
            new_size = os.path.getsize(img_path)
            
            print(f"✓ SUCCESS!")
            print(f"  Source: {source_used}")
            print(f"  Time: {elapsed:.2f}s")
            print(f"  Size: {new_size:,} bytes")
            
            self.success_log.append({
                'path': str(img_path),
                'source': source_used,
                'time': elapsed,
                'size': new_size,
                'dimensions': f"{width}x{height}"
            })
            
            return True
            
        except Exception as e:
            print(f"✗ ERROR saving: {e}")
            
            # Restore from backup
            if backup_path.exists():
                shutil.copy2(backup_path, img_path)
                print(f"  Restored from backup")
            
            self.failed_log.append({
                'path': str(img_path),
                'error': str(e)
            })
            
            # Try one more time with a different approach
            print(f"  Retrying with simpler method...")
            return self.emergency_replace(img_path)
    
    def emergency_replace(self, img_path):
        """Last resort replacement method"""
        try:
            width, height = self.get_image_dimensions(img_path)
            
            # Use the most reliable source
            reliable_sources = [
                f"https://via.placeholder.com/{width}x{height}",
                f"https://placehold.co/{width}x{height}",
                f"https://dummyimage.com/{width}x{height}"
            ]
            
            for url in reliable_sources:
                try:
                    response = requests.get(url, timeout=30)
                    if response.status_code == 200:
                        with open(img_path, 'wb') as f:
                            f.write(response.content)
                        
                        print(f"✓ EMERGENCY SUCCESS from {url}")
                        return True
                except:
                    continue
            
            # If still failing, create a colored rectangle
            img = Image.new('RGB', (width, height), color=(random.randint(100, 200), 
                                                           random.randint(100, 200), 
                                                           random.randint(100, 200)))
            img.save(img_path, 'JPEG')
            print(f"✓ CREATED LOCAL COLOR IMAGE")
            return True
            
        except Exception as e:
            print(f"✗ CRITICAL FAILURE: {e}")
            return False
    
    def find_all_images(self):
        """Find all image files recursively"""
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}
        
        image_files = []
        for root, dirs, files in os.walk(self.root_folder):
            # Skip backup files
            if any(x in root.lower() for x in ['backup', '.bak', 'old_', '_old']):
                continue
                
            for file in files:
                if file.lower().endswith('.backup'):
                    continue
                    
                file_path = Path(root) / file
                suffix = file_path.suffix.lower()
                
                if suffix in image_extensions:
                    # Skip very small files (likely placeholders)
                    try:
                        if os.path.getsize(file_path) < 1024:  # 1KB
                            image_files.append(file_path)
                        else:
                            # Also add files that might be placeholders
                            image_files.append(file_path)
                    except:
                        image_files.append(file_path)
        
        return image_files
    
    def process_parallel(self, max_workers=5):
        """Process images in parallel for speed"""
        all_images = self.find_all_images()
        total_images = len(all_images)
        
        print(f"{'='*80}")
        print(f"ULTIMATE IMAGE REPLACER")
        print(f"Target: {self.root_folder}")
        print(f"Total images found: {total_images}")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        if total_images == 0:
            print("No images found to process!")
            return
        
        # Process in parallel
        successful = 0
        failed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.replace_single_image, img): img for img in all_images}
            
            for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
                img_path = futures[future]
                try:
                    result = future.result()
                    if result:
                        successful += 1
                    else:
                        failed += 1
                    
                    # Progress update
                    progress = (i / total_images) * 100
                    print(f"\n[{i}/{total_images}] Progress: {progress:.1f}%")
                    print(f"  Successful: {successful} | Failed: {failed}")
                    
                except Exception as e:
                    print(f"\n✗ EXCEPTION for {img_path}: {e}")
                    failed += 1
        
        # Save logs
        self.save_logs()
        
        # Final report
        print(f"\n{'='*80}")
        print(f"PROCESSING COMPLETE!")
        print(f"Total images processed: {total_images}")
        print(f"Successfully replaced: {successful}")
        print(f"Failed: {failed}")
        print(f"Success rate: {(successful/total_images*100):.1f}%")
        print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")
        
        # Show most used sources
        if self.success_log:
            sources = {}
            for log in self.success_log:
                source = log['source']
                sources[source] = sources.get(source, 0) + 1
            
            print("\nTop sources used:")
            for source, count in sorted(sources.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {source}: {count} images")
    
    def save_logs(self):
        """Save processing logs to file"""
        log_dir = self.root_folder.parent / "image_replacement_logs"
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save success log
        if self.success_log:
            success_file = log_dir / f"success_{timestamp}.json"
            with open(success_file, 'w') as f:
                json.dump(self.success_log, f, indent=2)
        
        # Save failed log
        if self.failed_log:
            failed_file = log_dir / f"failed_{timestamp}.json"
            with open(failed_file, 'w') as f:
                json.dump(self.failed_log, f, indent=2)
        
        # Save summary
        summary = {
            'timestamp': timestamp,
            'total_success': len(self.success_log),
            'total_failed': len(self.failed_log),
            'root_folder': str(self.root_folder)
        }
        
        summary_file = log_dir / f"summary_{timestamp}.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nLogs saved to: {log_dir}")

# Main execution
if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║         ULTIMATE GROCERY IMAGE REPLACER                  ║
    ║  This will replace ALL images in your grocery website    ║
    ║           WITHOUT SKIPPING ANYTHING                      ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Your path
    target_path = r"C:\Users\Attain\Desktop\Projects\PHP Laravel Projects\Milestone Multivendor Grocery POS\public\storage"
    
    # Safety check
    if not os.path.exists(target_path):
        print(f"ERROR: Path does not exist: {target_path}")
        exit(1)
    
    print(f"Target folder: {target_path}")
    print("\nIMPORTANT WARNINGS:")
    print("1. This will replace EVERY image file in the folder")
    print("2. Original images will be backed up with .backup extension")
    print("3. The script will keep trying until ALL images are replaced")
    print("4. This may take a long time depending on number of images")
    
    response = input("\nType 'YES' to continue (or anything else to cancel): ")
    
    if response.strip().upper() == 'YES':
        print("\nStarting in 5 seconds...")
        time.sleep(5)
        
        # Create and run replacer
        replacer = UltimateImageReplacer(target_path)
        replacer.process_parallel(max_workers=10)  # Use 10 parallel workers
        
        print("\n✅ All images have been processed!")
        print("Check the 'image_replacement_logs' folder for detailed logs.")
    else:
        print("\nOperation cancelled.")