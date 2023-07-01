from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from users.models import User

from .models import Link
from .forms import LinkModelForm

# Create your views here.
class ListShowLinks(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.htmx == False:
            return Http404
        try:
            user = User.objects.get(id= pk)
            
        except:
            messages.error(request, "Cannot load links.")
        context = {
            'user': user,
            
            'tab': 3
        }
        return render(request, 'users/partials/tab.html', context)

class ListGetLinks(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.htmx == False:
            return Http404
        try:
            user = User.objects.get(id= pk)
            links = list(Link.objects.filter(user=user).values('type','link','id'))
            
        except:
            messages.error(request, "Cannot load links.")
            links = []
        for link in links:
            temp_link = Link(type=link['type'])
            link['label'] = temp_link.get_type_display()
        context = {
            'user': user,
            'links': links,
            
        }
        return render(request, 'list/partials/manage_links.html', context)
class ListEditLinks(LoginRequiredMixin, View):
    def get(self, request,pk):
        if request.htmx == False:
            return Http404
        try:
           
            link = Link.objects.get(id=pk, user=request.user)
            
            form = LinkModelForm(instance=link)

        except:
            messages.error(request, "Cannot load links.")
            link = []
        context = {
            'link_form': form,
            'link': link
           
        }
        
        return render(request, 'list/partials/link_form.html', context)
class ListDeleteLink(LoginRequiredMixin, View):
    def delete(self, request, pk):
        if request.htmx == False:
            return Http404
        
        try:
            link = Link.objects.get(id=pk)
            link.delete()
        except:
            print("error deleting link")

        try:
            #user = User.objects.get(id= pk)
            links = list(Link.objects.filter(user=request.user).values('type','link','id'))
            
        except:
            messages.error(request, "Cannot load links.")
            links = []
        for link in links:
            temp_link = Link(type=link['type'])
            link['label'] = temp_link.get_type_display()
        context = {
           
            'links': links,
            
        }
        return render(request, 'list/partials/manage_links.html', context)

class ListCreateLink(LoginRequiredMixin, View):
    def get(self, request):
        form = LinkModelForm()
        context = {
            'link_form': form,
            'link': None
        }
        return render(request, 'list/partials/link_form.html', context)

class ListSaveLinks(LoginRequiredMixin, View):
    def post(self, request):
        if request.htmx == False:
            return Http404
        try:
            print(request.POST)
            pk = request.POST['linkId']
            link_type = request.POST['type']
            link_link = request.POST['link']
            try:
                #link = Link.objects.get(user=request.user,type=link_type,link=link_link)
                link = Link.objects.get(user=request.user,id=pk)
                link_form = LinkModelForm(request.POST, instance=link)

            except:
                link_form = LinkModelForm(request.POST)

            if link_form.is_valid():
                link = link_form.save(commit=False)
                link.user = request.user
                link.save()
            
        except:
            messages.error(request, "Cannot load links.")
        try:
           
            links = list(Link.objects.filter(user=request.user).values('type','link','id'))
            
        except:
            messages.error(request, "Cannot load links.")
            links = []
        for link in links:
            temp_link = Link(type=link['type'])
            link['label'] = temp_link.get_type_display()
        context = {
            'links': links,
            
        }
        return render(request, 'list/partials/manage_links.html', context)
       