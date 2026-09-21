import json
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, DecimalField
from django.db.models.functions import TruncDate
from django.shortcuts import render
from django.utils import timezone

from orders.models import Order, OrderItem
from inventory.models import StockItem


@login_required
def home(request):
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    week_ago = today - timedelta(days=6)

    paid_orders = Order.objects.filter(status=Order.Status.PAID)

    line_total_expr = F('quantity') * F('unit_price')

    today_total = OrderItem.objects.filter(
        order__in=paid_orders, order__created_at__date=today
    ).aggregate(total=Sum(line_total_expr, output_field=DecimalField()))['total'] or Decimal('0')

    month_total = OrderItem.objects.filter(
        order__in=paid_orders, order__created_at__date__gte=start_of_month
    ).aggregate(total=Sum(line_total_expr, output_field=DecimalField()))['total'] or Decimal('0')

    today_order_count = paid_orders.filter(created_at__date=today).count()

    # Last 7 days daily totals for the chart.
    daily_qs = (
        OrderItem.objects.filter(order__in=paid_orders, order__created_at__date__gte=week_ago)
        .annotate(day=TruncDate('order__created_at'))
        .values('day')
        .annotate(total=Sum(line_total_expr, output_field=DecimalField()))
        .order_by('day')
    )
    daily_map = {row['day']: float(row['total']) for row in daily_qs}
    chart_labels = []
    chart_values = []
    for i in range(7):
        day = week_ago + timedelta(days=i)
        chart_labels.append(day.strftime('%a %d'))
        chart_values.append(daily_map.get(day, 0))

    # Top selling items this month.
    top_items = (
        OrderItem.objects.filter(order__in=paid_orders, order__created_at__date__gte=start_of_month)
        .values('menu_item__name')
        .annotate(qty_sold=Sum('quantity'), revenue=Sum(line_total_expr, output_field=DecimalField()))
        .order_by('-qty_sold')[:8]
    )

    low_stock = StockItem.objects.filter(quantity__lte=F('reorder_level'))

    return render(request, 'dashboard/home.html', {
        'today_total': today_total,
        'month_total': month_total,
        'today_order_count': today_order_count,
        'chart_labels': json.dumps(chart_labels),
        'chart_values': json.dumps(chart_values),
        'top_items': top_items,
        'low_stock': low_stock,
    })
