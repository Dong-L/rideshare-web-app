from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView
from .models import Ride
from django.db.models import F
from django.db.models import Q

#imports for profile:
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.db import transaction
from .models import Profile
from .forms import UserForm,ProfileForm
from http.client import responses


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'ride_list'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.GET = None

    def get_queryset(self):
        query = self.request.GET.get('search')
        select = self.request.GET.get('search_choice')
        if query == None:
            return Ride.objects.all()
        else :
            if(select == "origin"):
                object_list = Ride.objects.filter(
                    Q(origin__icontains=query) | Q(origin_state__icontains=query)
                )
                return object_list
            if(select == "destination"):
                object_list = Ride.objects.filter(
                    Q(destination__icontains=query) | Q(destination_state__icontains=query)
                )
                return object_list
            if(select == "departure_date"):
                object_list = Ride.objects.filter(
                    Q(departure_date__icontains=query)
                )
                return object_list

    def join_ride(self, request):
        if request.GET.get('joinRide'):
            ride = get_object_or_404(Ride, created_by=request.user)
            ride.seats_available = F('seats_available') - 1
            ride.save(update_fields=["seats_available"])
            return render(request, 'index.html')

@login_required
@transaction.atomic
def Account_Info(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('myaccount')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'accountInfo.html', { #was profile.html
        'user_form': user_form,
        'profile_form': profile_form
    })

def seeProfile(request, user_id):
    user = User.objects.get(username=user_id)
    return render(request, 'profile.html', {'user' : user})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/')


class RideView(CreateView):
    model = Ride
    template_name = 'create_ride.html'
    fields = ('origin', 'origin_state', 'destination', 'destination_state', 'departure_date', 'asking_price', 'seats_available')
    def get_success_url(self):
            return ".."
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        self.request.user.created_rides.add(obj)

        return HttpResponseRedirect(self.get_success_url())


def join_ride(request, **kwargs):
    id_to_join = kwargs['ride_id']
    is_join = kwargs['join']
    if is_join == '1':
        try:
            new_seats = Ride.objects.get(id=id_to_join).seats_available - 1
            if new_seats >= 0:
                Ride.objects.filter(id=id_to_join).update(seats_available=new_seats)
            Ride.objects.get(id=id_to_join).passenger_list.add(request.user)
            request.user.profile.rides.add(Ride.objects.get(id=id_to_join))
            return render(request, 'join_ride.html')
        except:
            return render(request, 'ride_not_exist.html')
    else:
        try:
            ride_to_leave = kwargs['ride_id']
            new_seats = Ride.objects.get(id=ride_to_leave).seats_available + 1
            Ride.objects.filter(id=ride_to_leave).update(seats_available=new_seats)
            Ride.objects.get(id=id_to_join).passenger_list.remove(request.user)
            request.user.profile.rides.remove(Ride.objects.get(id=ride_to_leave))
            return render(request, 'leave_ride.html')
        except:
            return render(request, 'ride_not_exist.html')


def delete_ride(request, **kwargs):
    id_to_del = kwargs['ride_id']
    Ride.objects.filter(id=id_to_del).delete()
    
    return render(request, 'del_ride.html')

