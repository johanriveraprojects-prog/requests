from django.urls import path

from . import views

app_name = "passes"

urlpatterns = [
    path("", views.pass_list, name="list"),
    path("nuevo/", views.pass_create, name="create"),
    path("<int:pk>/", views.pass_detail, name="detail"),
    path("<int:pk>/descargar.pkpass", views.pass_download, name="download"),
    path("<int:pk>/imagenes.zip", views.pass_images, name="images"),
    path("<int:pk>/img/<str:name>", views.pass_image, name="image"),
]
