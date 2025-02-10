from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import Doctor, News, User, Date
from api.serializers import DoctorSerializer, NewsSerializer, RegisterSerializer, LoginSerializer, \
    DoctorUpdateSerializer, UserSerializer, BookingSerializer, DateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated


class UserUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(
        request=UserSerializer,
        responses={200: "User updated successfully"}
    )
    def put(self, requests, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(instance=user, data=requests.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User update successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    @extend_schema(
        summary="User Login",
        description="Login using email and password to obtain JWT tokens.",
        request=LoginSerializer,
        responses={
            200: OpenApiParameter(name="Tokens", description="JWT  access  and refresh tokens"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials or validation errors"),
        },
        tags=["User Authentication"]
    )

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = User.objects.get(email=email)
            if user.check_password(password):
                if not user.is_active:
                    return Response({"detail": "User account is inactive"}, status=status.HTTP_400_BAD_REQUEST)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                return Response({
                    "refresh": str(refresh),
                    "access": access_token
                }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(password=make_password(serializer.validated_data['password']))
            #Generate JWT tokens

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": access_token,
                    "user" : serializer.data
                },status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DoctorApiView(APIView):
    throttle_classes = (AnonRateThrottle,)

    permission_classes = [IsAuthenticated]


    def get(self,request, pk=None):
        if pk:
            try:
                item = Doctor.objects.get(pk=pk)
                serializer = DoctorSerializer(item)
                return Response(serializer.data)
            except:
                return Response({'error': 'Doc not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)


class DoctorUpdateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
        summary="Doctor Update",
        description="Doctor update data",
        request=DoctorUpdateSerializer,  # Specify request body fields
        responses={
            200: OpenApiParameter(name="Update", description="Doctor update data"),
            400: OpenApiParameter(name="Errors", description="Invalid credentials or validation errors"),
        },
        tags=["Doctor Update"]
    )
    def put(self, request, pk):
        doctor = get_object_or_404(Doctor, pk=pk)
        serializer = DoctorUpdateSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=400)


class NewsApiView(APIView):
    throttle_classes = (AnonRateThrottle,)
    def get(self,request,pk=None):
        if pk:
            try:
                item = News.objects.get(pk=pk)
                serializer = NewsSerializer(item)
                return Response(serializer.data)
            except:
                return Response({'error': 'News not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            news = News.objects.all()
            serializer = NewsSerializer(news, many=True)
            return Response(serializer.data)


class DoctorFilterView(ListAPIView):
    serializer_class = DoctorSerializer
    queryset = Doctor.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['location', 'clinic_name']
    filterset_fields = ['experience', 'rating_percentage', 'consultation_fee', 'location']


class DoctorDateAPIView(APIView):
    def get(self, request):
        date = Date.objects.filter(status='pending')
        serializer = DateSerializer(date, many=True)
        return Response(serializer.data)


class BookingAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        Date.objects.filter(pk=pk, status='pending').update(user=user, status='confirmed')
        try:
            date = Date.objects.get(pk=pk, status='confirmed')
        except Date.DoesNotExist:
            return Response({"error": "Date not found or not pending"}, status=404)

        serializer = BookingSerializer(date)
        return Response(serializer.data)
