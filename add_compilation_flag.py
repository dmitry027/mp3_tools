import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, TCMP

def add_compilation_flag_easyid3():
    mp3_files = [f for f in os.listdir('.') if f.lower().endswith('.mp3')]

    for filename in mp3_files:
        try:
            # First try EasyID3 for basic tags
            audio = EasyID3(filename)

            # Then use low-level ID3 for TCMP
            id3 = ID3(filename)
            id3.add(TCMP(encoding=3, text='1'))
            id3.save()

            print(f"Added compilation flag to: {filename}")

        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    print("Starting to add compilation flags...")
    add_compilation_flag_easyid3()
    print("Done!")
