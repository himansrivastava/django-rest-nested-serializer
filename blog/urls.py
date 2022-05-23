from django.urls import path

from blog import views

app_name = "blog"

urlpatterns = [
    path("", views.UserAPIListView.as_view(), name="list"),
    path("<int:pk>/", views.UserAPIDetailView.as_view(), name="detail"),
    path(
        "comment/",
        views.CommentAPIListView.as_view(),
        name="comment_list",
    ),
    path(
        "comment/<int:pk>/",
        views.CommentAPIDetailView.as_view(),
        name="comment_detail",
    ),
]
