from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField("Kategoriya nomi", max_length=100, unique=True)
    is_active = models.BooleanField("Faol", default=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ["name"]

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="items", verbose_name="Kategoriya")
    name = models.CharField("Taom nomi", max_length=160)
    description = models.TextField("Tavsif", blank=True)
    price = models.DecimalField("Narxi (so'm)", max_digits=12, decimal_places=0)
    image = models.ImageField("Taom rasmi", upload_to="menu/", blank=True, null=True)
    is_available = models.BooleanField("Menyuda mavjud", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Taom"
        verbose_name_plural = "Taomlar"
        ordering = ["category__name", "name"]

    def __str__(self):
        return f"{self.name} — {self.price} so'm"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Yangi"
        ACCEPTED = "accepted", "Qabul qilindi"
        COOKING = "cooking", "Tayyorlanmoqda"
        READY = "ready", "Tayyor"
        COMPLETED = "completed", "Yakunlandi"
        CANCELLED = "cancelled", "Bekor qilindi"

    table_number = models.PositiveSmallIntegerField("Stol raqami")
    customer_name = models.CharField("Mijoz ismi", max_length=100, blank=True)
    customer_phone = models.CharField("Telefon", max_length=30, blank=True)
    note = models.TextField("Izoh", blank=True)
    status = models.CharField("Holat", max_length=20, choices=Status.choices, default=Status.NEW)
    total = models.DecimalField("Jami (so'm)", max_digits=12, decimal_places=0, default=0)
    created_at = models.DateTimeField("Buyurtma vaqti", default=timezone.now)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Buyurtma #{self.pk} — {self.table_number}-stol"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Buyurtma")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Taom")
    item_name = models.CharField("Taom nomi (nusxa)", max_length=160)
    price = models.DecimalField("Narxi (so'm)", max_digits=12, decimal_places=0)
    quantity = models.PositiveSmallIntegerField("Soni", default=1)
    subtotal = models.DecimalField("Jami", max_digits=12, decimal_places=0)

    class Meta:
        verbose_name = "Buyurtma taomi"
        verbose_name_plural = "Buyurtma taomlari"

    def __str__(self):
        return f"{self.item_name} x {self.quantity}"
