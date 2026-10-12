# Mazali — QR-kod orqali restoran buyurtma tizimi

Django asosida yaratilgan boshlang‘ich loyiha. Mijozlar menyuni ochadi, stol raqamini tanlaydi, savatga taom qo‘shadi va buyurtma beradi. Buyurtmalar Django Admin panelida saqlanadi va boshqariladi.

## 1. O‘rnatish (Windows 10/11)

VS Code terminalini loyiha papkasida oching:

```bat
py -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py makemigrations orders
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Brauzerda:
- Menyu: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- QR-kod rasmi: http://127.0.0.1:8000/qr-code/

## 2. Menyu va taom qo‘shish

1. `/admin/` sahifasiga kiring.
2. Superuser yaratishda belgilagan login/parol bilan kiring.
3. Avval **Kategoriyalar** bo‘limida kategoriya yarating (masalan, Milliy taomlar, Ichimliklar).
4. **Taomlar** bo‘limida taom nomi, kategoriya, narx va taom rasmini kompyuteringizdan tanlab yuklang (rasm URL manzili kerak emas).
5. Menyu sahifasini yangilang.

## 3. Bitta QR-kodni ishlatish

Loyiha barcha mijozlar uchun bitta QR-kod yaratadi. U `SITE_URL/` manzilini ochadi. Sayt internetga joylangandan keyin `.env` yoki server muhitida `SITE_URL=https://saytingiz.uz` deb belgilang, serverni qayta ishga tushiring va `/qr-code/` manzilidagi QR-kodni yuklab olib chop eting.

`127.0.0.1` QR-kodi faqat o‘sha kompyuterda ishlaydi; mijozlar telefonidan foydalanishi uchun sayt internetda joylangan bo‘lishi kerak. Oddiy `runserver` ishlab chiqarish (production) serveri emas.

## 4. Buyurtmalar

Mijoz stol raqamini tanlaydi (1–18), taomlarni savatga qo‘shadi va buyurtma beradi. Server narxlarni ma’lumotlar bazasidan qayta tekshiradi. Buyurtma va buyurtma tarkibi ma’lumotlar bazasida saqlanadi.

Admin paneldagi **Buyurtmalar** bo‘limida buyurtmalarni ko‘ring va holatini yangilang:
- Yangi
- Qabul qilindi
- Tayyorlanmoqda
- Tayyor
- Yakunlandi
- Bekor qilindi

## 5. Muhim eslatma

Bu tayyor ishlaydigan demo/boshlang‘ich loyiha. Haqiqiy restoran uchun internet hosting, HTTPS, kuchli `DJANGO_SECRET_KEY`, zaxira nusxa, spamdan himoya va xodimlar uchun ruxsatlarni hostingga chiqarishdan oldin sozlang. Buyurtma holati hozircha sahifa yangilanganda ko‘rinadi; jonli bildirishnomalar (WebSocket/SMS/Telegram) alohida qo‘shiladi.


## Stol raqamlari va rasm yuklash
- Restoranda 20 ta stol bor: xaridor menyuda 1–20 oralig‘idan o‘z stolini tanlaydi.
- Barcha stollar uchun bitta QR-kod ishlatiladi. QR menyuni ochadi, stol raqami buyurtma berishdan oldin tanlanadi.
- Admin paneldagi **Taomlar** bo‘limida rasm maydonidan kompyuterdagi rasm faylini tanlang. URL kiritish shart emas.
- Lokal `127.0.0.1` QR-kodi boshqa telefonlarda ishlamaydi. Boshqa telefonlardan foydalanish uchun saytni internetga joylashtirib, `SITE_URL` ni ommaviy manzilga sozlang.
