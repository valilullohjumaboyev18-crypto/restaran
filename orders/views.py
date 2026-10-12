import io
import json
import qrcode
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category, MenuItem, Order, OrderItem

@ensure_csrf_cookie
def menu(request):
    categories = Category.objects.filter(is_active=True).prefetch_related("items")
    items = MenuItem.objects.filter(is_available=True, category__is_active=True).select_related("category")
    return render(request, "orders/menu.html", {"categories": categories, "items": items})

@require_POST
def create_order(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
        table_number = int(payload.get("table_number", 0))
        raw_items = payload.get("items", [])
        if not 1 <= table_number <= 20:
            return JsonResponse({"ok": False, "error": "1 dan 20 gacha bo‘lgan stol raqamini tanlang."}, status=400)
        if not isinstance(raw_items, list) or not raw_items:
            return JsonResponse({"ok": False, "error": "Savat bo‘sh. Avval taom tanlang."}, status=400)

        quantities = {}
        for entry in raw_items:
            item_id = int(entry.get("id", 0))
            quantity = int(entry.get("quantity", 0))
            if quantity < 1 or quantity > 50:
                raise ValueError
            quantities[item_id] = quantities.get(item_id, 0) + quantity
        menu_items = {item.id: item for item in MenuItem.objects.filter(
            id__in=quantities.keys(), is_available=True, category__is_active=True
        )}
        if len(menu_items) != len(quantities):
            return JsonResponse({"ok": False, "error": "Ayrim taomlar hozir mavjud emas. Menyuni yangilang."}, status=400)

        customer_name = str(payload.get("customer_name", "")).strip()[:100]
        customer_phone = str(payload.get("customer_phone", "")).strip()[:30]
        note = str(payload.get("note", "")).strip()[:1000]
        total = sum(menu_items[item_id].price * quantity for item_id, quantity in quantities.items())

        order = Order.objects.create(
            table_number=table_number, customer_name=customer_name,
            customer_phone=customer_phone, note=note, total=total
        )
        OrderItem.objects.bulk_create([
            OrderItem(order=order, menu_item=menu_items[item_id],
                      item_name=menu_items[item_id].name, price=menu_items[item_id].price,
                      quantity=quantity, subtotal=menu_items[item_id].price * quantity)
            for item_id, quantity in quantities.items()
        ])
        return JsonResponse({"ok": True, "redirect": f"/order/{order.id}/", "order_id": order.id})
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Ma’lumotlarni tekshirib, qayta urinib ko‘ring."}, status=400)

def order_success(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id)
    return render(request, "orders/order_success.html", {"order": order})

def qr_code(request):
    target_url = f"{settings.SITE_URL}/"
    image = qrcode.make(target_url)
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
