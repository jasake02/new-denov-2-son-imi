# Denov 2-son ixtisoslashtirilgan maktab - School Website

ASP.NET Core 7.0 MVC web saytı yordamida yaratilgan "Denov 2-son ixtisoslashtirilgan maktab" uchun to'liq functional school management sistema.

## 🎯 Xususiyatlari

### Frontend Features
- ✅ Responsive dizayn (Bootstrap 5)
- ✅ Bosh sahifa (Home page) 
- ✅ Maktab haqida (About page)
- ✅ Yangiliklar (News) - dinamik bazadan
- ✅ Bo'limlar (Departments) - dinamik bazadan
- ✅ Bog'lanish formasi (Contact form)
- ✅ Mobile-friendly design

### Backend Features
- ✅ Admin panel with authentication
- ✅ Yangiliklar CRUD operatsiyalari
- ✅ Bo'limlar CRUD operatsiyalari
- ✅ Dashboard with statistics
- ✅ Contact messages management
- ✅ File upload (images)
- ✅ Responsive admin design

### Database
- ✅ SQL Server support
- ✅ Entity Framework Core
- ✅ Code-first migrations
- ✅ Seeded sample data

## 📋 Talablar

- Visual Studio 2022+ (v17.0 or higher)
- .NET 7.0 SDK
- SQL Server 2019+ yoki SQL Server Express
- Windows 10+ yoki Windows Server

## 🚀 O'rnatish va Boshlanish

### 1. Proyektni Ochish

```bash
# Visual Studio-da proyektni oching
1. Visual Studio-ni ochng
2. File -> Open -> Project/Solution
3. Denov2School/Denov2School.csproj faylini tanlang
```

### 2. Database Konfiguratsiyasi

#### Agar SQL Server Express mavjud bo'lsa:
- `appsettings.json` faylini oching
- Connection string da `Server=.\SQLEXPRESS` o'rnatganiga ishonch xosil qiling
- Yoki o'zingizning SQL Server manzilingizni ko'rsating

```json
"ConnectionStrings": {
    "DefaultConnection": "Server=.\\SQLEXPRESS;Database=Denov2School;Trusted_Connection=true;TrustServerCertificate=true;"
}
```

#### Agar Azure SQL yoki boshqa server bo'lsa:
```json
"ConnectionStrings": {
    "DefaultConnection": "Server=tcp:your_server.database.windows.net,1433;Database=Denov2School;User ID=your_username;Password=your_password;Encrypt=true;Connection Timeout=30;"
}
```

### 3. Bazani Yaratish

```bash
# Package Manager Console-da (Visual Studio ichida):
Add-Migration InitialCreate
Update-Database

# Yoki Terminal-da:
dotnet ef migrations add InitialCreate
dotnet ef database update
```

### 4. Proyektni Ishga Tushirish

```bash
# Visual Studio-da:
- Ctrl + F5 (Debugging bo'lmasdan) yoki
- F5 (Debugging bilan)

# Yoki Command Line-da:
dotnet run
```

### 5. Saytni Ochish

- Sayt: http://localhost:5000
- Admin Panel: http://localhost:5000/Admin/Account/Login

### 6. Admin Loginni Ishlatish

- **Foydalanuvchi**: admin
- **Parol**: admin

⚠️ **MUHIM**: Ishlashga chiqarishdan oldin (Production) parolni almashtiring!

## 📁 Proyekt Strukturasi

```
Denov2School/
├── Areas/
│   └── Admin/
│       ├── Controllers/    # Admin paneli kontrollerlari
│       └── Views/          # Admin paneli view-lari
├── Controllers/            # Frontend kontrollerlari
├── Models/                 # Database modellari
├── Views/                  # Frontend view-lari (Razor)
├── wwwroot/
│   ├── css/               # CSS fayllari
│   ├── js/                # JavaScript fayllari
│   ├── images/            # Rasmlar
│   └── uploads/           # Yuklangan fayllari
├── Data/
│   └── ApplicationDbContext.cs  # EF Core DbContext
├── Migrations/            # Database migrations
├── appsettings.json       # Konfiguratsiya
└── Program.cs             # Startup konfiguratsiyasi
```

## 🔐 Xavfsizlik Tavsiyalari

### Production-ga Ishga Tushirishdan Oldin:

1. **Admin Parolini O'zgartiring**
   ```csharp
   // Data/ApplicationDbContext.cs-da:
   // Default parolni kuchliroq parolga almashtiring
   UserName = "admin",
   Password = "StrongPassword123!@#"
   ```

2. **Parolni Hash Qiling**
   - ASP.NET Identity yoki BCrypt kabi kryptografik hashing ishlating
   - Plain text parol saqlamang!

3. **HTTPS Ishlatish**
   - Production-da HTTPS majburiy qiling
   - SSL sertifikatni o'rnatish

