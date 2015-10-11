from django.db import models


class Genere(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    popularity = models.DecimalField(blank=True, max_digits=4, decimal_places=2)
    director = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    imdb_score = models.DecimalField(blank=True, max_digits=2, decimal_places=1)
    created_on = models.DateTimeField(auto_now_add=True)
    genere = models.ManyToManyField(Genere)
    updated_on = models.DateTimeField(auto_now_add=False, blank=True, null=True, default=None)

        
