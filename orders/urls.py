from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("", views.menu, name="menu"),
    path("order/", views.create_order, name="create_order"),
    path("order/<int:order_id>/", views.order_success, name="order_success"),
    path("qr-code/", views.qr_code, name="qr_code"),
]
