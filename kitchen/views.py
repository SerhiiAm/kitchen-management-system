from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from kitchen.forms import (
    DishForm,
    CookCreationForm,
    CookExperienceUpdateForm,
    DishSearchForm,
    DishTypeSearchForm,
    CookSearchForm
)

from kitchen.models import DishType, Cook, Dish


def is_admin(user):
    return user.is_superuser or user.is_staff


class IndexView(generic.TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["num_dish_types"] = DishType.objects.count()
        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()

        num_visits = self.request.session.get("num_visits", 0) + 1
        self.request.session["num_visits"] = num_visits
        context["num_visits"] = num_visits

        return context


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_types_list"
    template_name = "kitchen/dish_type_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypeListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishTypeSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = DishType
    template_name = "kitchen/dish_type_detail.html"
    context_object_name = "dish_type"

    queryset = DishType.objects.prefetch_related("dishes")


class DishTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class DishTypeUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish-type-list")
    template_name = "kitchen/dish_type_form.html"
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class DishTypeDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-type-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name},
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = Dish.objects.select_related("dish_type").prefetch_related("cooks")


class DishCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    success_url = reverse_lazy("kitchen:dish-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class ToggleAssignToDishView(LoginRequiredMixin, UserPassesTestMixin, generic.View):
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)

    def get(self, request, pk, *args, **kwargs):
        cook = self.request.user
        dish = Dish.objects.get(id=pk)

        if cook in dish.cooks.all():
            dish.cooks.remove(cook)
        else:
            dish.cooks.add(cook)

        return HttpResponseRedirect(reverse_lazy("kitchen:dish-detail", args=[pk]))


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username},
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(username__icontains=form.cleaned_data["username"])
        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.prefetch_related("dishes__dish_type")


class CookCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    success_url = reverse_lazy("kitchen:cook-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)


class CookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy("kitchen:cook-detail", kwargs={"pk": self.object.pk})

    def test_func(self):
        return is_admin(self.request.user)


class CookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Cook
    success_url = reverse_lazy("kitchen:cook-list")
    raise_exception = True

    def test_func(self):
        return is_admin(self.request.user)
