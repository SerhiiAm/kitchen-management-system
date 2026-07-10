from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from kitchen.models import DishType, Dish

class ModelsTests(TestCase):
    def test_dish_type_str(self):
        dish_type = DishType.objects.create(name="Pizza")
        self.assertEqual(str(dish_type), "Pizza")

    def test_cook_str(self):
        cook = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            first_name="John",
            last_name="Doe",
            years_of_experience=5,
        )
        self.assertEqual(str(cook), "test_user (John Doe)")

    def test_cook_get_absolute_url(self):
        cook = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            years_of_experience=5,
        )
        self.assertEqual(cook.get_absolute_url(), reverse("kitchen:cook-detail", kwargs={"pk": cook.pk}))

    def test_dish_str(self):
        dish_type = DishType.objects.create(name="Main Course")
        dish = Dish.objects.create(
            name="Pasta Carbonara",
            description="Classic Italian pasta",
            price="12.99",
            dish_type=dish_type,
        )
        self.assertEqual(str(dish), "Pasta Carbonara")

    def test_create_cook_with_experience(self):
        username = "chef_pro"
        years = 10
        cook = get_user_model().objects.create_user(
            username=username,
            years_of_experience=years
        )
        self.assertEqual(cook.username, username)
        self.assertEqual(cook.years_of_experience, years)