# Denov 2-son ixtisoslashtirilgan Maktab - Technical Documentation

## 📖 Loyihani Tushuntirish

Bu proyekt "Denov 2-son ixtisoslashtirilgan maktab" uchun to'liq funksional school management va website tizimi. 
ASP.NET Core 7.0 MVC, Entity Framework Core, va SQL Server bilan yaratilgan.

### Asosiy Komponentlar

#### 1. Frontend (User-Facing)

**Routes/Pages:**
- `/` - Bosh sahifa (Home)
- `/Home/About` - Maktab haqida (About)
- `/News` - Yangiliklar (News listing)
- `/News/Detail/{id}` - Bir yangilik (News detail)
- `/Departments` - Bo'limlar (Departments listing)
- `/Departments/Detail/{id}` - Bir bo'lim (Department detail)
- `/Contact` - Bog'lanish formasi (Contact form)

**Features:**
- Responsive design (mobile-first)
- Bootstrap 5.3 UI components
- SEO-friendly
- Fast loading
- Image optimization

#### 2. Backend Admin Panel

**Routes/Pages:**
- `/Admin/Account/Login` - Admin login
- `/Admin/Dashboard/Index` - Dashboard with statistics
- `/Admin/News/Index` - News list
- `/Admin/News/Create` - Create news
- `/Admin/News/Edit/{id}` - Edit news
- `/Admin/News/Delete/{id}` - Delete news
- `/Admin/Departments/Index` - Departments list
- `/Admin/Departments/Create` - Create department
- `/Admin/Departments/Edit/{id}` - Edit department
- `/Admin/Departments/Delete/{id}` - Delete department

**Features:**
- User authentication (Cookie-based)
- Authorization [Authorize] attribute
- CRUD operations
- Image upload
- Dashboard statistics
- Responsive admin UI

## 🏗️ Arxitektura

### MVC Pattern

```
Models/
├── News.cs                    # News entity
├── Department.cs              # Department entity
├── ContactMessage.cs          # Contact message entity
└── AdminUser.cs              # Admin user entity

Controllers/
├── HomeController.cs          # Public pages
├── NewsController.cs          # Public news
├── DepartmentsController.cs    # Public departments
└── ContactController.cs       # Contact form

Areas/Admin/Controllers/
├── AccountController.cs       # Login/Logout
├── DashboardController.cs     # Admin dashboard
├── NewsController.cs          # Admin news management
└── DepartmentsController.cs   # Admin department management

Views/
├── Home/
│   ├── Index.cshtml
│   └── About.cshtml
├── News/
│   ├── Index.cshtml
│   └── Detail.cshtml
├── Departments/
│   ├── Index.cshtml
│   └── Detail.cshtml
├── Contact/
│   └── Index.cshtml
└── Shared/
    └── _Layout.cshtml

Areas/Admin/Views/
├── Account/
│   └── Login.cshtml
├── Dashboard/
│   └── Index.cshtml
├── News/
│   ├── Index.cshtml
│   ├── Create.cshtml
│   └── Edit.cshtml
├── Departments/
│   ├── Index.cshtml
│   ├── Create.cshtml
│   └── Edit.cshtml
└── Shared/
    └── _Layout.cshtml
```

## 💾 Database Schema

### ApplicationDbContext

```csharp
public DbSet<News> News { get; set; }
public DbSet<Department> Departments { get; set; }
public DbSet<ContactMessage> ContactMessages { get; set; }
public DbSet<AdminUser> AdminUsers { get; set; }
```

### Entity Relationships

```
News (1) ──────── (Many) No direct relationship
Department (1) ──── (Many) No direct relationship
ContactMessage (1) ──── (Many) No direct relationship
AdminUser (1) ──── (Many) No direct relationship
```

## 🔐 Authentication & Authorization

### Cookie-based Authentication

```csharp
// Program.cs-da:
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options => 
    {
        options.LoginPath = "/Admin/Account/Login";
        options.LogoutPath = "/Admin/Account/Logout";
    });

// Controller-da:
[Authorize]
public class DashboardController : Controller { }
```

### Login Flow

1. User kredentiallarni kiritadi
2. Database-da tekshiriladi
3. Agar to'g'ri bo'lsa, cookie tizimiga sign in qiladi
4. User authenticate qilinadi

## 📊 Database Initialization

### Seeded Data

**Default Admin User:**
- Username: `admin`
- Password: `admin`

**Sample Departments:**
- Tabiiy Fanlar (Science)
- Riyoziyat va Informatika (Math & IT)
- Til va Literatura (Languages & Literature)

**Sample News:**
- 2 sample news items with dates

## 🎨 Frontend Styling

### CSS Files
- `wwwroot/css/style.css` - Main website styles
- `wwwroot/css/admin-style.css` - Admin panel styles

### CSS Features
- Custom variables (CSS variables)
- Responsive breakpoints
- Animations (fade-in, slide)
- Hover effects
- Bootstrap 5 integration

