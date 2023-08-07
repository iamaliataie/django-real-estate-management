from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView

from .mixins import AdminAccessMixin, AdminStaffAccessMixin, AdminAgentMixin
from .forms import SignUpForm
from .models import User

from property.models import Property, PropertyType
from property.forms import PropertyForm, ImageFormSet

# Create your views here.


class PropertyInline():
    form_class = PropertyForm
    model = Property
    template_name = "property/property_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()
        if not self.object.agent:
            self.object.agent = self.request.user
            self.object.save()  

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('property:property_list')

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving. Useful if you have multiple formsets
        """
        images = formset.save(commit=False)  # self.save_formset(formset, contact)
        # add this 2 lines, if you have can_delete=True parameter 
        # set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.property = self.object
            image.save()

                            
class PropertyCreate(AdminStaffAccessMixin, PropertyInline, CreateView):
    
    success_url = reverse_lazy('property:property_list')
    
    def get_context_data(self, **kwargs):
        ctx = super(PropertyCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'images': ImageFormSet(prefix='images'),
            }
        else:
            return {
                'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }
            
class PropertyUpdate(AdminAgentMixin, PropertyInline, UpdateView):
    
    def get_context_data(self, **kwargs):
        ctx = super(PropertyUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()

        return ctx

    def get_named_formsets(self):
        return {
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
        }


class BookmarkView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = 'properties'
    template_name = 'property/property_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(BookmarkView, self).get_context_data(**kwargs)
        global properties, property_types
        properties = self.request.user.favorites.all()
        property_types = PropertyType.objects.all()
        context['properties'] = properties
        context['property_types'] = property_types
        context['page_title'] = 'Bookmarks'
        return context

    def post(self, request, *args, **kwargs):
        global properties
        form = self.request.POST
        if form['type'] == 'search':
            properties = request.user.favorites.all().filter(title__icontains=form['title'])
        elif form['type'] == 'filter':
            properties = request.user.favorites.all().filter(type__title=form['filter'])
        else:
            properties = properties.order_by(form['sort'])
            
        context = {
            'properties': properties,
            'property_types': property_types
        }
        return render(request, 'property/property_list.html', context)


@login_required
@csrf_exempt
def remove_from_bookmarks(request, pk):
    property = Property.objects.get(pk=pk)
    request.user.favorites.remove(property)
    return redirect('accounts:bookmarks')


class Login(LoginView):
    redirect_authenticated_user = True
    success_url = reverse_lazy('property:home')
    

class Register(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('accounts:login')