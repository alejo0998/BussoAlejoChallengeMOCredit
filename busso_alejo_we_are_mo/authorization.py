from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
import random
import string


def generate_random_string(length=10):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class ApiKeyCreationView(APIView):
    def post(self, request):
        api_key, key = APIKey.objects.create_key(name=generate_random_string())  # Esto generará una API Key sin asociarla a un usuario específico
        return Response({'api_key': f'Api-Key {key}'}, status=status.HTTP_201_CREATED)