from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=200)         # Título de la canción
    artist = models.CharField(max_length=200)        # Artista
    album = models.CharField(max_length=200, blank=True, null=True)  # Álbum (opcional)
    lyrics = models.TextField(blank=True, null=True) # Letra (opcional)
    file = models.FileField(upload_to='songs/')      # Archivo mp3
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de subida automática

    def __str__(self):
        return self.title
