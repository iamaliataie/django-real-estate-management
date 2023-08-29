from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .models import Inquiry
from .forms import InquiryReplyForm

from account.mixins import AdminStaffAccessMixin, InquiryPropertyAgentMixin

# from property.models import Property
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
            
            mail_subject = 'Inquiry reply.'
            html_message = render_to_string('inquiry/inquiry_reply.html', {
                'inquiry_user': reply.inquiry.name,
                'inquiry_title': reply.inquiry.title,
                'inquiry_property': reply.inquiry.property,
                'inquiry_content': reply.inquiry.content,
                'reply_user': request.user,
                'reply_title': reply.subject,
                'reply_content': reply.content,
            })
            to_email = reply.inquiry.email
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [to_email]
            text_message = f"""
                title: {reply.subject}
                property: {reply.inquiry.property.title}
                message: {reply.content}
                
                best regards:
                {request.user.get_full_name()}
                phone: {request.user.phone}
            """
            # Create the EmailMultiAlternatives object
            email = EmailMultiAlternatives(
                mail_subject, text_message, from_email, recipient_list
            )
            email.attach_alternative(html_message, "text/html")
            email.send()
            messages.success(request, 'Reply has been sent successfully')
        else: messages.warning(request, 'Reply has not been sent successfully')
        return redirect('inquiry:inquiry_detail', pk=self.get_object().id)
