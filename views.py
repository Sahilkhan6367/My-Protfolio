from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .models import ContactMessage

# ─── Portfolio Data (from Sahil's resume) ────────────────────────────────────

PORTFOLIO_DATA = {
    "name": "Sahil Khan",
    "title": "Full Stack Python Developer",
    "tagline": "Building scalable web apps with Django & REST APIs",
    "location": "Nagpur, Maharashtra, India",
    "email": "sk2332076@gmail.com",
    "phone": "+91-9322663997",
    "linkedin": "linkedin.com/in/sahil-khan",
    "github": "https://github.com/Sahilkhan6367",
    "about": (
        "Full Stack Python Developer with hands-on experience building scalable web applications "
        "using Django and REST APIs. Completed internship at ZappKode Solutions with expertise in backend "
        "development, database optimization, and implementing business logic for production systems. "
        "Strong foundation in software development methodologies, data structures, and algorithms. "
        "Currently seeking exciting opportunities to contribute to innovative projects. Passionate about "
        "creating efficient, maintainable solutions and continuous learning."
    ),
    "skills": {
        "Programming Languages": ["Python", "JavaScript", "SQL", "HTML5", "CSS3"],
        "Frameworks & Libraries": ["Django", "Flask", "REST Framework", "Bootstrap"],
        "Databases": ["MySQL", "PostgreSQL", "SQLite"],
        "Tools & Technologies": ["Git", "GitHub", "Postman", "RESTful APIs", "VS Code"],
        "Web Development": ["Responsive Design", "API Integration", "Auth & Authorization", "CRUD Operations"],
        "Core Competencies": ["Data Structures", "Algorithms", "OOP", "Database Design", "Query Optimization"],
    },
    "experience": [
        {
            "role": "Python Developer Intern",
            "company": "ZappKode Solutions",
            "location": "Nagpur, Maharashtra, India",
            "period": "September 2025 – March 2026",
            "points": [
                "Developed and maintained full-stack web applications using Django, implementing RESTful APIs for seamless frontend-backend communication.",
                "Designed and optimized relational database schemas using MySQL and PostgreSQL, improving query performance through efficient indexing and normalization.",
                "Implemented secure authentication and authorization systems including user registration, login, role-based access control, and session management.",
                "Built dynamic dashboards and admin panels with real-time data visualization for monitoring key business metrics.",
                "Collaborated with cross-functional teams to troubleshoot production issues, debug complex code, and deploy updates via Git workflows.",
                "Integrated third-party APIs with robust error handling and data validation for reliable system operations.",
                "Developed responsive frontends using HTML5, CSS3, JavaScript, and Bootstrap with cross-browser and mobile-first design.",
                "Wrote clean, modular, well-documented code following best practices; conducted code reviews and maintained technical documentation.",
            ],
        }
    ],
    "projects": [
        {
            "name": "E-Commerce Web Application",
            "tech": ["Django", "Python", "MySQL", "REST API", "Bootstrap"],
            "year": "2025",
            "icon": "🛒",
            "description": "Full-featured e-commerce platform with user authentication, product catalog, shopping cart, and order management.",
            "points": [
                "Implemented RESTful APIs for product search, filtering, and pagination with optimized SQL queries.",
                "Integrated secure payment gateway for seamless transactions.",
                "Developed responsive UI ensuring great experience across all devices.",
            ],
        },
        {
            "name": "JOBII – Job Portal Web Application",
            "tech": ["Python", "Django", "HTML", "CSS", "JavaScript", "SQLite", "Bootstrap"],
            "year": "2026",
            "icon": "💼",
            "description": "Full-stack job portal enabling companies to post jobs and candidates to apply online with secure authentication, role-based access, and resume management.",
            "points": [
                "Built secure user authentication & login system with role-based access control.",
                "Implemented company registration and job posting module with applicant tracking.",
                "Developed job listing, application system, and resume upload functionality.",
                "Created admin dashboard for managing companies, jobs, and applications.",
                "Designed responsive frontend using HTML, CSS, and JavaScript with Bootstrap.",
                "Utilized Django ORM and SQLite for scalable database management.",
            ],
        },
    ],
    "education": [
        {
            "degree": "Bachelor of Computer Application (BCA)",
            "institution": "Rashtrasant Tukadoji Maharaj Nagpur University (RTMNU)",
            "location": "Nagpur, India",
            "period": "November 2022 – May 2025",
            "coursework": [
                "Data Structures & Algorithms",
                "Database Management Systems",
                "Object-Oriented Programming",
                "Software Engineering",
                "Computer Networks",
                "Operating Systems",
                "Web Technologies",
            ],
        }
    ],
    "certifications": [
        {
            "name": "Full Stack Python Development",
            "desc": "Comprehensive training in Python, Django, REST APIs, databases, and modern web technologies.",
        },
        {
            "name": "Problem Solving",
            "desc": "Active participation in coding challenges focusing on data structures, algorithms, and optimization techniques.",
        },
    ],
}


def index(request):
    return render(request, "index.html", {"data": PORTFOLIO_DATA})


@require_POST
def contact(request):
    try:
        body = json.loads(request.body)
        name    = body.get("name", "").strip()
        email   = body.get("email", "").strip()
        subject = body.get("subject", "").strip()
        message = body.get("message", "").strip()

        if not all([name, email, subject, message]):
            return JsonResponse({"success": False, "error": "All fields are required."}, status=400)

        # Save to database
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        # Send email notification
        email_body = f"""
New contact form submission from your Portfolio website!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 Name    : {name}
📧 Email   : {email}
📌 Subject : {subject}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 Message:
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Reply directly to: {email}
        """

        send_mail(
            subject=f"[Portfolio] New Message: {subject}",
            message=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
            fail_silently=False,
        )

        return JsonResponse({"success": True, "message": "Your message has been sent successfully! I'll get back to you soon."})

    except Exception as e:
        return JsonResponse({"success": False, "error": f"Something went wrong: {str(e)}"}, status=500)