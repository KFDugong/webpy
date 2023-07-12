from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("comment/<int:pk>/", views.comment_detail, name="comment_detail"),
    path("comment/<int:pk>/update/", views.comment_update, name="comment_update"),
    path("comment/<int:pk>/delete/", views.comment_delete, name="comment_delete"),
    path("comment/<int:pk>/feedback/<int:feedback>", views.comment_feedback, name='comment_feedback'),
    path("rating/<int:pk>/", views.rating_detail, name="rating_detail"),
    path("rating/<int:pk>/update/", views.rating_update, name="rating_update"),
    path("rating/<int:pk>/delete/", views.rating_delete, name="rating_delete"),
    path("comment/<int:pk>/toggle_hidden/", views.comment_toggle_hidden, name="comment_toggle_hidden"),
]
