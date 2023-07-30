from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView
from .models import Property
from .forms import PropertyForm, ImageFormSet

# Create your views here.

class Home(ListView):
    model = Property
    template_name = 'home.html'


class PropertyInline():
    form_class = PropertyForm
    model = Property
    template_name = "property/property_create_or_update.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('/')

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
            
            
class PropertyCreate(PropertyInline, CreateView):

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


class PropertyUpdate(PropertyInline, UpdateView):
    def get_context_data(self, **kwargs):
        ctx = super(PropertyUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
        }