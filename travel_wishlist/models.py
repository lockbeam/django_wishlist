from django.db import models

# Used to create a Place table in the database
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, visited? {self.visited}'

