from django.core.mail import send_mail
import secrets
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework import status

from users.serializers import UserSerializer


User = get_user_model()


class Get_token(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        
        try:
            user = User.objects.filter(email=email, confirmation_code=confirmation_code).exists()
            user.is_active = True
            
            def get_tokens_for_user(self, user):
                refresh = RefreshToken.for_user(user)
                token = str(refresh.access_token)
                return token
            return Response (("Ваш токен: " + get_tokens_for_user(user)))
        
        except User.DoesNotExist:
            return Response("Пользователь не найден или код подтверждения не верный")


class RegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.data.get('email')
            username = serializer.data.get('username')
            confirmation_code = secrets.token_hex(9)
            User.objects.create_user(
                email=email, username=username, confirmation_code=confirmation_code
            )
            
            send_mail(
                'Registration',
                'Your confirmation code is ' + str(confirmation_code),
                'from@gmail.com',
                [str(email)],
                fail_silently=False,
            )
            return Response("Код подтверждения выслан вам на почту ")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

