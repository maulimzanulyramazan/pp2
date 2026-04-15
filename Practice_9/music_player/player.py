import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.music_folder = music_folder
        self.playlist = self.load_music()
        self.current_index = 0
        self.is_playing = False

    def load_music(self):
        files = []
        for file in os.listdir(self.music_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                files.append(os.path.join(self.music_folder, file))
        return files

    def play(self):
        if not self.playlist:
            print("No music files found.")
            return

        track = self.playlist[self.current_index]
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True
        print(f"Now playing: {os.path.basename(track)}")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        print("Playback stopped.")

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def prev_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

