from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Dish, DishType

DISH_LIST_URL = reverse("kitchen:dish-list")


class PublicDishTests(TestCase):
    def test_login_required(self):
        """Test that list of dishes is login required"""
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 302)


class PrivateDishTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="test_user",
            password="password123",
            years_of_experience=5,
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main")

    def test_retrieve_dishes(self):
        """Test that dishes can be retrieved"""
        Dish.objects.create(name="Pasta", price=10.00, dish_type=self.dish_type)
        Dish.objects.create(name="Pizza", price=12.00, dish_type=self.dish_type)

        response = self.client.get(DISH_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_list.html")
        self.assertEqual(len(response.context["dish_list"]), 2)

    def test_search_dishes(self):
        """Test that dish search works"""
        Dish.objects.create(name="Pasta", price=10.00, dish_type=self.dish_type)
        Dish.objects.create(name="Pizza", price=12.00, dish_type=self.dish_type)

        response = self.client.get(DISH_LIST_URL, {"name": "Pasta"})

        self.assertEqual(len(response.context["dish_list"]), 1)
        self.assertEqual(response.context["dish_list"][0].name, "Pasta")

    def test_toggle_assign_to_dish_forbidden_for_regular_user(self):
        """Test that regular user cannot toggle assignment"""

        self.user.is_superuser = False
        self.user.save()

        dish = Dish.objects.create(name="Soup", price=5.00, dish_type=self.dish_type)
        url = reverse("kitchen:toggle-dish-assign", args=[dish.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

        dish.refresh_from_db()
        self.assertNotIn(self.user, dish.cooks.all())

    def test_dish_delete_forbidden_for_regular_user(self):
        """Test that a regular user receives 403 Forbidden when trying to delete a dish"""
        dish = Dish.objects.create(name="Delete me", price=1.00, dish_type=self.dish_type)
        url = reverse("kitchen:dish-delete", args=[dish.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
