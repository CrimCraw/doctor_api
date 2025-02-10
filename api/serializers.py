from rest_framework import serializers
from api.models import Doctor, News, User, Date
from root import settings

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'roles')


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Doctor
        fields = ['user','id', 'speciality', 'experience', 'location', 'clinic_name', 'consultation_fee', 'is_consultation_free', 'available_today', 'rating_percentage', 'patient_stories']

        def get_avatar(self, obj):
            if obj.img:
                return settings.BASE_URL + obj.img.url
            return None

class NewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    img = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ['user','title', 'img', 'created_at']

    def get_img(self, obj):
        if obj.img:
            return settings.BASE_URL + obj.img.url
        return None

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class DoctorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['speciality', 'experience', 'location', 'clinic_name', 'consultation_fee',
                  'is_consultation_free', 'available_today', 'rating_percentage', 'patient_stories']

class DateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Date
        fields = ['id', 'user', 'doctor', 'date', 'time', 'status']


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Date
        fields = ['id', 'user', 'doctor', 'date', 'time', 'status']


