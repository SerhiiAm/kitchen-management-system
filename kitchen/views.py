from django.shortcuts import render

from kitchen.models import DishType, Cook, Dish


def index(request):
    """View function for the home page of the site."""

    num_dishtypes = DishType.objects.count()
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get('num_visits', 0) + 1
    request.session['num_visits'] = num_visits
    context = {
        'num_dishtypes': num_dishtypes,
        'num_cooks': num_cooks,
        'num_dishes': num_dishes,
        'num_visits': num_visits,
    }

    return render(request, "kitchen/index.html", context)
