from django.db import models
# below allows us to add built in Foreign Key
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

# Used to create a Place table in the database
class Place(models.Model):
    user = models.ForeignKey('auth.User', null=False, on_delete=models.CASCADE) # delete associated places
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True ) # null and blank = True - we're not requiring an input if the user doesn't have a photo

    # below overrides Django's built in save method allows us to do what we want and then continue with the usuaul save route
    def save(self, *args, **kwargs):
        old_place = Place.objects.filter(pk=self.pk).first() # pull up snapshot of old database
        if old_place and old_place.photo: # checking to see if a photo already exists within the old place
            if old_place.photo != self.photo: # if a photo exists and it isn't the new photo ,
                self.delete_photo(old_place.photo) # delete the old photo

        super().save(*args, **kwargs)

    def delete_photo(self, photo):
        if default_storage.exists(photo.name): # check to see if a photo exists
            default_storage.delete(photo.name)

    # below overrides Django's built in delete path
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)

        super().delete(*args, **kwargs)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo :('
        notes_str = self.notes[100:] if self.notes else 'no notes :(' #truncate notes to first 100 characters
        return f'{self.name}, visited? {self.visited} on {self.date_visited}. Notes: {notes_str}. Photo {photo_str}'

