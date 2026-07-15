from django.urls import path

from kitchen.views import (
    IndexView, DishTypeListView, DishTypeCreateView,
    DishTypeUpdateView, DishTypeDeleteView, DishListView,
    DishDetailView, DishCreateView, DishUpdateView,
    DishDeleteView, ToggleAssignToDishView, CookListView,
    CookDetailView, CookCreateView, CookUpdateView,
    CookDeleteView, DishTypeDetailView,
)

app_name = "kitchen"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("dish-type/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish-types/<int:pk>/", DishTypeDetailView.as_view(), name="dish-type-detail"),
    path("dish-type/create/", DishTypeCreateView.as_view(), name="dish-type-create"),
    path("dish-type/<int:pk>/update/", DishTypeUpdateView.as_view(), name="dish-type-update"),
    path("dish-type/<int:pk>/delete/", DishTypeDeleteView.as_view(), name="dish-type-delete"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("dish/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
    path("dish/create/", DishCreateView.as_view(), name="dish-create"),
    path("dish/<int:pk>/update/", DishUpdateView.as_view(), name="dish-update"),
    path("dish/<int:pk>/delete/", DishDeleteView.as_view(), name="dish-delete"),
    path("dish/<int:pk>/toggle-assign/", ToggleAssignToDishView.as_view(), name="toggle-dish-assign"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"),
    path("cook/create/", CookCreateView.as_view(), name="cook-create"),
    path("cook/<int:pk>/update/", CookUpdateView.as_view(), name="cook-update"),
    path("cook/<int:pk>/delete/", CookDeleteView.as_view(), name="cook-delete"),

]
