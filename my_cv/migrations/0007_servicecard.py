from django.db import migrations, models


CARDS = [
    {
        "title": "بک‌اند پایدار",
        "title_en": "Reliable",
        "highlight": "و مقیاس‌پذیر",
        "highlight_en": "backends",
        "body": "با Django و معماری تمیز، APIهای RESTful و پایگاه‌داده‌ای می‌سازم که با رشد کسب‌وکار شما کند نمی‌شن و زیر فشار ترافیک نمی‌شکنن.",
        "body_en": "I build Django systems with a clean architecture, REST APIs, and databases that stay fast as your business grows and do not break under traffic.",
        "static_image": "snapfolio/img/services/services-1.webp",
        "accent": "accent",
        "order": 1,
    },
    {
        "title": "یکپارچه‌سازی و تحلیل",
        "title_en": "Data integration",
        "highlight": "داده",
        "highlight_en": "and analysis",
        "body": "داده‌های پراکنده رو با وب‌اسکرپینگ، ETL و یکپارچه‌سازی API جمع و تمیز می‌کنم و به گزارش و تصمیم قابل اتکا تبدیل می‌کنم؛ بدون کار دستی تکراری.",
        "body_en": "I collect and clean scattered data with web scraping, ETL, and API integration, then turn it into reports and decisions you can trust — without repetitive manual work.",
        "static_image": "snapfolio/img/services/services-2.webp",
        "accent": "light",
        "order": 2,
    },
    {
        "title": "هوش مصنوعی",
        "title_en": "Practical",
        "highlight": "کاربردی",
        "highlight_en": "AI",
        "body": "چت‌بات‌های دانش‌محور (RAG)، دستیارهای هوشمند و سیستم‌های توصیه‌گر که روی داده‌ی خود شما کار می‌کنن و در محیط واقعی هم جواب می‌دن، نه فقط در دمو.",
        "body_en": "Knowledge chatbots (RAG), intelligent assistants, and recommenders that run on your own data and hold up in production, not just in a demo.",
        "static_image": "snapfolio/img/services/services-3.webp",
        "accent": "bronze",
        "order": 3,
    },
    {
        "title": "کشف و تحلیل نیاز",
        "title_en": "Discover and scope",
        "highlight": "",
        "highlight_en": "",
        "body": "قبل از نوشتن اولین خط کد، مسئله رو دقیق می‌شناسیم. در یک جلسه‌ی عمیق، فرآیند فعلی‌تون رو بررسی می‌کنم، ریسک‌ها رو شناسایی می‌کنم و دامنه‌ی نسخه‌ی اول رو مشخص می‌کنم؛ تا بدونید دقیقاً چی ساخته می‌شه و هزینه‌ی اشتباه نمی‌دید.",
        "body_en": "Before the first line of code, we get the problem clear. In one deep session I review your current process, name the risks, and set the scope of the first version — so you know exactly what gets built and you do not pay for a wrong start.",
        "static_image": "snapfolio/img/portfolio/portfolio-1.webp",
        "accent": "accent",
        "order": 4,
    },
    {
        "title": "طراحی و پیاده‌سازی",
        "title_en": "Design and build",
        "highlight": "",
        "highlight_en": "",
        "body": "ایده رو به محصولی تبدیل می‌کنم که کاربر واقعی بتونه ازش استفاده کنه: از طراحی و اتصال به داده و مدل هوش مصنوعی تا استقرار روی سرور و تحویل کامل، همراه با مستندات.",
        "body_en": "I turn the idea into a product real users can use: from design and connecting data and the AI model, through server deployment and a full handoff, with documentation.",
        "static_image": "snapfolio/img/portfolio/portfolio-2.webp",
        "accent": "light",
        "order": 5,
    },
    {
        "title": "پشتیبانی و بهبود مستمر",
        "title_en": "Support and improvement",
        "highlight": "",
        "highlight_en": "",
        "body": "بعد از انتشار هم کنارتونم. سیستم رو پایش می‌کنم، خطاها رو سریع رفع می‌کنم، کیفیت پاسخ‌های مدل رو بهتر می‌کنم و ظرفیت لازم برای تغییرات کوچک و رشد محصول رو در نظر می‌گیرم.",
        "body_en": "I stay with you after launch. I monitor the system, fix errors quickly, improve the model’s answers, and leave room for small changes and for the product to grow.",
        "static_image": "snapfolio/img/portfolio/portfolio-5.webp",
        "accent": "bronze",
        "order": 6,
    },
]


def seed_cards(apps, schema_editor):
    ServiceCard = apps.get_model("my_cv", "ServiceCard")
    for card in CARDS:
        ServiceCard.objects.update_or_create(
            title=card["title"],
            defaults={**card, "link": "#contact", "is_visible": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("my_cv", "0006_confidential_tag"),
    ]

    operations = [
        migrations.CreateModel(
            name="ServiceCard",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160, verbose_name="عنوان")),
                ("title_en", models.CharField(blank=True, max_length=160, verbose_name="Title (EN)")),
                ("highlight", models.CharField(blank=True, help_text="بخش دوم عنوان، مثلاً «و مقیاس‌پذیر». اگر خالی باشد فقط عنوان نشان داده می‌شود.", max_length=80, verbose_name="ادامه‌ی عنوان")),
                ("highlight_en", models.CharField(blank=True, max_length=80, verbose_name="Highlight (EN)")),
                ("body", models.TextField(verbose_name="متن کارت")),
                ("body_en", models.TextField(blank=True, verbose_name="Body (EN)")),
                ("image", models.ImageField(blank=True, null=True, upload_to="services/", verbose_name="تصویر")),
                ("static_image", models.CharField(blank=True, help_text="مسیر داخل static، اگر تصویر بالا خالی باشد. مثلاً snapfolio/img/services/services-1.webp", max_length=180, verbose_name="تصویر پیش‌فرض")),
                ("link", models.CharField(blank=True, default="#contact", max_length=200, verbose_name="لینک")),
                ("accent", models.CharField(choices=[("accent", "سبز"), ("light", "روشن"), ("bronze", "برنزی")], default="accent", max_length=20, verbose_name="رنگ کارت")),
                ("is_visible", models.BooleanField(default=True, verbose_name="نمایش در سایت")),
                ("order", models.PositiveIntegerField(default=0, verbose_name="ترتیب")),
            ],
            options={
                "verbose_name": "کارت خدمات",
                "verbose_name_plural": "کارت‌های خدمات",
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(seed_cards, migrations.RunPython.noop),
    ]
