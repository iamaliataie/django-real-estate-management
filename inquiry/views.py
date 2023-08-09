from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView

from .models import Inquiry
from .forms import InquiryReplyForm

from account.mixins import AdminStaffAccessMixin, InquiryPropertyAgentMixin

from property.models import Property
# Create your views here.

class InquiryListView(AdminStaffAccessMixin, ListView):
    model = Inquiry
    template_name = 'inquiry/inquiry_list.html'
    
    def get_queryset(self):
        queryset = super(InquiryListView, self).get_queryset()
        queryset = Inquiry.objects.filter(property__agent=self.request.user)
        return queryset


class InquiryDetailView(InquiryPropertyAgentMixin, FormMixin, DetailView):
    model = Inquiry
    form_class = InquiryReplyForm
    # template_name = 'inquiry/inquiry_detail.html'
    
    def dispatch(self, request, *args, **kwargs):
        inquiry = self.get_object()
        inquiry.status = 'read'
        inquiry.save()
        return super(InquiryDetailView, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            reply = form.save(commit=False)
            reply.inquiry = self.get_object()
            reply.save()
            messages.success(request, 'Reply has been sent successfully')
        else: messages.warning(request, 'Reply has not been sent successfully')
        return redirect('inquiry:inquiry_detail', pk=self.get_object().id)
