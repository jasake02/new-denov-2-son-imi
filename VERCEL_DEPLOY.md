# Vercel Deploy

## Kerakli env o'zgaruvchilar

- `SECRET_KEY`
- `DATABASE_URL` yoki `POSTGRES_URL`
- `BLOB_READ_WRITE_TOKEN`

## Tavsiya etilgan storage

- Database: Vercel Marketplace orqali `Neon Postgres`
- Media uploads: `Vercel Blob`

## Deploy tartibi

1. GitHub repo'ni Vercel'ga ulang.
2. Storage bo'limidan Postgres va Blob yarating.
3. Yuqoridagi env qiymatlari loyiha ichiga tushganini tekshiring.
4. Deploy qiling.

## Muhim

- Ilk deploy paytida bo'sh Postgres bo'lsa, loyiha ichidagi `py_school/school.db` ma'lumotlari avtomatik ko'chiriladi.
- Admin paneldagi yangi rasmlar va media fayllar `Vercel Blob` ga yoziladi.
