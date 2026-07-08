from django.urls import path

from kitchen.views import (
    index, DishTypeListView, DishTypeCreateView,
    DishTypeUpdateView, DishTypeDeleteView, DishListView,
)

app_name = "kitchen"

urlpatterns = [
    path("", index, name="index"),
    path("dish-type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-type/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-type/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-type/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dish/", DishListView.as_view(), name="dish-list"),

]
