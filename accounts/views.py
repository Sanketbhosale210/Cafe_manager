from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .decorators import admin_required
from .forms import StaffCreateForm, StaffEditForm
from .models import User


class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    auth_logout(request)
    return redirect('accounts:login')


@admin_required
def staff_list(request):
    staff = User.objects.all().order_by('username')
    return render(request, 'accounts/staff_list.html', {'staff': staff})


@admin_required
def staff_add(request):
    if request.method == 'POST':
        form = StaffCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff account created.")
            return redirect('accounts:staff_list')
    else:
        form = StaffCreateForm()
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Add staff member'})


@admin_required
def staff_edit(request, pk):
    staff_member = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = StaffEditForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            messages.success(request, "Staff account updated.")
            return redirect('accounts:staff_list')
    else:
        form = StaffEditForm(instance=staff_member)
    return render(request, 'accounts/staff_form.html', {'form': form, 'title': f'Edit {staff_member.username}'})


@admin_required
def staff_delete(request, pk):
    staff_member = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if staff_member == request.user:
            messages.error(request, "You can't delete your own account.")
        else:
            staff_member.delete()
            messages.success(request, "Staff account deleted.")
        return redirect('accounts:staff_list')
    return render(request, 'accounts/staff_confirm_delete.html', {'staff_member': staff_member})
