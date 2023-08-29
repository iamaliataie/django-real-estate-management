from datetime import date
from django.conf import settings
from django.contrib import messages
from django.forms.models import BaseModelForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives


from .mixins import AdminStaffAccessMixin, AdminAgentMixin, AgentMixin
from .forms import SignUpForm, CustomUserChangeForm
from .models import User

from property.models import Property, PropertyType, Image
from property.forms import PropertyForm, ImageFormSet

from inquiry.models import Inquiry

from deal.models import Deal
from deal.forms import DealForm

from search.models import SearchCriteria
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
        
        if self.object.type.title == 'Residential':
            self.object.marker_color = 'green'
            self.object.type_color = 'success'
            self.object.type_title = 'Residential'
        elif self.object.type.title == 'Commercial':
            self.object.marker_color = 'red'
            self.object.type_color = 'danger'
            self.object.type_title = 'Commercial'
        elif self.object.type.title == 'Rental':
            self.object.marker_color = 'yellow'
            self.object.type_color = 'warning'
            self.object.type_title = 'Rental'
        
        self.object.save()
        
        if not self.object.agent:
            self.object.agent = self.request.user
            self.object.save()
            
            data = {
                'user': self.request.user,
                'property': self.object
            }
            current_site = get_current_site(self.request)
            mail_subject = 'New property added.'
            html_message = render_to_string('property/new_property_email.html', {
                'user': data['user'],
                'property': data['property'],
                'domain': current_site.domain,
            })
            to_email = settings.EMAIL_HOST_USER
            from_email = self.request.user.email
            recipient_list = [to_email]
            text_message = f"New property add by {data['user'].get_full_name()}, review property by going to this link http://127.0.0.1:8000/properties/{self.object.id}"

            # Create the EmailMultiAlternatives object
            email = EmailMultiAlternatives(
                mail_subject, text_message, from_email, recipient_list
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            
            
            ## email new property to customers matched search criteria
            property_type = self.object.type
            search = SearchCriteria.objects.filter(type=property_type)
            recipient_list = []
            for sc in search:
                recipient_list.append(sc.user.email)
                
            current_site = get_current_site(self.request)
            mail_subject = 'New property added.'
            html_message = render_to_string('property/customer_new_property_email.html', {
                'property': self.object,
                'domain': current_site.domain,
            })
            text_message = f"New {self.object.type.title} property added. View property by going to this link http://127.0.0.1:8000/properties/{self.object.id}"
            # Create the EmailMultiAlternatives object
            email = EmailMultiAlternatives(
                mail_subject, text_message, from_email, recipient_list
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('property:property_detail', self.object.id)

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
    
    def get_context_data(self, **kwargs):
        ctx = super(PropertyCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['page_title'] = 'Create Property'
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'images': ImageFormSet(prefix='images'),}
        else:
            return {'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),}
    
            
class PropertyUpdate(AdminAgentMixin, PropertyInline, UpdateView):
    
    def get_context_data(self, **kwargs):
        ctx = super(PropertyUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        ctx['page_title'] = 'Update Property'
        return ctx

    def get_named_formsets(self):
        return {'images': ImageFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),}


@login_required
def remove_property_image(request, pk):
    image = get_object_or_404(Image, pk=pk)
    property = image.property
    image.delete()
    return redirect('accounts:property_update', pk=property.id)


class PropertyDeleteView(AgentMixin, DeleteView):
    model = Property
    template_name = 'property/delete.html'
    success_url = reverse_lazy('accounts:agent_property_list')


class AgentPropertyListView(AdminStaffAccessMixin, ListView):
    model = Property
    template_name = 'property/property_list.html'
    context_object_name = 'properties'
    
    def get_queryset(self):
        queryset = super(AgentPropertyListView, self).get_queryset()
        queryset = Property.objects.filter(agent=self.request.user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(AgentPropertyListView, self).get_context_data(**kwargs)
        context['page_title'] = 'My Properties'
        return context
    

class DealCreateView(AdminStaffAccessMixin, CreateView):
    model = Deal
    form_class = DealForm
    success_url = reverse_lazy('accounts:deal_list')
    
    def get_initial(self):
        property = Property.objects.get(id=self.kwargs['pk'])
        return { 'agent': self.request.user, 'property': property }

    def form_valid(self, form):
        print(form.cleaned_data)
        deal = form.save()
        property = deal.property
        property.deal = True
        property.deal_date = date.today()
        property.save()
        return super().form_valid(form)


class DealPropertyChooseView(AdminStaffAccessMixin, ListView):
    model = Property
    template_name = 'deal/deal_property_list.html'
    
    def get_queryset(self):
        queryset = super(DealPropertyChooseView, self).get_queryset()
        queryset = Property.objects.filter(agent=self.request.user, active=True, deal=False)
        return queryset


class DealListView(AdminStaffAccessMixin, ListView):
    model = Deal
    def get_queryset(self):
        queryset = super(DealListView, self).get_queryset()
        queryset = Deal.objects.filter(agent=self.request.user)
        return queryset


class DealDetailView(AgentMixin, DetailView):
    model = Deal


class DealUpdateView(AgentMixin, UpdateView):
    model = Deal
    form_class = DealForm
    
    def get_success_url(self):
        return reverse_lazy('accounts:deal_detail', kwargs={'pk': self.object.pk})
    

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
    success_url = reverse_lazy('accounts:register')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        data = {
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your account.'
        html_message = render_to_string('registration/verify_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':data.get('uid'),
            'token':data.get('token'),
        })
        to_email = form.cleaned_data.get('email')
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [to_email]
        text_message = f"Please verify your email address by going to this link http://127.0.0.1:8000/accounts/activate/{data['uid']}/{data['token']}"
        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            mail_subject, text_message, from_email, recipient_list
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        messages.success(self.request, 'Please confirm your email address to complete the registration')
        return super().form_valid(form)
    
    
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/email_confirmed.html',)
    else:
        return HttpResponse('Activation link is invalid!')
    
    
class ProfileView(LoginRequiredMixin, PasswordChangeView):

    template_name = 'account/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['user_form'] = CustomUserChangeForm(instance=self.request.user)
        return context
    
    def form_valid(self, form: BaseModelForm):
        messages.success(self.request, 'Your password has been updated successfully.')
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        if 'profile' in request.POST:
            form = CustomUserChangeForm(request.POST, instance=request.user)
            for field in form.fields:
                if form[field].value() == '':
                    messages.warning(request, 'fields cannot be empty')
                    return redirect('accounts:profile')
            if form.is_valid():
                form.save()
                messages.success(request, 'Your profile has been updated successfully.')
            else:
                messages.warning(self.request, f"{''.join(form.errors.as_data()['email'][0])} - {form['email'].value()}" )
            return redirect('accounts:profile')
        return super().post(request, *args, **kwargs)