### Color Scheme
- Primary: #0d6efd (Blue)
- Success: #198754 (Green)
- Warning: #ffc107 (Yellow)
- Danger: #dc3545 (Red)
- Info: #0dcaf0 (Cyan)

## 📱 Responsive Design

### Breakpoints
- Mobile: < 576px
- Tablet: 576px - 768px
- Desktop: 768px - 1200px
- Large: 1200px+

### Mobile-First Approach
- Base styles untuk mobile
- Media queries uchun katta ekranlar

## 🔧 JavaScript Functions

### Main Website (script.js)

```javascript
// Validation
validateForm(formId)

// Notifications
showSuccessMessage(message, duration)
showErrorMessage(message, duration)

// Utilities
formatDate(dateString)
confirmDelete(message)
copyToClipboard(text)
scrollToTop()
```

### Admin Panel (admin-script.js)

```javascript
// Notifications
showSuccess(message)
showError(message)
showWarning(message)

// Forms
validateForm(formId)
autoSaveForm(formId)
clearFormAutoSave(formId)

// Files
validateFileSize(file, maxSizeMB)
validateFileType(file, allowedTypes)
previewImage(inputId, previewId)

// Table operations
filterTable(inputId, tableId)
exportTableToCSV(tableId, filename)
printTable(tableId)
```

## 🚀 Deployment Process

### Step-by-step

1. **Code Preparation**
   ```bash
   # Build release
   dotnet build -c Release
   ```

2. **Database Migration**
   ```bash
   dotnet ef migrations add [MigrationName]
   dotnet ef database update
   ```

3. **Publishing**
   ```bash
   dotnet publish -c Release -o ./publish
   ```

4. **Upload to Hosting**
   - FTP yoki Web Deploy ishlating
   - wwwroot folder-ni transfer qiling
   - appsettings.json-ni update qiling

5. **Domain Configuration**
   - DNS settings-ni update qiling
   - SSL certificate-ni install qiling
   - HTTPS-ni redirect qiling

## 📝 Code Comments

### C# Code Comments

```csharp
/// <summary>
/// Batafsil tavsifi
/// </summary>
public void MethodName()
{
    // Implement logic
}
```

### HTML Comments

```html
<!-- Section tavsifi -->
<section>
    Content
</section>
```

### CSS Comments

```css
/* ===================================
   SECTION NAME
   =================================== */
```

## 🧪 Testing

### Manual Testing Checklist

**Frontend:**
- [ ] Barcha sahifalar ochiladi
- [ ] Formalar submit qilinadi
- [ ] Responsivity tekshirildi
- [ ] Images load qilinadi
- [ ] Links to'g'ri ishlaydi

**Admin Panel:**
- [ ] Login qilish ishlaydi
- [ ] News qo'shish/tahrirlash/o'chirish
- [ ] Department qo'shish/tahrirlash/o'chirish
- [ ] Image upload ishlaydi
- [ ] Dashboard stats dogri

**Database:**
- [ ] Migrations qo'llanildi
- [ ] Data save qilinadi
- [ ] Relationships to'g'ri

## 🔍 Performance Optimization

### Implemented
- ✅ CSS minification (Bootstrap CDN)
- ✅ JS bundling (Bootstrap JS)
- ✅ Image lazy loading
- ✅ Caching strategies
- ✅ Database query optimization

### Recommendations
- Add CDN for static files
- Enable GZIP compression
- Implement caching headers
- Optimize database indexes
- Use async/await extensively

## 🐛 Common Issues

### Issue 1: Database Connection Fails
**Sabab**: Connection string noto'g'ri
**Yechim**: appsettings.json-da tekshiring

### Issue 2: Migrations Don't Apply
**Sabab**: Database mavjud emas
**Yechim**: `dotnet ef database update`

### Issue 3: Admin Login Not Working
**Sabab**: Seeded data mavjud emas
**Yechim**: Database recreate qiling

### Issue 4: Images Don't Upload
**Sabab**: wwwroot/uploads folder mavjud emas
**Yechim**: Folder yarating yoki permission tekshiring

## 📈 Future Enhancements

- [ ] Student portal
- [ ] Parent notifications
- [ ] Attendance tracking
- [ ] Grade management
- [ ] Payment system
- [ ] Mobile app
- [ ] SMS notifications
- [ ] Email newsletters
- [ ] Advanced search
- [ ] User roles & permissions

## 📚 External Resources

- [ASP.NET Core Docs](https://docs.microsoft.com/aspnet/core)
- [EF Core Docs](https://docs.microsoft.com/ef/core)
- [Bootstrap Docs](https://getbootstrap.com/docs)
- [SQL Server Docs](https://docs.microsoft.com/sql)

## 📞 Technical Support

Muammolar uchun yozib qo'ying:
- Email: support@denov2sonimi.uz
- Telefon: +998-76-228-25-64

---

**Oxirgi yangilanish**: Februari 2024
**Versiya**: 1.0.0
**Status**: ✅ Production Ready
