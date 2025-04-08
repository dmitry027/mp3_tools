import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3NoHeaderError

def rename_mp3_files():
    # Get all mp3 files in the current directory
    mp3_files = [f for f in os.listdir('.') if f.lower().endswith('.mp3')]
    
    for filename in mp3_files:
        try:
            # Load the MP3 file and its ID3 tags
            audio = EasyID3(filename)
            
            # Get title and artist (default to empty string if tag doesn't exist)
            title = audio.get('title', [''])[0].strip()
            artist = audio.get('artist', [''])[0].strip()
            
            if not title and not artist:
                print(f"Skipping {filename}: No title or artist tags found")
                continue
                
            # Create new filename
            new_filename = f"{title} - {artist}.mp3"
            
            # Sanitize filename (replace invalid characters)
            invalid_chars = '<>:"/\\|?*'
            for char in invalid_chars:
                new_filename = new_filename.replace(char, '_')
            
            # Rename the file
            if filename != new_filename:
                try:
                    os.rename(filename, new_filename)
                    print(f"Renamed: {filename} -> {new_filename}")
                except OSError as e:
                    print(f"Error renaming {filename}: {e}")
            
        except ID3NoHeaderError:
            print(f"Skipping {filename}: No ID3 tags found")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    print("Starting MP3 file renaming...")
    rename_mp3_files()
    print("Done!")
