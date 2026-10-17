"""Seed the database with Mohammad's real portfolio content.

Idempotent: safe to run multiple times (uses update_or_create on natural keys).
Run with:  python manage.py seed_content
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction

from my_cv.models import (
    Certificate,
    Experience,
    Profile,
    Project,
    ProjectImage,
    Skill,
    SkillCategory,
    SocialLink,
)

ABOUT = (
    "با Django وب‌سایت و بک‌اند می‌سازم، داده را تحلیل می‌کنم تا به تصمیم برسد، و عامل "
    "هوشمند، RAG و اتوماسیون n8n را به جریان کار تیم وصل می‌کنم. در انتشارات، سیستم "
    "فروش، انبار و تولید کتاب را از نو چیدم و بخش‌های پژوهش، اجرا، بازرگانی و حسابداری "
    "را به هم وصل کردم؛ برای همین قبل از نوشتن کد، فرآیند کسب‌وکار را دقیق می‌بینم. "
    "چهار وب‌سایت منتشرشده نمونه‌ی همین کار است."
)

ABOUT_EN = (
    "I build websites and backends with Django, analyze data until it supports a "
    "decision, and wire AI agents, RAG, and n8n automation into how a team actually "
    "works. At a publishing house I rebuilt the sales, warehouse, and book-production "
    "systems and connected research, operations, commerce, and accounting, so I read "
    "the business process carefully before I write code. Four live websites show "
    "that work."
)

# (name, name_en, icon, order, [(skill, skill_en, level, featured), ...])
# level 1–5 maps to ~48–92% (never 100).
SKILLS = [
    ("کدنویسی", "Coding", "fas fa-code", 1, [
        ("Python", "", 5, True),
        ("Django", "", 5, True),
        ("REST API", "", 4, True),
        ("الگوریتم", "Algorithms", 3, True),
    ]),
    ("پایگاه داده", "Database", "fas fa-database", 2, [
        ("PostgreSQL", "", 4, True),
        ("SQL Server", "", 3, True),
        ("اصول پایگاه داده", "Database fundamentals", 4, True),
        ("ChromaDB", "", 4, True),
    ]),
    ("تحلیل داده", "Data Analysis", "fas fa-chart-line", 3, [
        ("تحلیل داده", "Data analysis", 4, True),
        ("Power BI", "", 4, True),
    ]),
    ("هوش مصنوعی", "Artificial Intelligence", "fas fa-brain", 4, [
        ("LangChain", "", 4, True),
        ("RAG", "", 4, True),
        ("OpenAI API", "", 4, True),
        ("سیستم توصیه‌گر", "Recommender systems", 3, True),
    ]),
    ("DevOps", "DevOps", "fas fa-cubes", 5, [
        ("Docker", "", 4, True),
        ("Git", "", 5, True),
        ("Liara", "", 4, True),
        ("مبانی شبکه", "Networking basics", 3, True),
    ]),
    ("اتوماسیون", "Automation", "fas fa-robot", 6, [
        ("n8n", "", 4, True),
    ]),
    ("وب‌اسکرپینگ", "Web Scraping", "fas fa-spider", 7, [
        ("BeautifulSoup", "", 4, True),
        ("Camoufox", "", 4, True),
        ("یکپارچه‌سازی API", "API integration", 4, True),
    ]),
    ("مهارت‌های نرم", "Soft skills", "fas fa-lightbulb", 8, [
        ("حل مسئله", "Problem solving", 4, True),
        ("کار تیمی", "Teamwork", 4, True),
        ("ارتباط مؤثر", "Communication", 4, True),
    ]),
]

EXPERIENCES = [
    {
        "role": "مدیر داخلی انتشارات",
        "role_en": "Internal Publishing Manager",
        "organization": "پژوهشکده مطالعات و تحقیقات بین‌الملل ابرار معاصر تهران",
        "organization_en": "Abrar Moaser Tehran Institute for International Studies",
        "location": "تهران",
        "location_en": "Tehran",
        "period": "خرداد ۱۴۰۲ – اکنون",
        "period_en": "June 2023 – Present",
        "is_current": True,
        "order": 1,
        "description": (
            "سیستم فروش موجود را بازطراحی کردم و یک سیستم تازه برای فروش ساختم.\n"
            "انبارداری را از دستورالعمل نگهداری تا ثبت ورود، خروج و سفارش پوشش دادم.\n"
            "سیستم طراحی و تولید کتاب را چیدم.\n"
            "ارتباط پایدار بین معاونت پژوهشی، بخش اجرایی، بازرگانی و حسابداری را برقرار کردم.\n"
            "ساختارهای مالی را شفاف کردم.\n"
            "کالاهای امانی و نمایندگی فروش را قابل رصد کردم."
        ),
        "description_en": (
            "I redesigned the existing sales system and built a new one.\n"
            "Warehousing covered storage rules through recording inbound, outbound, and orders.\n"
            "I set up the book design and production system.\n"
            "I connected research, operations, commerce, and accounting so the link would hold.\n"
            "I made the financial structure easier to see through.\n"
            "Consignment goods and sales representation became trackable."
        ),
    },
    {
        "role": "منشی دفتر قاضی و مسئول دبیرخانه",
        "role_en": "Judge's Office Secretary & Registry Officer",
        "organization": "دادسرای نظامی جنوب‌غرب استان تهران",
        "organization_en": "Military Prosecutor's Office, Southwest Tehran",
        "location": "تهران",
        "location_en": "Tehran",
        "period": "دی ۱۳۹۹ – آذر ۱۴۰۱",
        "period_en": "January 2021 – December 2022",
        "is_current": False,
        "order": 2,
        "description": "کار اداری دبیرخانه در دوران خدمت.",
        "description_en": "Registry work during military service.",
    },
    {
        "role": "دستیار داخلی حوزه‌ی افغانستان (بخش بین‌الملل)",
        "role_en": "Internal Assistant for Afghanistan Desk (International)",
        "organization": "دفتر خبری ایران",
        "organization_en": "Iran News Office",
        "location": "تهران",
        "location_en": "Tehran",
        "period": "اردیبهشت ۱۳۹۸ – آبان ۱۳۹۹",
        "period_en": "May 2019 – November 2020",
        "is_current": False,
        "order": 3,
        "description": "هماهنگی داخلی بخش بین‌الملل.",
        "description_en": "Internal coordination on an international desk.",
    },
    {
        "role": "مسئول دفتر",
        "role_en": "Office Manager",
        "organization": "انجمن علوم سیاسی ایران",
        "organization_en": "Iranian Political Science Association",
        "location": "تهران",
        "location_en": "Tehran",
        "period": "مهر ۱۳۹۷ – مرداد ۱۳۹۸",
        "period_en": "October 2018 – August 2019",
        "is_current": False,
        "order": 4,
        "description": "مدیریت دفتر و هماهنگی جلسه‌ها.",
        "description_en": "Office management and meeting coordination.",
    },
]

COVER_ROOT = settings.BASE_DIR / "portfolio-samples"
N8N_COVER_DIR = COVER_ROOT / "n8n"

PROJECTS = [
    {
        "title": "پذیرش ایمیل و نوبت‌دهی کلینیک",
        "title_en": "Clinic inbox and appointment booking",
        "slug": "clinic-inbox-appointments",
        "summary": "گردش‌کار n8n برای خواندن ایمیل بیمار، تشخیص نیت با هوش مصنوعی و پاسخ نوبت از روی تقویم قابل‌ویرایش بیمارستان.",
        "summary_en": "An n8n workflow that reads patient email, classifies intent with AI, and replies with a slot from the hospital-owned calendar.",
        "category": Project.Category.AUTOMATION,
        "status": Project.Status.COMPLETED,
        "problem": (
            "پذیرش باید برای هر ایمیل تشخیص دهد بیمار وقت آزاد می‌خواهد، ساعت مشخصی را رزرو کرده، "
            "یا متن اصلاً قابل فهم نیست؛ تقویم هم فقط باید دست بیمارستان باشد."
        ),
        "problem_en": (
            "Front desk had to tell whether an email asked for any slot, a specific time, "
            "or was unclear — and the calendar had to stay with the hospital, not the patient."
        ),
        "solution": (
            "در n8n ایمیل به تقویم ثابت بیمارستان چسبانده می‌شود، مدل نیت را به سه شاخه می‌برد، "
            "و پاسخ با قالب ثابت می‌رود: نزدیک‌ترین نوبت، تأیید یا جایگزین ساعت درخواستی، "
            "و پاسخ از دانش خدمات یا راهنمای بازنویسی ایمیل."
        ),
        "solution_en": (
            "n8n attaches a hospital-editable calendar, an AI switch splits three intents, "
            "and static templates reply with the next free slot, confirm or replace a requested "
            "time, or answer from clinic services / a rewrite guide."
        ),
        "outcome": "سه مسیر پاسخ مشخص روی یک بوم، با ساعات و نوبت‌هایی که فقط پرسنل بیمارستان عوض می‌کنند.",
        "outcome_en": "Three clear reply paths on one canvas, with hours and slots only staff can edit.",
        "cover_file": "n8n/01-clinic-inbox-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 0,
        "skills": ["n8n", "OpenAI API"],
    },
    {
        "title": "نبض جست‌وجو — بریف رقابتی کلینیک",
        "title_en": "Search pulse — clinic competitive brief",
        "slug": "brand-search-pulse",
        "summary": "پایش هفتگی رتبه و سهم صدا در گوگل که به‌جای لاگ خام، سه‌اقدام اجرایی برای مدیر بازاریابی می‌سازد.",
        "summary_en": "A weekly rank and share-of-voice check that turns SERP data into three actions for the marketing lead.",
        "category": Project.Category.AUTOMATION,
        "status": Project.Status.COMPLETED,
        "problem": "لاگ رتبه به مدیر بازاریابی نمی‌گوید این هفته کدام صفحه خدمت را عوض کند یا چرا اسنیپت از دست رفته است.",
        "problem_en": "A rank log does not tell a marketing lead which service page to change this week, or why a snippet was lost.",
        "solution": (
            "هر دوشنبه کلمات برند، خدمت و رقیب از گوگل‌شیت خوانده می‌شود، نتایج گوگل جمع می‌شود، "
            "رتبه و سهم صدا با هفته قبل مقایسه می‌شود و با قواعد ثابت (افت رتبه، اسنیپت، بسته محلی) "
            "یک بریف ایمیلی سه اقدام ساخته و ذخیره می‌شود."
        ),
        "solution_en": (
            "Every Monday brand, service, and competitor keywords are read from Sheets, Google results "
            "are collected, rank and share of voice are compared with last week, and fixed rules "
            "(rank drop, snippet, local pack) produce a three-action email brief."
        ),
        "outcome": "گزارش دوشنبه برای بازاریابی کلینیک: چه عوض شده و دقیقاً سه کار این هفته چیست.",
        "outcome_en": "A Monday brief for clinic marketing: what changed, and the three jobs for the week.",
        "cover_file": "n8n/02-brand-search-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 1,
        "skills": ["n8n", "OpenAI API", "یکپارچه‌سازی API"],
    },
    {
        "title": "وب‌سایت مطب دکتر وحید عبدالرحیمی",
        "title_en": "Dr. Vahid Abdolrahimi clinic website",
        "summary": "سایت سه‌زبانه‌ی فوق تخصص شبکیه و لیزر، با رزرو نوبت، خدمات مطب و جراحی، و چت‌بات شخصی پزشک به فارسی، انگلیسی و عربی.",
        "summary_en": "Trilingual retina and laser specialist site with booking, clinic and surgery services, and the doctor’s own chatbot in Persian, English, and Arabic.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "problem": (
            "مراجع باید خدمات شبکیه و لیزر، محیط مطب و مسیر نوبت را یک‌جا ببیند، "
            "و پرسش‌های تکراری به فارسی، انگلیسی و عربی جواب بگیرند بدون اینکه هر بار منتظر تماس بماند."
        ),
        "problem_en": (
            "Patients needed retina and laser services, the clinic, and the booking path in one place, "
            "and repeated questions answered in Persian, English, and Arabic without waiting on a phone call."
        ),
        "solution": (
            "سایت مطب را با صفحه‌های خانه، درباره دکتر، خدمات مطب (ویزیت، اپتومتری، تجویز عینک، "
            "لنز و پروتز، تصویربرداری)، خدمات جراحی (بلفاروپلاستی، لیزر دور چشم، لیفت شقیقه، "
            "افتادگی پلک، توده و باکل)، مقالات، گالری، ویدیو و تماس ساختم. زبان سایت فارسی، "
            "انگلیسی و عربی است. چت‌بات شخصی دکتر عبدالرحیمی روی همین سایت به هر سه زبان فعال است "
            "و درباره خدمات و مسیر نوبت راهنمایی می‌کند. آدرس مطب در ونک، تلفن‌ها و ساعت کاری "
            "شنبه تا پنجشنبه ۱۱ تا ۱۴ در صفحه و پابرگ آمده است."
        ),
        "solution_en": (
            "I built the clinic site with home, about, clinic services (visits, optometry, glasses, "
            "lenses and prostheses, imaging), surgery (blepharoplasty, periocular laser, temple lift, "
            "ptosis, lesions, and buckle), articles, gallery, videos, and contact. The site runs in "
            "Persian, English, and Arabic. Dr. Abdolrahimi’s personal chatbot is live on the same site "
            "in all three languages and guides visitors through services and booking. The Vanak address, "
            "phone numbers, and Saturday–Thursday 11:00–14:00 hours sit on the page and in the footer."
        ),
        "outcome": (
            "سایت روی drabdolrahimi.com زنده است: معرفی فوق تخصص شبکیه و لیزر، رزرو نوبت، "
            "و چت‌بات سه‌زبانه در دسترس بیماران."
        ),
        "outcome_en": (
            "The site is live at drabdolrahimi.com: retina and laser practice, appointment booking, "
            "and a trilingual chatbot available to patients."
        ),
        "github_url": "https://github.com/Meska75/drvahidabdolrahimi",
        "live_url": "https://drabdolrahimi.com/",
        "cover_file": "sites/drabdolrahimi-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 5,
        "skills": ["Django", "Liara"],
    },
    {
        "title": "Pop360",
        "title_en": "Pop360",
        "summary": "سایت معرفی پاپ۳۶۰ برای طراحی وب، هوش مصنوعی، داده و اتوماسیون، با بلاگ، جستجو و فرم سفارش پروژه.",
        "summary_en": "Pop360’s site for web, AI, data, and automation, with a blog, search, and a project-order form.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "problem": (
            "کسب‌وکار باید قبل از ساخت بفهمد وب، هوش مصنوعی، داده یا اتوماسیون کدام‌یک ارزش دارد "
            "و سفارش را از کجا شروع کند؛ معرفی خدمات هم نباید با آموزش قاطی شود."
        ),
        "problem_en": (
            "A business needs to see whether web, AI, data, or automation is worth building, "
            "and where an order starts — without mixing the service list into the training section."
        ),
        "solution": (
            "صفحه خانه پاپ۳۶۰ را حول همین سؤال چیدم: معرفی کوتاه، سپس هفت خدمت با لینک صفحه خودشان "
            "(اپ اندروید، وب‌سایت با Django، داشبورد، دستیار هوش مصنوعی، وب‌اپ، دیتاساینس و اتوماسیون). "
            "آموزش از منوی خدمات جداست. تیم، بلاگ، جستجو، ورود و ثبت‌نام، و دکمه سفارش پروژه "
            "در نوار بالا در دسترس است."
        ),
        "solution_en": (
            "I shaped the Pop360 homepage around that question: a short intro, then seven services "
            "each with its own page (Android apps, Django websites, dashboards, AI assistants, "
            "web apps, data science, and automation). Training stays out of the services menu. "
            "The team, blog, search, sign-in, and project-order button sit in the top bar."
        ),
        "outcome": "pop360.ir منتشر است؛ مسیر مشاوره و سفارش پروژه از خانه و منو باز است و بلاگ جدا از فهرست خدمات دیده می‌شود.",
        "outcome_en": "pop360.ir is published; consultation and project orders start from the home page and menu, and the blog stays separate from the service list.",
        "live_url": "https://pop360.ir/",
        "cover_file": "sites/pop360-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 6,
        "skills": ["Django"],
    },
    {
        "title": "آراز دید نورا",
        "title_en": "Araz Did Noura",
        "summary": "سایت سه‌زبانه‌ی مرکز پروتز چشم سفارشی در تهران، با رزرو مشاوره، خدمات ساخت و پولیش، و مجله.",
        "summary_en": "Trilingual site for a custom ocular-prosthesis studio in Tehran, with consult booking, fabrication and polish services, and a journal.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "problem": (
            "مراجع بعد از تخلیه یا تغییر شکل چشم باید روند ساخت پروتز، مراقبت بعدی و راه رزرو مشاوره را "
            "روشن ببیند؛ و از همان اول بداند پروتز بینایی را برنمی‌گرداند."
        ),
        "problem_en": (
            "After eye loss or a changed socket, a visitor needs the fabrication path, later care, "
            "and a way to book a consult — and to hear up front that a prosthesis does not restore sight."
        ),
        "solution": (
            "سایت آراز دید نورا را به فارسی، انگلیسی و عربی چیدم. خانه ساخت سفارشی را با سه محور دقت، "
            "هنر و مراقبت توضیح می‌دهد؛ صفحه خدمات، پروتز چشم و پولیش و ترمیم را جدا می‌کند. "
            "سرپرست علمی، دکتر وحید عبدالرحیمی، در بخش خودش معرفی شده است. رزرو مشاوره، آدرس مرکز "
            "در گاندی جنوبی، تلفن‌ها، تصاویر و مجله (تطبیق رنگ عنبیه، نگهداری روزانه، نخستین ویزیت) "
            "از همان صفحه در دسترس است."
        ),
        "solution_en": (
            "I built Araz Did Noura in Persian, English, and Arabic. The homepage explains custom "
            "fabrication through precision, craft, and care; services split ocular prosthesis from "
            "polish and repair. Scientific lead Dr. Vahid Abdolrahimi has his own section. Consult "
            "booking, the Gandhi South address, phone numbers, photos, and the journal (iris matching, "
            "daily care, the first visit) are reachable from the same page."
        ),
        "outcome": "arazdid.com زنده است؛ معرفی ساخت پروتز، رزرو مشاوره و مجله مراقبت بدون وعده بازگشت بینایی در دسترس است.",
        "outcome_en": "arazdid.com is live; prosthesis fabrication, consult booking, and the care journal are available, without promising restored sight.",
        "live_url": "https://arazdid.com/fa/",
        "cover_file": "sites/arazdid-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 7,
        "skills": ["Django"],
    },
    {
        "title": "راهکار ۱۸۰",
        "title_en": "Rahkar 180",
        "summary": "تبدیل ایده خام به بیزینس‌پلن کوتاه بر پایه بوم ناب، با نقطه سربه‌سر از اعداد خود کاربر و ملاحظات اجرای ایران.",
        "summary_en": "Turns a raw idea into a short Lean Canvas business plan, with break-even from the user’s own numbers and Iran execution notes.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "problem": (
            "ایده خام در گفتگوی پراکنده گم می‌شود. قالب جهانی بوم ناب هم پرداخت، ارز، مجوز و محدودیت‌های "
            "اجرا در ایران را ندارد، و خروجی باید سندی باشد که بشود نشان داد نه یک جواب چت."
        ),
        "problem_en": (
            "A raw idea disappears in a scattered chat. A global Lean Canvas also skips payment, "
            "currency, licenses, and other constraints of doing business in Iran, and the result "
            "has to be a document someone can show, not a chat reply."
        ),
        "solution": (
            "فرم را روی بلوک‌های بوم ناب چیدم: مسئله، مشتری، ارزش پیشنهادی، کانال، درآمد، هزینه و رقبا، "
            "به‌علاوه پرداخت، ارز و مجوز. سند رایگان بدون هوش مصنوعی از همان پاسخ‌ها ساخته می‌شود: "
            "خلاصه یک‌صفحه‌ای، بیزینس‌پلن کوتاه قابل چاپ و نقطه سربه‌سر از اعداد خود کاربر. "
            "راهنما و وبلاگ تعریف بیزینس‌پلن، بوم ناب، اعتبارسنجی، تفاوت با طرح توجیهی و MVP را جدا می‌کنند. "
            "لایه پولی تحلیل ریسک و نقشه ۳۰ تا ۹۰ روزه هنوز به درگاه وصل نیست و قیمتش اعلام نشده است."
        ),
        "solution_en": (
            "I structured the form on Lean Canvas blocks: problem, customer, value proposition, "
            "channel, revenue, cost, and competition, plus payment, currency, and licensing. "
            "The free document is built from those answers without AI: a one-page summary, a short "
            "printable plan, and break-even from the user’s own figures. The guide and blog define "
            "the business plan, Lean Canvas, validation, how this differs from a bank feasibility study, "
            "and what an MVP is. The paid risk analysis and 30–90 day roadmap are not connected to "
            "a payment gateway yet, and the price is not published."
        ),
        "outcome": (
            "rahkar180.ir منتشر است و سند رایگان ایده از همین حالا ساخته می‌شود؛ "
            "بخش تحلیل پولی بعد از وصل شدن پرداخت به همان سند اضافه می‌شود."
        ),
        "outcome_en": (
            "rahkar180.ir is published and the free idea document can be generated now; "
            "the paid analysis is added to the same document once checkout is connected."
        ),
        "live_url": "https://rahkar180.ir/",
        "cover_file": "sites/rahkar180-cover.webp",
        "is_featured": True,
        "is_private": False,
        "order": 8,
        "skills": ["Django"],
    },
    {
        "title": "سامانه پایش و تحلیل پرواز",
        "title_en": "Flight monitoring and analysis platform",
        "summary": "جمع‌آوری اطلاعات مشخص پرواز از وب‌اسکرپینگ و API رسمی، تحلیل روند، و داشبورد آنلاین برای کارفرما. شرح دقیق محرمانه است.",
        "summary_en": "Specified flight data collected by scraping and an official API, then trend analysis and an online dashboard. Precise details stay confidential.",
        "category": Project.Category.SCRAPE,
        "categories": "scrape,data,web,automation,service,confidential",
        "status": Project.Status.COMPLETED,
        "problem": "اطلاعات پرواز در چند منبع پراکنده بود و کارفرما برای هر پرواز یک تصویر واحد، قابل‌اعتماد و آنلاین می‌خواست.",
        "problem_en": "Flight facts were scattered across sources, and the client needed one trustworthy online view of each flight.",
        "solution": "جمع‌آوری را در دو فاز اسکرپ و API رسمی چیدم، داده‌ها را همسان و اعتبارسنجی کردم، و نتیجه را به روند، هشدار و داشبورد آنلاین رساندم.",
        "solution_en": "I set collection up in two phases, scraping then an official API, harmonized and checked the data, and carried it through to trends, alerts, and an online dashboard.",
        "outcome": "داشبورد آنلاین با سابقه داده، آلارم پیامکی و شبکه‌های اجتماعی، و پیش‌بینی روند با رگرسیون. جزئیات دقیق محرمانه است.",
        "outcome_en": "An online dashboard with data history, SMS and social alerts, and a regression forecast. The precise account stays confidential.",
        "writeup": (
            "# محرمانگی\n"
            "شرح دقیق این پروژه محرمانه است. نام کارفرما، منبع‌ها و جزئیات عملیاتی اینجا نیست. "
            "متن زیر فقط چارچوب کار است؛ همان‌قدر که با موافقت کارفرما می‌شود گفت.\n\n"
            "# کار من در تیم\n"
            "پروژه را پنج نفر ساختیم. جمع‌آوری، همسان‌سازی و اعتبارسنجی داده، زمان‌بندی برداشت، "
            "تحلیل روند و پیش‌بینی، لایه‌های پایگاه‌داده، و زیرساخت وب‌اسکرپینگ را من انجام دادم. "
            "بخش‌های دیگر محصول را چهار نفر دیگر تیم توسعه دادند.\n\n"
            "# مسئله\n"
            "کارفرما اطلاعات مشخصی از پروازها می‌خواست که در چند منبع پخش بود. باید برای هر پرواز "
            "آن داده‌ها جمع می‌شد، محتواهای مختلف هر پرواز کنار هم خوانده می‌شد، و نتیجه در یک "
            "داشبورد آنلاین به کارفرما می‌رسید.\n\n"
            "# جمع‌آوری\n"
            "برداشت دو فاز داشت. فاز اول وب‌اسکرپینگ بود و فاز دوم API رسمی. خروجی این دو مسیر "
            "همسان شد، اعتبار داده سنجیده شد، و رکوردهای معیوب اسکرپ پیش از استفاده اصلاح شدند.\n\n"
            "بازه جمع‌آوری را کاربر انتخاب می‌کرد: نزدیک به لحظه، یا در یک فاصله زمانی مشخص.\n\n"
            "# تحلیل و داشبورد\n"
            "روندهایی که برای کارفرما مهم بود شناسایی شد. آلارم همان موضوع‌ها با پیامک و در "
            "شبکه‌های اجتماعی به او رسید. داشبورد آنلاین نتیجه برداشت و تحلیل را یک‌جا نشان می‌داد. "
            "روند آینده هم با رگرسیون برآورد می‌شد.\n\n"
            "# پایگاه داده\n"
            "سه پایگاه کنار هم کار می‌کرد. پایگاه کش برای خواندن سریع بود. پایگاه جدا سابقه را "
            "نگه می‌داشت تا تحلیل روی تاریخچه انجام شود. پایگاه عمیق و چانک‌بندی‌شده حجم داده‌های "
            "خیلی قدیمی را می‌گرفت؛ داده‌ای که قرار است طی چند سال جمع شود و نباید پایگاه روز را سنگین کند.\n\n"
            "قبل از ذخیره، رکورد تکراری، کثیف و تهی کنار گذاشته می‌شد.\n\n"
            "# وب‌اسکرپینگ\n"
            "منابع محدودیت نمایش، نرخ درخواست و حساسیت آی‌پی داشتند. برای نوع‌های مختلف داده از "
            "Selenium، BeautifulSoup و Camoufox استفاده شد. داده‌ای که سایت اشتباه برمی‌گرداند جدا "
            "مدیریت می‌شد. پاپ‌آپ، محدودیت نرخ و حساسیت آی‌پی هم در همین لایه کنترل می‌شد. اسکرپر "
            "روی لینوکس، ویندوز و موبایل اجرا می‌شد. کل سامانه داخل Docker بود.\n\n"
            "# نتیجه\n"
            "کارفرما به داشبورد آنلاین پرواز رسید: داده از اسکرپ و API رسمی، سابقه قابل تحلیل، "
            "هشدار، و برآورد روند. شرح دقیق‌تر محرمانه می‌ماند."
        ),
        "writeup_en": (
            "# Confidentiality\n"
            "The precise account of this project is confidential. The client’s name, the sources, "
            "and the operational detail are not here. What follows is the frame of the work, "
            "and only as much as the client agreed to share.\n\n"
            "# My part of the team\n"
            "Five people built the product. I did collection, harmonizing and validating the data, "
            "the collection schedule, trend analysis and forecasting, the database layers, and the "
            "scraping stack. The other four people on the team built the rest.\n\n"
            "# The problem\n"
            "The client needed specific facts about flights that lived in several sources. For each "
            "flight those facts had to be gathered, the different readings of that flight had to be "
            "read together, and the result had to reach the client on an online dashboard.\n\n"
            "# Collection\n"
            "Collection had two phases. The first was web scraping and the second was an official API. "
            "The two streams were harmonized, the data was validated, and faulty scrape records were "
            "corrected before anyone relied on them.\n\n"
            "The user chose the cadence: close to the moment, or on a set interval.\n\n"
            "# Analysis and the dashboard\n"
            "The trends the client cared about were identified. Alerts for those topics went out by "
            "SMS and on social networks. The online dashboard showed the collected and analyzed result "
            "in one place. The future trend was estimated with regression.\n\n"
            "# Databases\n"
            "Three databases worked side by side. A cache database served fast reads. A separate "
            "database kept history so analysis could run on the past. A deep, chunked database held "
            "the very old volume — data that will accumulate over years and should not weigh down "
            "the database used day to day.\n\n"
            "Duplicate, dirty, and null records were caught before they were stored.\n\n"
            "# Web scraping\n"
            "The sources limited what a page would show, how often it could be asked, and how they "
            "treated an IP. Different kinds of data were collected with Selenium, BeautifulSoup, and "
            "Camoufox. Records a site returned wrong were handled on their own. Pop-ups, rate limits, "
            "and IP sensitivity were controlled in the same layer. The scraper ran on Linux, Windows, "
            "and mobile. The whole system was packaged with Docker.\n\n"
            "# Outcome\n"
            "The client received an online flight dashboard: data from scraping and an official API, "
            "a history that can be analyzed, alerts, and a trend estimate. Anything more precise "
            "stays confidential."
        ),
        "cover_file": "sites/flight-monitor-explorer.webp",
        "gallery": [
            {
                "file": "sites/flight-monitor-explorer.webp",
                "caption": "پایش پروازها روی داشبورد آنلاین",
                "caption_en": "Flight monitoring on the online dashboard",
            },
            {
                "file": "sites/flight-monitor-analytics.webp",
                "caption": "تحلیل قیمت مسیرها در همان سامانه",
                "caption_en": "Route price analysis in the same system",
            },
        ],
        "is_featured": True,
        "is_private": True,
        "order": 2,
        "skills": ["Python", "BeautifulSoup", "Camoufox", "Docker", "تحلیل داده"],
    },
]

CERTIFICATES = [
    {
        "title": "آموزش Docker برای برنامه‌نویس‌ها و مهندسین DevOps",
        "title_en": "Docker for Developers and DevOps Engineers",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "آموزش جنگو Django",
        "title_en": "Django course",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "آموزش اصول پایگاه داده و SQL Server",
        "title_en": "Database fundamentals and SQL Server",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "آموزش درک برنامه‌نویسی",
        "title_en": "Understanding programming",
        "issuer": "مکتب‌خونه", "issuer_en": "Maktabkhooneh",
        "instructor": "جادی میرمیرانی", "instructor_en": "Jadi Mirmirani",
        "year": "۱۴۰۲", "year_en": "2023", "hours": 17, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "آموزش پایتون مقدماتی",
        "title_en": "Introductory Python",
        "issuer": "مکتب‌خونه", "issuer_en": "Maktabkhooneh",
        "instructor": "جادی میرمیرانی", "instructor_en": "Jadi Mirmirani",
        "year": "۱۴۰۲", "year_en": "2023", "hours": 57, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "مقدمه‌ای بر الگوریتم و برنامه‌نویسی",
        "title_en": "Introduction to algorithms and programming",
        "issuer": "مجتمع فنی تهران", "issuer_en": "Tehran Institute of Technology",
        "instructor": "", "instructor_en": "",
        "year": "۱۴۰۱", "year_en": "2022", "hours": 38, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "آموزش درک مقدماتی شبکه",
        "title_en": "Introductory networking",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.BACKEND,
    },
    {
        "title": "ساخت اپلیکیشن‌های LLM",
        "title_en": "Building LLM applications",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.AI_DATA,
    },
    {
        "title": "دوره‌ی یک‌ساله‌ی طراحی و نمونه‌سازی محصولات هوش مصنوعی و اینترنت اشیا (AIoT)",
        "title_en": "One-year AIoT product design and prototyping course",
        "issuer": "مرکز تحقیقاتی چیتا، دانشگاه تهران",
        "issuer_en": "Cheetah Research Center, University of Tehran",
        "instructor": "", "instructor_en": "",
        "year": "۱۴۰۲", "year_en": "2023", "hours": None, "category": Certificate.Category.AI_DATA,
    },
    {
        "title": "طراحی داشبوردهای هوش تجاری با Power BI",
        "title_en": "Business intelligence dashboards with Power BI",
        "issuer": "مجتمع فنی تهران", "issuer_en": "Tehran Institute of Technology",
        "instructor": "", "instructor_en": "",
        "year": "۱۴۰۲", "year_en": "2023", "hours": 24, "category": Certificate.Category.AI_DATA,
    },
    {
        "title": "آموزش اتوماسیون با n8n",
        "title_en": "Automation with n8n",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.AI_DATA,
    },
    {
        "title": "آموزش اکسل کاربردی",
        "title_en": "Practical Excel",
        "issuer": "مکتب‌خونه", "issuer_en": "Maktabkhooneh",
        "instructor": "سجاد شکوهیار", "instructor_en": "Sajjad Shokuhyar",
        "year": "۱۴۰۱", "year_en": "2022", "hours": 20, "category": Certificate.Category.AI_DATA,
    },
    {
        "title": "ICDL Level 2",
        "title_en": "ICDL Level 2",
        "issuer": "مجتمع فنی تهران", "issuer_en": "Tehran Institute of Technology",
        "instructor": "", "instructor_en": "",
        "year": "۱۴۰۱", "year_en": "2022", "hours": 63, "category": Certificate.Category.OTHER,
    },
    {
        "title": "آموزش عملی کار با آردوینو (برنامه‌نویسی میکروکنترلرها)",
        "title_en": "Hands-on Arduino (microcontroller programming)",
        "issuer": "", "issuer_en": "", "instructor": "", "instructor_en": "",
        "year": "", "year_en": "", "hours": None, "category": Certificate.Category.OTHER,
    },
]

SOCIAL_LINKS = [
    ("GitHub", "https://github.com/Meska75", "fab fa-github", 1),
    ("LinkedIn", "https://www.linkedin.com/", "fab fa-linkedin", 2),
    ("Email", "mailto:mohammad.eska34@gmail.com", "fas fa-envelope", 3),
]


class Command(BaseCommand):
    help = "Seed the database with the real portfolio content (idempotent)."

    @transaction.atomic
    def handle(self, *args, **options):
        Profile.objects.update_or_create(
            full_name="محمد اسکندرلو",
            defaults={
                "full_name_en": "Mohammad Eskandarloo",
                "headline": "مهندس بک‌اند پایتون/جنگو و هوش مصنوعی",
                "headline_en": "Python/Django backend engineer & AI builder",
                "tagline": "وب‌سایت و بک‌اند با Django می‌سازم، داده را به تصمیم تبدیل می‌کنم و هوش مصنوعی را وارد کار روزمره‌ی کسب‌وکار می‌کنم.",
                "tagline_en": "I build websites and backends with Django, turn data into decisions, and bring AI into everyday business work.",
                "about": ABOUT,
                "about_en": ABOUT_EN,
                "location": "تهران",
                "location_en": "Tehran",
                "email": "mohammad.eska34@gmail.com",
                "phone": "09198298159",
                "show_phone": False,
                "available_for_work": True,
            },
        )

        for label, url, icon, order in SOCIAL_LINKS:
            SocialLink.objects.update_or_create(
                label=label, defaults={"url": url, "icon": icon, "order": order})

        skill_by_name = {}
        keep_category_names = {item[0] for item in SKILLS}
        keep_skill_names = set()
        for cat_name, cat_en, icon, order, skills in SKILLS:
            category, _ = SkillCategory.objects.update_or_create(
                name=cat_name, defaults={"name_en": cat_en, "icon": icon, "order": order})
            for s_order, (s_name, s_en, level, featured) in enumerate(skills, start=1):
                keep_skill_names.add(s_name)
                skill, _ = Skill.objects.update_or_create(
                    name=s_name,
                    defaults={
                        "category": category,
                        "name_en": s_en,
                        "level": level,
                        "featured": featured,
                        "order": s_order,
                    },
                )
                skill_by_name[s_name] = skill
        Skill.objects.exclude(name__in=keep_skill_names).delete()
        SkillCategory.objects.exclude(name__in=keep_category_names).delete()

        for exp in EXPERIENCES:
            Experience.objects.update_or_create(
                role=exp["role"], organization=exp["organization"],
                defaults={k: v for k, v in exp.items() if k not in ("role", "organization")})

        for p in PROJECTS:
            data = dict(p)
            skills = data.pop("skills", [])
            cover_file = data.pop("cover_file", None)
            gallery = data.pop("gallery", [])
            project, _ = Project.objects.update_or_create(
                title=data["title"],
                defaults={k: v for k, v in data.items() if k != "title"})
            resolved = [skill_by_name[name] for name in skills if name in skill_by_name]
            project.skills.set(resolved)
            self._attach_cover(project, cover_file)
            self._attach_gallery(project, gallery)
        Project.objects.exclude(title__in={p["title"] for p in PROJECTS}).delete()

        for order, cert in enumerate(CERTIFICATES, start=1):
            Certificate.objects.update_or_create(
                title=cert["title"],
                defaults={**{k: v for k, v in cert.items() if k != "title"}, "order": order})

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {Profile.objects.count()} profile, {Skill.objects.count()} skills, "
            f"{Experience.objects.count()} experiences, {Project.objects.count()} projects, "
            f"{Certificate.objects.count()} certificates, {SocialLink.objects.count()} social links."
        ))

    def _attach_cover(self, project, filename):
        if not filename:
            return
        src = COVER_ROOT / filename
        if not src.exists():
            src = N8N_COVER_DIR / Path(filename).name
        if not src.exists():
            self.stdout.write(self.style.WARNING(f"Cover missing: {src}"))
            return
        stored_name = Path(filename).name
        current = Path(project.cover_image.name).name if project.cover_image else ""
        if current == stored_name and project.cover_image.storage.exists(project.cover_image.name):
            return
        with src.open("rb") as fh:
            project.cover_image.save(stored_name, File(fh), save=True)

    def _attach_gallery(self, project, items):
        if not items:
            return
        keep = []
        for order, item in enumerate(items):
            image, _ = ProjectImage.objects.update_or_create(
                project=project,
                order=order,
                defaults={
                    "caption": item.get("caption", ""),
                    "caption_en": item.get("caption_en", ""),
                },
            )
            filename = item["file"]
            src = COVER_ROOT / filename
            if not src.exists():
                self.stdout.write(self.style.WARNING(f"Gallery image missing: {src}"))
                keep.append(image.pk)
                continue
            stored_name = Path(filename).name
            current = Path(image.image.name).name if image.image else ""
            has_file = bool(image.image) and image.image.storage.exists(image.image.name)
            if current != stored_name or not has_file:
                with src.open("rb") as fh:
                    image.image.save(stored_name, File(fh), save=True)
            keep.append(image.pk)
        project.images.exclude(pk__in=keep).delete()
