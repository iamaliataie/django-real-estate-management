from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Property, PropertyType

from inquiry.forms import InquiryForm

# Create your views here.

class Home(ListView):
    queryset = Property.objects.filter(active=True, deal=False)
    model = Property
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        locations = list(Property.objects.filter(active=True, deal=False).values())
        context['locations'] = locations
        return context


class PropertyListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PropertyListView, self).get_context_data(**kwargs)
        global properties
        properties =  Property.objects.filter(active=True, deal=False)
        context['properties'] = properties
        context['page_title'] = 'Properties'
        return context

    def post(self, request, *args, **kwargs):
        global properties
        form = self.request.POST
        
        if 'search' in form:
            properties = Property.objects.filter(active=True, deal=False)
            
            if form['property_type']:
                properties = properties.filter(type__title=form['property_type'])
            if form['city']:
                properties = properties.filter(city__icontains=form['city'])
            if form['range_from'] and form['range_to']:
                properties = properties.filter(price__range=(int(form['range_from']), int(form['range_to'])))
            if form['bedrooms']:
                properties = properties.filter(features__icontains=f"{form['bedrooms']} bedrooms")
                
            context ={
                'properties': properties,
                'page_title': 'Search'
            }
            return render(request, 'property/property_list.html', context)
        elif form['type'] == 'filter':
            properties = Property.objects.filter(active=True, deal=False).filter(type__title=form['filter'])
        else:
            properties = properties.order_by(form['sort'])
            
        context = {
            'properties': properties,
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


class TypePropertyListView(ListView):
    model = Property
    template_name = 'property/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        global properties
        properties = super(TypePropertyListView, self).get_queryset()
        slug = self.kwargs.get('slug')
        properties = Property.objects.filter(type__slug=slug, active=True, deal=False)
        return properties

    
    def get_context_data(self, **kwargs):
        context = super(TypePropertyListView, self).get_context_data(**kwargs)
        global slug
        slug = self.kwargs.get('slug')
        context['page_title'] = slug.capitalize()
        return context

    def post(self, request, *args, **kwargs):
        global properties
        form = self.request.POST
        
        if form['type'] == 'filter':
            properties = Property.objects.filter(active=True, deal=False).filter(type__title=form['filter'])
        else:
            properties = properties.order_by(form['sort'])
            
        context = {
            'properties': properties,
            'page_title': slug.capitalize(),
        }
        return render(request, 'property/property_list.html', context)
    

@login_required
@csrf_exempt
def add_to_favorites(request):
    
    form = request.POST
    if not form.get('property_id'):
        print('something is not a valid form')
    else:
        property = Property.objects.filter(id=form.get('property_id')).first()
        if not property:
            print('property not found')
        else:
            request.user.favorites.add(property)
            request.user.save()
    
    return redirect('property:property_detail', pk=form.get('property_id'))


