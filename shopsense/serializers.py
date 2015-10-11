from rest_framework import serializers
from shopsense.models import Movie, Genere

class MovieSerializer(serializers.ModelSerializer):
    genere = serializers.SlugRelatedField(many=True, queryset=Genere.objects.all(), slug_field='name')
    
    class Meta:
        model = Movie
        fields = ('popularity', 'director', 'name', 'imdb_score', 'genere')

class GenereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genere
        fields = ('name',)