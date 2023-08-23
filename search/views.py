from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import SearchCriteria

# Create your views here.

@login_required
def clear_user_search(request):
    SearchCriteria.objects.filter(user=request.user).delete()
    return redirect(request.META.get('HTTP_REFERER'))