4. **Environment Variables**
   ```json
   // appsettings.Production.json yarating
   // Maxfiy ma'lumotlarni environment variables-da saqlang
   ```

5. **Authentication Tahkitlashtirish**
   - ASP.NET Identity bilan almashtiring
   - Two-factor authentication qo'shing

6. **Input Validation**
   - Barcha user input-larini validate qiling
   - SQL injection-dan himoya qiling

7. **File Upload Xavfsizligi**
   - Faqat rasm fayllari qabul qiling
   - File size limitini o'rnatishga ishonch xosil qiling

## 📱 Mobil-first Responsivity

Sayt barcha qurilmalar uchun optimallashtirilgan:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🗄️ Database Schema

### News Table
```sql
- Id (int, PK)
- Title (nvarchar(200))
- Content (nvarchar(max))
- ImagePath (nvarchar(max), nullable)
- CreatedDate (datetime)
- ModifiedDate (datetime, nullable)
```

### Department Table
```sql
- Id (int, PK)
- Name (nvarchar(150))
- Description (nvarchar(max), nullable)
- ImagePath (nvarchar(max), nullable)
- CreatedDate (datetime)
- ModifiedDate (datetime, nullable)
```

### ContactMessage Table
```sql
- Id (int, PK)
- FullName (nvarchar(100))
- Email (nvarchar(max))
- Message (nvarchar(max))
- CreatedDate (datetime)
- IsRead (bit)
```

### AdminUser Table
```sql
- Id (int, PK)
- UserName (nvarchar(50))
- Password (nvarchar(max))
- CreatedDate (datetime)
- LastLogin (datetime, nullable)
- IsActive (bit)
```

## 🌐 Domain Setup

### Hosting-ga Ishga Tushirish:

1. **Hosting Tanlash**
   - Windows hosting with .NET 7.0 support
   - SQL Server support mavjud bo'lishi kerak

2. **Ushbu Hostinglar Tavsiya Etiladi**
   - Azure App Service
   - HostGator ASP.NET Hosting
   - Bluehost Windows Hosting
   - GoDaddy ASP.NET Hosting

3. **Domain Sozlash**
   - denov2sonimi.uz domenini hosting-ga ulang
   - DNS settings-ni o'zgartiring

4. **Proyektni Publish Qilish**
   ```bash
   # Release mode-da publish qilish
   dotnet publish -c Release -o ./publish
   
   # Yoki Visual Studio-da:
   # Right-click on project -> Publish...
   ```

5. **Database Migratsiyalarini Ishga Tushirish**
   ```bash
   # Production-da migrations qo'llash
   dotnet ef database update --project Denov2School
   ```

## 📧 Email Setup (Optional)

Contact formasi uchun email qo'shish:

```csharp
// Startup-da email service qo'shish
builder.Services.AddScoped<IEmailService, EmailService>();

// appsettings.json-da
"EmailSettings": {
    "SmtpServer": "smtp.gmail.com",
    "SmtpPort": 587,
    "SenderEmail": "your-email@gmail.com",
    "SenderPassword": "your-app-password"
}
```

## 🐛 Troubleshooting

### Database Connection Error
```
Xato: "Unable to connect to the database"
Yechim: 
- Connection string-ni tekshiring
- SQL Server xizmati ishlamoqda-mi tekshiring
- Firewall sozlamalarini tekshiring
```

### Migration Error
```
Xato: "There is already an open reader..."
Yechim:
- Database-ni close qilaring
- Visual Studio-ni restart qilang
- SQL Server Management Studio-da database-ni close qilang
```

### Admin Login Not Working
```
Xato: Invalid username/password
Yechim:
- Database seeding tekshiring
- appsettings.json-da default admin user mavjudmi tekshiring
```

## 📚 Foydalanilgan Texnologiyalar

- **Framework**: ASP.NET Core 7.0
- **ORM**: Entity Framework Core 7.0
- **Database**: SQL Server
- **Frontend**: Bootstrap 5.3, HTML5, CSS3
- **JavaScript**: Vanilla JS
- **Authentication**: Cookie-based

## 📞 Support

Muammolar yoki savollar uchun:
- Email: info@denov2sonimi.uz
- Telefon: +998-76-228-25-64

## 📄 Litsenziya

Bu proyekt Denov 2-son ixtisoslashtirilgan maktab uchun yaratilgan.

## 🎓 Bilim Manbalar

- [ASP.NET Core Documentation](https://docs.microsoft.com/en-us/aspnet/core/)
- [Entity Framework Core](https://docs.microsoft.com/en-us/ef/core/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/)
- [SQL Server Documentation](https://docs.microsoft.com/en-us/sql/)

---

**Yaratilgan Sana**: 2024
**Versiya**: 1.0.0
**Last Updated**: Februari 2024
