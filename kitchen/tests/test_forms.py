from django.test import TestCase
from kitchen.forms import DishForm, CookCreationForm, CookExperienceUpdateForm
from kitchen.models import DishType
from django.contrib.auth import get_user_model

class FormTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_dish_form_is_valid(self):
        cook = get_user_model().objects.create_user(
            username="cook1", years_of_experience=1
        )

        form_data = {
            "name": "Pasta",
            "description": "Tasty pasta",
            "price": "10.00",
            "dish_type": self.dish_type.id,
            "cooks": [cook.id],
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_creation_form_is_valid(self):
        """Test that CookCreationForm is valid with correct data"""
        form_data = {
            "username": "new_cook",
            "password1": "password123!@",
            "password2": "password123!@",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_experience_update_form_validation(self):
        """Test custom validation for negative experience"""
        form_data = {"years_of_experience": -5}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_cook_experience_update_form_too_high(self):
        """Test custom validation for too high experience"""
        form_data = {"years_of_experience": 105}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["years_of_experience"][0], "Experience cannot be more than 100 years.")