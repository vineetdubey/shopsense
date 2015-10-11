from shopsense.models import Movie, Genere
from shopsense.serializers import MovieSerializer, GenereSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import  Q

class MoviesList(APIView):
    """
    List all movies, or create a new movies.
    """
    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Post movies with Generes name
        """
        import ipdb;ipdb.set_trace()
        data = request.data
        if data.get('genre'):
            """
            This should have been gone in validation but I couldn't find a way with 
            SlugRelatedField so I added the movie as SlugRelatedField was expecting data.
            """
            genre = [genere.strip() for genere in data.get('genre')]
            genere_list = Genere.objects.filter(name__in = genre)
            if len(genre) != len(genere_list):
                genere_names = [genere.name for genere in genere_list]
                missing_genere = list(set(genre)-set(genere_names))
                error = '%s genere not available.You can add them from genere endpoint.'%(missing_genere)
                return Response([{'error': error}], status=status.HTTP_400_BAD_REQUEST)
            data['genere'] = genere_list
            del(genre)
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MovieDetail(APIView):
    """
    Retrieve a movie details by providing movie name or the director name or the genre.
    param- querystring parameter
    """
    def get_object(self, param):
        try:
            movies_list = Movie.objects.filter(Q(name__icontains = param) | 
                                               Q(director__icontains = param) |
                                               Q(genere__name__icontains = param))
            if movies_list:
                return movies_list
            return None
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request):
        param = request.GET.get('param')
        if param:
            movies_list = self.get_object(param)
            if movies_list:
                serializer = MovieSerializer(movies_list, many=True)
                return Response(serializer.data)
            return Response({"Result:Sorry,No Match Found"})
        return Response({"Result":"No Search Parameter Not Found"})


class GenereList(APIView):
    """
    List all Genere, or create a new Genere.
    """
    def get(self, request):
        genere = Genere.objects.all()
        serializer = GenereSerializer(genere, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GenereSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)