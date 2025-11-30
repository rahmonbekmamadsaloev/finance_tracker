from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializer import  RegisterSerializer, LoginSerializer, RefreshSerializer, LogoutSerializer




class RegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]



class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh_token = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh_token),"access": str(refresh_token.access_token)}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class RefreshAPIView(generics.GenericAPIView):
    serializer_class = RefreshSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get("token")

        try:
            refresh = RefreshToken(token)
            new_access = refresh.access_token

            return Response( {"refresh": str(refresh),"access": str(new_access)},status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid refresh token"},status=status.HTTP_400_BAD_REQUEST)



class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data.get("token")

        try:
            refresh = RefreshToken(token)
            refresh.blacklist()
            return Response({"detail": "Successfully logged out"},status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"detail": "Failed to process token"},status=status.HTTP_400_BAD_REQUEST)
