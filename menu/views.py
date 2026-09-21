from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required
from .models import MenuItem, Category
from .forms import MenuItemForm, CategoryForm


@login_required
def menu_list(request):
    items = MenuItem.objects.select_related('category').all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        items = items.filter(category_id=category_id)
    return render(request, 'menu/menu_list.html', {
        'items': items,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
    })


@admin_required
def menu_add(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item added.")
            return redirect('menu:menu_list')
    else:
        form = MenuItemForm()
    return render(request, 'menu/menu_form.html', {'form': form, 'title': 'Add menu item'})


@admin_required
def menu_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Menu item updated.")
            return redirect('menu:menu_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'menu/menu_form.html', {'form': form, 'title': f'Edit {item.name}'})


@admin_required
def menu_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Menu item deleted.")
        return redirect('menu:menu_list')
    return render(request, 'menu/menu_confirm_delete.html', {'item': item})


@admin_required
def category_list(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added.")
            return redirect('menu:category_list')
    else:
        form = CategoryForm()
    return render(request, 'menu/category_list.html', {'categories': categories, 'form': form})


@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted.")
    return redirect('menu:category_list')
