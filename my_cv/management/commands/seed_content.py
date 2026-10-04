"""Seed the database with Mohammad's real portfolio content.

Idempotent: safe to run multiple times (uses update_or_create on natural keys).
Run with:  python manage.py seed_content
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from my_cv.models import (
    Certificate,
    Experience,
    Profile,
    Project,
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

PROJECTS = [
    {
        "title": "دستیار دانش هوشمند (RAG)",
        "title_en": "Intelligent Knowledge Assistant (RAG)",
        "summary": "چت‌بات هوشمند روی کتاب‌های PDF دوزبانه (فارسی/انگلیسی) با خط‌لوله‌ی کامل RAG.",
        "summary_en": "Smart chatbot over bilingual PDF books (Persian/English) with a full RAG pipeline.",
        "category": Project.Category.AI,
        "status": Project.Status.COMPLETED,
        "problem": "پاسخ‌گویی دقیق به پرسش‌ها از روی محتوای تخصصیِ کتاب‌ها، نه دانش عمومی مدل.",
        "problem_en": "Answer questions from specialized book content, not the model's general knowledge.",
        "solution": (
            "یک خط‌لوله‌ی RAG ساختم: استخراج و قطعه‌بندی متن از PDF، تولید embedding با "
            "مدل text-embedding-3-large، ذخیره در پایگاه برداری ChromaDB و بازیابی متنی "
            "برای پاسخ‌گویی با GPT-4o-mini از طریق LangChain."
        ),
        "solution_en": (
            "I built a RAG pipeline: extract and chunk PDF text, embed with "
            "text-embedding-3-large, store in ChromaDB, and retrieve context for answers "
            "with GPT-4o-mini via LangChain."
        ),
        "outcome": "پاسخ‌های متکی بر منبع و دوزبانه، با امکان گسترش به هر مجموعه‌سند دیگری.",
        "outcome_en": "Source-grounded bilingual answers, reusable for any other document set.",
        "github_url": "https://github.com/Meska75/quera-LLM-project-2",
        "is_featured": True,
        "is_private": False,
        "order": 1,
        "skills": ["LangChain", "RAG", "OpenAI API", "ChromaDB", "Python"],
    },
    {
        "title": "سامانه‌ی تجمیع چند-فروشگاهی",
        "title_en": "Multi-store aggregation platform",
        "summary": "دسترسی بلادرنگ کاربران یک فروشگاه به کالای ۱۰ فروشگاه معتبر دیگر.",
        "summary_en": "Realtime access for one shop's users to products from 10 other trusted stores.",
        "category": Project.Category.BACKEND,
        "status": Project.Status.COMPLETED,
        "problem": (
            "یک فروشگاه می‌خواست کاربرانش در لحظه به کالای چندین فروشگاه معتبر دسترسی "
            "داشته باشند."
        ),
        "problem_en": "A shop wanted its users to see products from several trusted stores in realtime.",
        "solution": (
            "دو مسیر تأمین داده طراحی کردم: برای فروشگاه‌های دارای API رسمی (باسلام و "
            "دیجی‌کالا) اتصال مستقیم API، و برای ۸ فروشگاه دیگر وب‌اسکرپینگ منظم. داده‌ها "
            "در PostgreSQL روی هاست Liara ذخیره می‌شدند تا سریع در دسترس کاربران باشند."
        ),
        "solution_en": (
            "I designed two data paths: official APIs where available (Basalam and Digikala), "
            "and scheduled scraping for eight other stores. Data lived in PostgreSQL on Liara "
            "so users could access it quickly."
        ),
        "outcome": "تجمیع ۱۰ منبع فروشگاهی (۲ API رسمی + ۸ اسکرپینگ) با دسترسی بلادرنگ.",
        "outcome_en": "Aggregated 10 store sources (2 official APIs + 8 scrapers) with realtime access.",
        "is_featured": True,
        "is_private": True,
        "order": 2,
        "skills": ["Django", "PostgreSQL", "Camoufox", "یکپارچه‌سازی API", "Liara"],
    },
    {
        "title": "پلتفرم جمع‌آوری داده‌ی تیمی",
        "title_en": "Team data-collection platform",
        "summary": "موتور Core سمت سرور + داشبورد تعریف تسک برای کارمندان یک شرکت.",
        "summary_en": "Server-side Core engine plus a task dashboard for company staff.",
        "category": Project.Category.BACKEND,
        "status": Project.Status.COMPLETED,
        "problem": "نیاز یک شرکت به جمع‌آوری خودکار داده از سامانه‌های مختلف بر اساس تسک‌های تعریف‌شده.",
        "problem_en": "A company needed automated collection from several systems based on defined tasks.",
        "solution": (
            "به‌صورت تیمی یک موتور Core روی سرور و یک داشبورد وب ساختیم که کارمندان از "
            "طریق آن تسک تعریف می‌کردند؛ Core با ترکیب ۱ API رسمی و ۲ منبع وب‌اسکرپینگ "
            "(BeautifulSoup و Camoufox) داده را جمع‌آوری و ذخیره می‌کرد. چون هاست اجازه‌ی "
            "اجرای Camoufox را نمی‌داد، کل سرویس را Dockerize کردم."
        ),
        "solution_en": (
            "As a team we built a Core engine and a web dashboard where staff defined tasks. "
            "Core combined one official API and two scraping sources (BeautifulSoup and Camoufox). "
            "Because the host could not run Camoufox, I dockerized the whole service."
        ),
        "outcome": "خودکارسازی جمع‌آوری داده با معماری Core + داشبورد و استقرار داکرایزشده.",
        "outcome_en": "Automated collection with a Core + dashboard architecture, deployed with Docker.",
        "is_featured": False,
        "is_private": True,
        "order": 3,
        "skills": ["Python", "BeautifulSoup", "Camoufox", "Docker"],
    },
    {
        "title": "نرم‌افزار تحلیل داده‌ی فروش و توصیه‌گر هوشمند",
        "title_en": "Sales analytics & smart recommender",
        "summary": "آنالیز داده‌های فروش با Python و نمایش در داشبورد همراه پیشنهادهای مبتنی بر AI.",
        "summary_en": "Python sales analysis in a dashboard, with AI-based purchase suggestions.",
        "category": Project.Category.DATA,
        "status": Project.Status.COMPLETED,
        "problem": "تبدیل داده‌های خام فروش به بینش قابل‌اقدام و پیشنهادهای خرید برای کاربر.",
        "problem_en": "Turn raw sales data into actionable insight and purchase suggestions.",
        "solution": (
            "داده‌های جمع‌آوری‌شده را با Python تحلیل می‌کردم، نتایج را در داشبورد به "
            "کاربر نشان می‌دادم و همان داده‌ها را برای تولید پیشنهاد به هوش مصنوعی "
            "می‌فرستادم (تحلیل رفتار کاربر برای راهنمایی خرید)."
        ),
        "solution_en": (
            "I analyzed collected data in Python, showed results on a dashboard, and sent the "
            "same data to an AI layer for recommendations based on user behavior."
        ),
        "outcome": "نرم‌افزار تحلیل فروش با لایه‌ی توصیه‌گر هوشمند.",
        "outcome_en": "A sales analytics product with a smart recommendation layer.",
        "is_featured": False,
        "is_private": True,
        "order": 4,
        "skills": ["Python", "تحلیل داده", "سیستم توصیه‌گر"],
    },
    {
        "title": "وب‌سایت مطب دکتر وحید عبدالرحیمی",
        "title_en": "Dr. Vahid Abdolrahimi clinic website",
        "summary": "وب‌سایت کامل و سه‌زبانه‌ی یک پزشک با Django، مستقرشده روی Liara.",
        "summary_en": "A complete trilingual physician site in Django, deployed on Liara.",
        "category": Project.Category.WEB,
        "status": Project.Status.IN_PROGRESS,
        "problem": "نیاز یک پزشک به وب‌سایت حرفه‌ای و چندزبانه برای معرفی خدمات و ارتباط با بیماران.",
        "problem_en": "A physician needed a professional multilingual site for services and patient contact.",
        "solution": (
            "یک سایت کامل با Django شامل سیستم حساب کاربری، بلاگ، گالری، صفحات خدمات و تیم "
            "طراحی و توسعه دادم و آن را روی Liara مستقر کردم. سایت سه‌زبانه است. فاز بعدی، "
            "افزودن یک دستیار هوش مصنوعی برای راهنمایی بیماران، کمک به تعیین وقت و کمک به "
            "ادمین‌ها در تولید محتوای چندزبانه است."
        ),
        "solution_en": (
            "I designed and built a full Django site with accounts, blog, gallery, services, "
            "and team pages, then deployed it on Liara. The site is trilingual. Next is an AI "
            "assistant to guide patients, help with appointments, and support admins with "
            "multilingual content."
        ),
        "outcome": "سایت سه‌زبانه‌ی مستقرشده؛ دستیار هوش مصنوعی در دست توسعه.",
        "outcome_en": "Trilingual site in production; AI assistant still in development.",
        "github_url": "https://github.com/Meska75/drvahidabdolrahimi",
        "live_url": "https://drabdolrahimi.ir",
        "is_featured": True,
        "is_private": False,
        "order": 1,
        "skills": ["Django", "Liara"],
    },
    {
        "title": "راهکار ۱۸۰",
        "title_en": "Rahkar 180",
        "summary": "وب‌سایت منتشرشده.",
        "summary_en": "A published website.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "live_url": "https://rahkar180.ir",
        "is_featured": True,
        "is_private": False,
        "order": 2,
    },
    {
        "title": "آراز دید نورا",
        "title_en": "Araz Did Noura",
        "summary": "وب‌سایت پروتز چشم سفارشی در تهران.",
        "summary_en": "Website for custom ocular prostheses in Tehran.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "live_url": "https://arazdid.com",
        "is_featured": True,
        "is_private": False,
        "order": 3,
    },
    {
        "title": "Pop360",
        "title_en": "Pop360",
        "summary": "وب‌سایت منتشرشده.",
        "summary_en": "A published website.",
        "category": Project.Category.WEB,
        "status": Project.Status.COMPLETED,
        "live_url": "https://pop360.ir",
        "is_featured": True,
        "is_private": False,
        "order": 4,
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
            project, _ = Project.objects.update_or_create(
                title=data["title"],
                defaults={k: v for k, v in data.items() if k != "title"})
            resolved = [skill_by_name[name] for name in skills if name in skill_by_name]
            project.skills.set(resolved)

        for order, cert in enumerate(CERTIFICATES, start=1):
            Certificate.objects.update_or_create(
                title=cert["title"],
                defaults={**{k: v for k, v in cert.items() if k != "title"}, "order": order})

        self.stdout.write(self.style.SUCCESS(
            f"Seeded: {Profile.objects.count()} profile, {Skill.objects.count()} skills, "
            f"{Experience.objects.count()} experiences, {Project.objects.count()} projects, "
            f"{Certificate.objects.count()} certificates, {SocialLink.objects.count()} social links."
        ))
