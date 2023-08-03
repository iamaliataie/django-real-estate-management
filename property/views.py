from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.views.generic.edit import FormMixin
from .models import Property, PropertyType
from .forms import PropertyForm, ImageFormSet

from inquiry.forms import InquiryForm

# Create your views here.

class Home(ListView):
    model = Property
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        locations = list(Property.objects.values())
        context['locations'] = locations
        return context


class PropertyListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs)
        global properties, property_types
        properties = Property.objects.all()
        property_types = PropertyType.objects.all()
        context['properties'] = properties
        context['property_types'] = property_types
        return context

    def post(self, request, *args, **kwargs):
        global properties
        form = self.request.POST
        if form['type'] == 'search':
            properties = Property.objects.filter(title__icontains=form['title'])
        elif form['type'] == 'filter':
            properties = Property.objects.filter(type__title=form['filter'])
        else:
            properties = properties.order_by(form['sort'])
            
        context = {
            'properties': properties,
            'property_types': property_types
        }
        return render(request, 'property/property_list.html', context)
    

class PropertyDetailView(FormMixin, DetailView):
    model = Property
    template_name = 'property/property_detail.html'
    context_object_name = 'property'
    form_class = InquiryForm
    
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.property = self.get_object()
            inquiry.save()
            messages.success(request, 'Your inquiry has been sent successfully')
        else: messages.warning(request, 'Your inquiry has not been sent successfully')
        return redirect('property:property_detail', pk=self.get_object().id)

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
        
        print(ctx['named_formsets'])
        return ctx

    def get_named_formsets(self):
        return {
            'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
        }