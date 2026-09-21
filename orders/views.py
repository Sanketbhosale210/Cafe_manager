from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from menu.models import MenuItem, Category
from inventory.models import StockMovement
from .models import Order, OrderItem

CART_SESSION_KEY = 'pos_cart'


def _get_cart(session):
    return session.setdefault(CART_SESSION_KEY, {})


@login_required
def pos(request):
    cart = _get_cart(request.session)
    categories = Category.objects.prefetch_related('items').all()
    uncategorised = MenuItem.objects.filter(category__isnull=True, is_available=True)

    cart_lines = []
    total = Decimal('0.00')
    if cart:
        items_by_id = MenuItem.objects.in_bulk([int(i) for i in cart.keys()])
        for item_id, qty in cart.items():
            item = items_by_id.get(int(item_id))
            if not item:
                continue
            line_total = item.price * qty
            total += line_total
            cart_lines.append({'item': item, 'qty': qty, 'line_total': line_total})

    return render(request, 'orders/pos.html', {
        'categories': categories,
        'uncategorised': uncategorised,
        'cart_lines': cart_lines,
        'total': total,
    })


@login_required
def pos_add(request, item_id):
    if request.method == 'POST':
        cart = _get_cart(request.session)
        key = str(item_id)
        cart[key] = cart.get(key, 0) + 1
        request.session.modified = True
    return redirect('orders:pos')


@login_required
def pos_remove(request, item_id):
    if request.method == 'POST':
        cart = _get_cart(request.session)
        key = str(item_id)
        if key in cart:
            cart[key] -= 1
            if cart[key] <= 0:
                del cart[key]
            request.session.modified = True
    return redirect('orders:pos')


@login_required
def pos_clear(request):
    if request.method == 'POST':
        request.session[CART_SESSION_KEY] = {}
        request.session.modified = True
    return redirect('orders:pos')


@login_required
def pos_checkout(request):
    if request.method != 'POST':
        return redirect('orders:pos')

    cart = _get_cart(request.session)
    if not cart:
        messages.error(request, "Cart is empty.")
        return redirect('orders:pos')

    items_by_id = MenuItem.objects.in_bulk([int(i) for i in cart.keys()])

    order = Order.objects.create(
        table_number=request.POST.get('table_number', ''),
        customer_name=request.POST.get('customer_name', ''),
        payment_method=request.POST.get('payment_method', Order.PaymentMethod.CASH),
        status=Order.Status.PAID,
        created_by=request.user,
        paid_at=timezone.now(),
    )

    for item_id, qty in cart.items():
        menu_item = items_by_id.get(int(item_id))
        if not menu_item:
            continue
        OrderItem.objects.create(order=order, menu_item=menu_item, quantity=qty, unit_price=menu_item.price)

        # Auto-deduct linked inventory stock.
        if menu_item.stock_item_id:
            stock_item = menu_item.stock_item
            stock_item.quantity = stock_item.quantity - Decimal(qty)
            stock_item.save(update_fields=['quantity', 'updated_at'])
            StockMovement.objects.create(
                stock_item=stock_item, change=-Decimal(qty), reason=StockMovement.Reason.SALE,
                note=f"Order #{order.pk}", created_by=request.user,
            )

    request.session[CART_SESSION_KEY] = {}
    request.session.modified = True
    messages.success(request, f"Order #{order.pk} completed.")
    return redirect('orders:receipt', pk=order.pk)


@login_required
def receipt(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/receipt.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.select_related('created_by').all()
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    return render(request, 'orders/order_history.html', {'orders': orders[:200], 'status': status})
