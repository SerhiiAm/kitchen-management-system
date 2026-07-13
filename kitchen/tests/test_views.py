from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from kitchen.models import Dish, DishType

INDEX_URL = reverse("kitchen:index")
DISH_LIST_URL = reverse("kitchen:dish-list")
DISH_TYPE_LIST_URL = reverse("kitchen:dish-type-list")
COOK_LIST_URL = reverse("kitchen:cook-list")


class PublicTests(TestCase):
    """Tests for unauthenticated users (Public)"""

    def test_index_visit_count_increments(self):
        """Test that the custom visit counter in the session increments correctly"""
        # First visit
        first_response = self.client.get(INDEX_URL)
        self.assertEqual(first_response.context["num_visits"], 1)

        second_response = self.client.get(INDEX_URL)
        self.assertEqual(second_response.context["num_visits"], 2)

    def test_login_required_for_lists(self):
        """Test that access to list views is restricted for unauthenticated users"""
        urls = [DISH_LIST_URL, DISH_TYPE_LIST_URL, COOK_LIST_URL]
        for url in urls:
            response = self.client.get(url)

            self.assertEqual(response.status_code, 302)


class PrivateRegularUserTests(TestCase):
    """Tests for authenticated regular users (without admin/staff permissions)"""

    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="regular_cook",
            password="password123",
            years_of_experience=3,
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Italian")

    def test_retrieve_dishes(self):
        """Test retrieving the list of dishes"""
        Dish.objects.create(name="Pasta", price=10.00, dish_type=self.dish_type)
        Dish.objects.create(name="Pizza", price=12.00, dish_type=self.dish_type)

        response = self.client.get(DISH_LIST_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kitchen/dish_list.html")
        self.assertEqual(len(response.context["dish_list"]), 2)

    def test_search_dishes(self):
        """Test that custom dish search by name works correctly"""
        Dish.objects.create(name="Pasta", price=10.00, dish_type=self.dish_type)
        Dish.objects.create(name="Pizza", price=12.00, dish_type=self.dish_type)

        response = self.client.get(DISH_LIST_URL, {"name": "Pasta"})

        self.assertEqual(len(response.context["dish_list"]), 1)
        self.assertEqual(response.context["dish_list"][0].name, "Pasta")

    def test_search_dish_types(self):
        """Test that custom dish type search by name works correctly"""
        DishType.objects.create(name="Dessert")

        response = self.client.get(DISH_TYPE_LIST_URL, {"name": "Italian"})

        self.assertEqual(len(response.context["dish_types_list"]), 1)
        self.assertEqual(response.context["dish_types_list"][0].name, "Italian")

    def test_search_cooks(self):
        """Test that custom cook search by username works correctly"""
        get_user_model().objects.create_user(
            username="chef_mario", password="password123", years_of_experience=10
        )

        response = self.client.get(COOK_LIST_URL, {"username": "mario"})

        self.assertEqual(len(response.context["cook_list"]), 1)
        self.assertEqual(response.context["cook_list"][0].username, "chef_mario")

    def test_toggle_assign_to_dish_forbidden_for_regular_user(self):
        """Test that a regular user is redirected when trying to toggle dish assignment"""
        dish = Dish.objects.create(name="Soup", price=5.00, dish_type=self.dish_type)
        url = reverse("kitchen:toggle-dish-assign", args=[dish.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        dish.refresh_from_db()
        self.assertNotIn(self.user, dish.cooks.all())

    def test_dish_delete_forbidden_for_regular_user(self):
        """Test that a regular user receives a 403 Forbidden status when attempting to delete a dish"""
        dish = Dish.objects.create(name="Delete me", price=1.00, dish_type=self.dish_type)
        url = reverse("kitchen:dish-delete", args=[dish.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)


class PrivateAdminUserTests(TestCase):
    """Tests for users with Admin / Staff permissions"""

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_user(
            username="admin_chef",
            password="password123",
            is_staff=True,
            years_of_experience=15,
        )
        self.client.force_login(self.admin_user)
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(name="Steak", price=25.00, dish_type=self.dish_type)

    def test_toggle_assign_to_dish_success_for_admin(self):
        """Test that an administrator can successfully assign and unassign themselves from a dish"""
        url = reverse("kitchen:toggle-dish-assign", args=[self.dish.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertIn(self.admin_user, self.dish.cooks.all())

        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertNotIn(self.admin_user, self.dish.cooks.all())

    def test_dish_delete_allowed_for_admin(self):
        """Test that an administrator can successfully delete a dish"""
        url = reverse("kitchen:dish-delete", args=[self.dish.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)

        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())
