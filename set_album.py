import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

def set_album_for_mp3s(target_dir, album_name):
    """Set album tag for all MP3 files in the specified directory."""
    if not os.path.isdir(target_dir):
        print(f"Error: Directory not found - {target_dir}")
        return

    mp3_files = [f for f in os.listdir(target_dir) if f.lower().endswith('.mp3')]
    if not mp3_files:
        print(f"No MP3 files found in {target_dir}")
        return

    print(f"Setting album to '{album_name}' for {len(mp3_files)} files in {target_dir}")

    for filename in mp3_files:
        filepath = os.path.join(target_dir, filename)
        try:
            # Try to load existing ID3 tags
            audio = EasyID3(filepath)
        except ID3NoHeaderError:
            # If no tags exist, create new ones
            audio = EasyID3()
        
        # Set the album tag
        audio['album'] = album_name
        audio.save(filepath)
        print(f"Updated: {filename}")

    print("Album tag update complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Set album tag for all MP3 files in a directory')
    parser.add_argument('-t', '--target-dir', required=True, help='Directory containing MP3 files')
    parser.add_argument('-a', '--album', required=True, help='Album name to set')
    
    args = parser.parse_args()
    
    set_album_for_mp3s(args.target_dir, args.album)

