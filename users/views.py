from django.shortcuts import render,redirect
from .forms import UserForm,ProfileForm
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
# @transaction.atomic
# def register(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = ProfileForm(request.POST)
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user.password)
#             user.save()
#             profile = profile_form.save(commit=False)
#             profile.user = request.user
#             profile.save()
#             return redirect('users:login')
#     else:
#         user_form = UserForm()
#         profile_form = ProfileForm()
#     return render(request, 'register.html', {
#             'user_form': user_form,
#             'profile_form': profile_form
#             })

@transaction.atomic
def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.set_password(user.password)
            user.profile.age = profile_form.cleaned_data.get('age')
            user.profile.address = profile_form.cleaned_data.get('address')
            user.save()
            return redirect('users:login')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {
            'user_form': user_form,
            'profile_form': profile_form
            })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            user_form.save()
            profile.save()
            return redirect('login')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'users/update_user.html', {
        'user_form': user_form,
        'profile_form': profile_form
        })