"""Batch Processor - Watch folder and automatically process PDFs"""
import os
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class PDFProcessor(FileSystemEventHandler):
    """Watch a folder and process PDFs automatically."""
    
    def __init__(self, watch_dir, output_dir, action="compress"):
        self.watch_dir = Path(watch_dir)
        self.output_dir = Path(output_dir)
        self.action = action
        self.processed = set()
        
    def on_created(self, event):
        """Handle new file creation."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        if file_path.suffix.lower() == ".pdf" and file_path not in self.processed:
            print(f"New PDF detected: {file_path}")
            self.process_pdf(file_path)
            self.processed.add(file_path)
    
    def process_pdf(self, input_path):
        """Process PDF based on configured action."""
        output_path = self.output_dir / input_path.name
        
        try:
            if self.action == "compress":
                from compress import compress_pdf
                compress_pdf(str(input_path), str(output_path))
                print(f"Compressed: {input_path.name} -> {output_path.name}")
                
            elif self.action == "watermark":
                from watermark import add_watermark
                add_watermark(str(input_path), str(output_path), text="BATCH PROCESSED")
                print(f"Watermarked: {input_path.name} -> {output_path.name}")
                
            elif self.action == "split":
                from split import split_pdf
                split_pdf(str(input_path), str(self.output_dir / "split"))
                print(f"Split: {input_path.name}")
                
        except Exception as e:
            print(f"Error processing {input_path.name}: {e}")


def watch_folder(watch_dir, output_dir, action="compress"):
    """
    Watch a folder for new PDFs and process them.
    
    Args:
        watch_dir: Directory to watch for new PDFs
        output_dir: Directory to save processed PDFs
        action: Action to perform (compress, watermark, split)
    """
    event_handler = PDFProcessor(watch_dir, output_dir, action)
    observer = Observer()
    
    observer.schedule(event_handler, str(watch_dir), recursive=False)
    observer.start()
    
    print(f"Watching {watch_dir} for new PDFs...")
    print(f"Action: {action}")
    print(f"Output: {output_dir}")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Batch PDF Processor")
    parser.add_argument("watch_dir", help="Directory to watch")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("--action", default="compress", 
                       choices=["compress", "watermark", "split"],
                       help="Action to perform")
    
    args = parser.parse_args()
    
    watch_folder(args.watch_dir, args.output_dir, args.action)

