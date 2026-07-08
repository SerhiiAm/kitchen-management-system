from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from kitchen.models import DishType, Cook, Dish


def index(request):
    """View function for the home page of the site."""

    num_dish_types = DishType.objects.count()
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    context = {
        'num_dish_types': num_dish_types,
        'num_cooks': num_cooks,
        'num_dishes': num_dishes,
        'num_visits': num_visits,
    }

    return render(request, "kitchen/index.html", context)


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_types_list"
    template_name = "kitchen/dish_type_list.html"


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5
