from django.db import models
from mutagen.id3 import ID3, TIT2, TPE1, TALB, USLT, APIC
from mutagen.mp3 import MP3

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True, null=True)
    lyrics = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='songs/')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Guardar normalmente primero
        super().save(*args, **kwargs)

        # Ahora agregamos los metadatos ID3
        if self.file:
            file_path = self.file.path
            audio = MP3(file_path, ID3=ID3)

            # Si no tiene tags, los crea
            if not audio.tags:
                audio.add_tags()

            # Añadir título, artista, álbum
            audio.tags.add(TIT2(encoding=3, text=self.title))
            audio.tags.add(TPE1(encoding=3, text=self.artist))
            if self.album:
                audio.tags.add(TALB(encoding=3, text=self.album))

            # Añadir letra (si existe)
            if self.lyrics:
                audio.tags.add(USLT(encoding=3, lang='spa', desc='Lyrics', text=self.lyrics))

            # Añadir imagen (portada)
            if self.cover:
                with open(self.cover.path, 'rb') as img:
                    audio.tags.add(APIC(
                        encoding=3,  # utf-8
                        mime='image/jpeg',  # o 'image/png' si es png
                        type=3,  # portada delantera
                        desc='Cover',
                        data=img.read()
                    ))

            # Guardar los cambios en el archivo mp3
            audio.save(v2_version=3)
