import os
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess

def convert_flac_to_mp3(flac_path, output_dir=None, delete_original=False):
    """
    Convert a single FLAC file to MP3 (320 kbps) using ffmpeg.
    
    Args:
        flac_path (Path): Path to the FLAC file
        output_dir (Path, optional): Directory to save MP3. If None, uses same directory as FLAC.
        delete_original (bool): Whether to delete the original FLAC file after conversion.
    """
    # Determine output path
    if output_dir is None:
        output_dir = flac_path.parent
    else:
        output_dir = Path(output_dir) / flac_path.parent.relative_to(flac_path.parent.anchor)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    mp3_path = output_dir / f"{flac_path.stem}.mp3"
    
    try:
        # Convert using ffmpeg
        subprocess.run([
            'ffmpeg',
            '-i', str(flac_path),
            '-codec:a', 'libmp3lame',
            '-q:a', '0',  # 0 = highest quality (320 kbps)
            '-id3v2_version', '3',
            '-loglevel', 'warning',
            '-y',  # Overwrite without asking
            str(mp3_path)
        ], check=True)
        
        print(f"Converted: {flac_path} -> {mp3_path}")
        
        if delete_original:
            flac_path.unlink()
            print(f"Deleted original: {flac_path}")
            
    except subprocess.CalledProcessError as e:
        print(f"Error converting {flac_path}: {e}")
    except Exception as e:
        print(f"Unexpected error with {flac_path}: {e}")

def find_flac_files(directory):
    """
    Recursively find all FLAC files in a directory.
    """
    directory = Path(directory)
    return list(directory.rglob('*.flac'))

def main():
    parser = argparse.ArgumentParser(description='Convert FLAC files to MP3 (320 kbps)')
    parser.add_argument('directory', help='Directory to search for FLAC files')
    parser.add_argument('--output', '-o', help='Output directory (default: same as input)')
    parser.add_argument('--delete', '-d', action='store_true', 
                        help='Delete original FLAC files after conversion')
    parser.add_argument('--threads', '-t', type=int, default=4,
                        help='Number of parallel threads to use (default: 4)')
    
    args = parser.parse_args()
    
    # Check if ffmpeg is available
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: ffmpeg is not installed. Please install ffmpeg first.")
        return
    
    flac_files = find_flac_files(args.directory)
    
    if not flac_files:
        print(f"No FLAC files found in {args.directory}")
        return
    
    print(f"Found {len(flac_files)} FLAC files to convert")
    
    # Convert files in parallel
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        for flac_file in flac_files:
            executor.submit(convert_flac_to_mp3, flac_file, args.output, args.delete)
    
    print("Conversion complete!")

if __name__ == '__main__':
    main()

