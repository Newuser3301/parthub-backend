from django.urls import path
from b2b.views import MyB2BProfileView, B2BPostListCreateView, B2BPostRetrieveUpdateDestroyView

urlpatterns = [
    path("b2b/me/", MyB2BProfileView.as_view()),

    path("b2b/posts/", B2BPostListCreateView.as_view()),
    path("b2b/posts/<int:pk>/", B2BPostRetrieveUpdateDestroyView.as_view()),
]
