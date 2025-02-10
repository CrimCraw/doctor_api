from django.urls import path
from api.views import DoctorApiView, NewsApiView, DoctorFilterView, RegisterApiView, LoginApiView, DoctorUpdateApiView, \
    UserUpdateView, DoctorDateAPIView, BookingAPIView

urlpatterns = [
    path("register", RegisterApiView.as_view(), name="register"),
    path('doctor', DoctorApiView.as_view(), name='doctors-list'),
    path('doctor/<int:pk>', DoctorApiView.as_view(), name='doctors-detail'),
    path('doctors/<int:pk>/', DoctorUpdateApiView.as_view(), name='doctor-update'),
    path("user/<int:pk>/update", UserUpdateView.as_view(), name='user-update'),
    path("search", DoctorFilterView.as_view(), name='search'),
    path('news', NewsApiView.as_view(), name='news-list'),
    path('news/<int:pk>', NewsApiView.as_view(), name='news-detail'),
    path("login", LoginApiView.as_view(), name="login"),
    path("date/", DoctorDateAPIView.as_view(), name="doctors"),
    path("booking/<int:pk>/", BookingAPIView.as_view(), name="booking"),

]
