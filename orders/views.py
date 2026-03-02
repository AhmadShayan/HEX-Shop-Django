from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from carts.models import CartItem
from .forms import OrderForm
from .models import Order, Payment, OrderProduct
import datetime


@login_required(login_url='login')
def payments(request):
    return render(request, 'orders/payments.html')


@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    if cart_items.count() == 0:
        return redirect('store')   # Fixed typo: 'sotre' -> 'store'

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)   # Fixed: += not =
        quantity += cart_item.quantity
    tax = (2 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number from date + pk
            current_date = datetime.date.today().strftime('%Y%m%d')
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }
            return render(request, 'orders/payments.html', context)
    return redirect('checkout')


@login_required(login_url='login')
def confirm_order(request):
    """
    Cash-on-Delivery: marks the order complete, saves OrderProduct records, clears cart.
    """
    if request.method == 'POST':
        order_number = request.POST.get('order_number')
        current_user = request.user

        try:
            order = Order.objects.get(order_number=order_number, user=current_user, is_ordered=False)
        except Order.DoesNotExist:
            messages.error(request, 'Order not found.')
            return redirect('store')

        # Create a COD payment record
        payment = Payment.objects.create(
            user=current_user,
            payment_id='COD-' + order_number,
            payment_method='Cash on Delivery',
            amount_paid=str(order.order_total),
            status='Pending',
        )

        # Link payment, mark order as placed
        order.payment = payment
        order.is_ordered = True
        order.status = 'Accepted'
        order.save()

        # Save each cart item as an OrderProduct and reduce stock
        cart_items = CartItem.objects.filter(user=current_user)
        for item in cart_items:
            order_product = OrderProduct()
            order_product.order = order
            order_product.payment = payment
            order_product.user = current_user
            order_product.product = item.product
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

            item_variations = item.variations.all()
            order_product.variation.set(item_variations)
            order_product.save()

            # Reduce stock
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear the cart
        CartItem.objects.filter(user=current_user).delete()

        messages.success(
            request,
            f'Your order #{order_number} has been placed! Our team will contact you to confirm delivery.'
        )
        return render(request, 'orders/order_complete.html', {'order': order})

    return redirect('store')
