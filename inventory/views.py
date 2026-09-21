from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.decorators import admin_required
from .models import StockItem, StockMovement
from .forms import StockItemForm, StockMovementForm


@login_required
def stock_list(request):
    items = StockItem.objects.all()
    return render(request, 'inventory/stock_list.html', {'items': items})


@admin_required
def stock_add(request):
    if request.method == 'POST':
        form = StockItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            if item.quantity:
                StockMovement.objects.create(
                    stock_item=item, change=item.quantity, reason=StockMovement.Reason.RESTOCK,
                    note="Initial stock", created_by=request.user,
                )
            messages.success(request, "Stock item added.")
            return redirect('inventory:stock_list')
    else:
        form = StockItemForm()
    return render(request, 'inventory/stock_form.html', {'form': form, 'title': 'Add stock item'})


@admin_required
def stock_edit(request, pk):
    item = get_object_or_404(StockItem, pk=pk)
    if request.method == 'POST':
        form = StockItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock item updated.")
            return redirect('inventory:stock_list')
    else:
        form = StockItemForm(instance=item)
    return render(request, 'inventory/stock_form.html', {'form': form, 'title': f'Edit {item.name}'})


@admin_required
def stock_delete(request, pk):
    item = get_object_or_404(StockItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Stock item deleted.")
        return redirect('inventory:stock_list')
    return render(request, 'inventory/stock_confirm_delete.html', {'item': item})


@login_required
def stock_adjust(request, pk):
    """Record a restock / wastage / correction movement."""
    item = get_object_or_404(StockItem, pk=pk)
    if request.method == 'POST':
        form = StockMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.stock_item = item
            movement.created_by = request.user
            movement.save()
            item.quantity = item.quantity + movement.change
            item.save(update_fields=['quantity', 'updated_at'])
            messages.success(request, f"Stock for {item.name} updated.")
            return redirect('inventory:stock_list')
    else:
        form = StockMovementForm()
    return render(request, 'inventory/stock_adjust.html', {'form': form, 'item': item})
