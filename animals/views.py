from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.dates import (
    ArchiveIndexView, TodayArchiveView
)
from django.views.generic import (
    TemplateView, ListView, DetailView, 
    CreateView, UpdateView, DeleteView, FormView,
)

from animals.models import Animal
from zoo_site.forms import AnimalSearchForm

class SignUpView(CreateView):
    """
    Uses Django's built-in UserCreationForm (username + password × 2).
    On successful registration the user is logged in immediately and
    redirected to the home page — no separate login step required.

    Extra context added:
      - page_title: for the heading
    """
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('animals:home')

    def form_valid(self, form):
        # Save the form and get the user instance
        user = form.save()
        # Log the user in using the 'user' variable, not 'self.obj'
        login(self.request, user)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Account'
        return context

class HomeView(TemplateView):
    template_name = 'animals/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to the Zoo'
        context['total_animals'] = Animal.objects.count()
        context['captive_count'] = Animal.objects.filter(born_in_captivity=True).count()
        context['wild_count'] = Animal.objects.filter(born_in_captivity=False).count()
        return context

class AnimalListView(LoginRequiredMixin, ListView):
    model = Animal
    template_name = 'animals/animal_list.html'
    context_object_name = 'animals' # rename object_list
    paginate_by = 5
    
    def get_queryset(self):
        return Animal.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = Animal.objects.count()
        return context
    
class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'animals/animal_detail.html'
    context_object_name = 'animal'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        animal = self.get_object()
        context['page_title'] = f"Animal: {animal.name}"
        context['is_elderly'] = self.object.age > 15
        context['weight_category'] = self._weight_category(animal.weight)
        return context
    
    @staticmethod
    def _weight_category(weight):
        """Returns a human-readable weight category label."""
        if weight < 10:
            return 'Small'
        elif weight < 100:
            return 'Medium'
        elif weight < 500:
            return 'Large'
        return 'Very Large'
    
class AnimalCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    fields = ['name', 'age', 'weight', 'born_in_captivity']
    success_url = reverse_lazy('animals:animal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Add New Animal'
        context['form_action'] = 'Create'
        return context
    
class AnimalUpdateView(LoginRequiredMixin, UpdateView):
    model = Animal
    fields = ['name', 'age', 'weight', 'born_in_captivity']
    template_name = 'animals/animal_form.html'
    success_url = reverse_lazy('animals:animal-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Edit: {self.object.name}'
        context['form_action'] = 'Update'
        return context
    
class AnimalDeleteView(LoginRequiredMixin, DeleteView):
    model = Animal
    template_name = 'animals/animal_confirm_delete.html'
    success_url = reverse_lazy('animals:animal-list')

class AnimalSearchView(LoginRequiredMixin, ListView):
    model = Animal
    template_name = 'animals/animal_search.html'
    context_object_name = 'animals'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Animal.objects.filter(name__icontains=query)
        return Animal.objects.none()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == "GET" and self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Search Animals'
        context['results'] = None
        context['search_performed'] = False

        form = AnimalSearchForm(self.request.GET or None)
        context['form'] = form
        
        if self.request.GET and form.is_valid():
            data = form.cleaned_data
            queryset = Animal.objects.all()

            if data.get('name'):
                queryset = queryset.filter(name__icontains=data['name'])

            if data.get('min_age') is not None:
                queryset = queryset.filter(age__gte=data['min_age'])
            if data.get('max_age') is not None:
                queryset = queryset.filter(age__lte=data['max_age'])

            if data.get('min_weight') is not None:
                queryset = queryset.filter(weight__gte=data['min_weight'])
            if data.get('max_weight') is not None:
                queryset = queryset.filter(weight__lte=data['max_weight'])

            if data.get('born_in_captivity') is not None:
                queryset = queryset.filter(born_in_captivity=data['born_in_captivity'])

            context['results'] = queryset
            context['result_count'] = queryset.count()
            context['search_performed'] = True

        return context
    
class AnimalArchiveIndexView(LoginRequiredMixin, ArchiveIndexView):
    model = Animal
    date_field = "date_added"  # Use whatever date field you have in your Animal model
    context_object_name = "animal_list"

class AnimalTodayArchiveView(TodayArchiveView):
    queryset = Animal.objects.all()
    date_field = "date_added"  # Ensure this matches your model field
    allow_empty = True