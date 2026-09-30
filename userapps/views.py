from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            return Response({'error': str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


