from django.shortcuts import render, redirect
from django.views import View


from users.models import User
from users.utils import paginate_users
# Create your views here.


class Index(View):
    def get(self, request):
        users = User.objects.all().filter(is_superuser=False).defer('password')

        custom_range, users = paginate_users(request, users, 1)
        context = {
            'users': users,
            'custom_range': custom_range
        }
        return render(request, 'core/index.html', context)

    
def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
