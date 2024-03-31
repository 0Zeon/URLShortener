import hashlib
from django.db import models
from django.db.utils import IntegrityError

class ShortLink(models.Model):
    originUrl = models.URLField(max_length=2048)
    shortUrl = models.CharField(max_length=255, unique=True, blank=True)
    hash = models.CharField(max_length=10, unique=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    isDeleted = models.BooleanField(default=False)

    def generate_hash(self, url, count=0):
        hash_value = hashlib.md5((url + str(count)).encode()).hexdigest()[:10]
        return hash_value

    def save(self, *args, **kwargs):
        if not self.hash:
            count = 0
            while True:
                self.hash = self.generate_hash(self.originUrl, count)
                self.shortUrl = f"http://localhost:8000/short-links/{self.hash}"
                try:
                    super(ShortLink, self).save(*args, **kwargs)
                    break
                except IntegrityError:
                    count += 1