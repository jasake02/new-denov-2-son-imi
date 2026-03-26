# 🚀 TEZKOR BOSHLASH QOʻLLANMASI

Denov 2-son ixtisoslashtirilgan maktab website-ni 5 daqiqada ishga tushirish!

## ✅ Talablar

- [ ] Visual Studio 2022+ o'rnatilgan
- [ ] .NET 7.0 SDK o'rnatilgan
- [ ] SQL Server Express o'rnatilgan
- [ ] Bu proyekt downloaded

## 🎯 Tezkor Boshlash (5 Daqiqa)

### 1️⃣ Proyektni Oching (1 min)

```powershell
# Proyekt papkasiga boring
cd "c:\Users\user\Desktop\maktab uchun webv\Denov2School"

# Visual Studio-da oching
start Denov2School.csproj
```

### 2️⃣ Connection String Tekshiring (30 sek)

`appsettings.json` faylini oching:

```json
"ConnectionStrings": {
    "DefaultConnection": "Server=.\\SQLEXPRESS;Database=Denov2School;Trusted_Connection=true;TrustServerCertificate=true;"
}
```

Server nomi to'g'rimi? Agar xilaf bo'lsa o'zgarting.

### 3️⃣ Database Yarating (2 min)

Visual Studio-da **Package Manager Console** oching (Tools → NuGet Package Manager → Package Manager Console)

```powershell
# Run qiling:
Update-Database
```

Kutun... Database yaratilmoqda!

### 4️⃣ Proyektni Ishga Tushiring (30 sek)

```
Ctrl + F5 (o'zga debugging bo'lmasdan)
```

Yoki:
```
F5 (debugging bilan)
```

### 5️⃣ Saytni Tekshiring (1 min)

**Sayt**: http://localhost:5000
- [ ] Bosh sahifa ochiladi
- [ ] Yangiliklar ko'rinadi
- [ ] Bo'limlar ko'rinadi

**Admin Panel**: http://localhost:5000/Admin/Account/Login
- Username: `admin`
- Password: `admin`

---

## 🎊 Tayyor!

Tabriklaymiz! Website-ingiz ishlamoqda! 🎉

### Nimani Qilsa Bo'ladi?

#### Frontend-da
- ✅ Bosh sahifani o'zgartiring
- ✅ Yangilik qo'shing
- ✅ Bo'lim qo'shing
- ✅ Contact formasi test qiling

#### Admin Panel-da
- ✅ Login qiling
- ✅ Dashboard-ni ko'ring
- ✅ Yangilik yarating
- ✅ Rasm upload qiling

---

## 🐛 Muammo Bo'lsa?

### Xato: Database Connection Failed

```
"Unable to connect to the database"
```

**Yechim:**
1. SQL Server Express ishlamoqda-mi tekshiring
2. Connection string-ni tekshiring
3. Database nomi to'g'rimi tekshiring

```powershell
# SQL Server status tekshiring:
Get-Service MSSQLServer
```

### Xato: Port Already in Use

```
"Address already in use: http://0.0.0.0:5000"
```

**Yechim:**
- Port-ni o'zgartiring `launchSettings.json`-da
- Yoki eski proceessi kill qiling

### Xato: Admin Login Not Working

```
"Invalid username/password"
```

**Yechim:**
1. Database created bo'lganiga ishonch xosil qiling
2. Admin user seeded bo'lganiga ishonch xosil qiling
3. Database recreate qiling:
```powershell
Update-Database -Force
```

---

## 📁 Fayllarni O'zgartirish

### Bosh Sahifani O'zgartirish

File: `Views/Home/Index.cshtml`

```html
<!-- Hero sarlavhasini o'zgarting -->
<h1 class="display-4 fw-bold mb-3">Yangi Sarlavha</h1>
```

### Rang O'zgartirish

File: `wwwroot/css/style.css`

```css
:root {
    --primary: #0d6efd;  /* Bu rang-ni o'zgarting */
}
```

### Footer Ma'lumotlarini O'zgartirish

File: `Views/Shared/_Layout.cshtml`

```html
<p class="text-muted">
    <i class="fas fa-phone"></i> +998-XX-XXX-XX-XX
</p>
```

---

## 🌐 Hosting-ga Ishga Tushirish

### 1. Proyektni Publish Qilish

```powershell
# Release mode-da build qiling
dotnet publish -c Release -o ./publish
```

### 2. Hosting-ni Tanlash

✅ Tavsiya etilgan:
- Azure App Service
- GoDaddy ASP.NET Hosting
- HostGator Windows Hosting

### 3. Upload Qilish

- FTP bilan `publish` papkasini upload qiling
- appsettings.json-da connection string-ni update qiling
- HTTPS-ni o'rnatish

### 4. Domain Ulash

- denov2sonimi.uz domenini DNS-da o'zgarting
- Hosting-da domain-ni ulang

---

## 📱 Mobile Test

```
Ctrl + Shift + M (Chrome DevTools)
```

Yoki:
- Galaxy S20
- iPad
- iPhone

Responsive qiladi?

---

## 📊 Stats

- **Lines of Code**: ~3000+
- **Database Tables**: 4
- **API Endpoints**: 15+
- **Frontend Pages**: 7
- **Admin Pages**: 8

---

## 🎓 Keyingi Qadamlar

1. ✅ Projectga O'rnatish va Ishga Tushirish
2. ✅ Admin Panel-dan Test Qilish
3. ✅ Content-ni Qo'shish
4. ✅ Design-ni Customize Qilish
5. ✅ Hosting-ga Ishga Tushirish
6. ✅ Domain-ni Ulash
7. ✅ SSL Certificate-ni O'rnatish

---

## 💡 Pro Tips

- 💾 Ko'p Code o'zgartiradigan bo'lsangiz, Git yordamida backup qiling
- 🔒 Admin parolni kuchliroq qilishni unutmang
- 📧 SMTP setup qiling contact formasi uchun
- 🖼️ Rasmlarni optimize qiling
- ⚡ Caching-ni o'rnatish

---

## 📞 Yordam

Muammo bo'lsa:
1. SETUP_GUIDE.md-ni o'qing
2. TECHNICAL_DOCS.md-ni o'qing
3. Xato xabarini web-da qidiring
4. Support-ga murojaat qiling

---

**Tayyor bo'ldingiz! Muvaffaqiyat! 🎉**

`Created: 2024 | Version: 1.0.0`
