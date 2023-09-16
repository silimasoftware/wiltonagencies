from django.urls import path
from .views import Portal, Logout, Login


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("", Portal.as_view(), name="portal"),
    path("<slug:module>/", Portal.as_view(), name="portal"),
    path("<slug:module>/<slug:page>/", Portal.as_view(), name="portal"),
]
