from django.test import TestCase
from .models import Doctor, News
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class DoctorModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="testuser@example.com", password="password123")
        self.doctor = Doctor.objects.create(
            user=self.user,
            speciality="Cardiologist",
            experience=10,
            location="New York",
            clinic_name="Healthy Heart Clinic",
            consultation_fee=100.00,
            is_consultation_free=True,
            available_today=True,
            rating_percentage=95,
            patient_stories=50
        )

    def test_doctor_creation(self):
        self.assertEqual(self.doctor.user.email, "testuser@example.com")
        self.assertEqual(self.doctor.speciality, "Cardiologist")
        self.assertEqual(self.doctor.experience, 10)

    def test_str_method(self):
        self.assertEqual(str(self.doctor), "Cardiologist")

class NewsModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="newsuser@example.com", password="password123")
        self.news = News.objects.create(
            user=self.user,
            title="Breaking News",
            img="news_image.jpg"
        )

    def test_news_creation(self):
        self.assertEqual(self.news.user.email, "newsuser@example.com")
        self.assertEqual(self.news.title, "Breaking News")

    def test_str_method(self):
        self.assertEqual(str(self.news), "Breaking News")
