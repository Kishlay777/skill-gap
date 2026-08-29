from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "dev-secret-key-change-this-in-production"

# ---------------------------------------------------------------------------
# In-memory "database" — in a real app this would come from a real database.
# Lives here in one place, expressed as plain Python data structures. Lists
# that users can edit at runtime (skills, profile) are mutated in place so
# changes show up immediately without a restart.
# ---------------------------------------------------------------------------

NAV_ITEMS = [
    {"page": "dashboard", "label": "Dashboard", "icon": "home"},
    {"page": "profile", "label": "Profile", "icon": "user"},
    {"page": "skills", "label": "Skills", "icon": "award"},
    {"page": "jobs", "label": "Jobs", "icon": "briefcase"},
    {"page": "training", "label": "Training & Courses", "icon": "cap"},
    {"page": "gap", "label": "Skill Gap Analysis", "icon": "chart"},
    {"page": "reports", "label": "Reports & Insights", "icon": "trend"},
    {"page": "employers", "label": "Employers", "icon": "users"},
    {"page": "admin", "label": "Admin", "icon": "gear"},
]

BOTTOM_NAV_ITEMS = [
    {"page": "support", "label": "Help & Support", "icon": "help"},
]

USER = {"name": "User Name"}

DASHBOARD_KPIS = [
    {"icon": "briefcase", "title": "Job Matches", "num": "12", "pill": "\u2191 20% this month"},
    {"icon": "chart", "title": "Skill Gap Score", "num": "65%", "pill": "\u2191 10% this month"},
    {"icon": "award", "title": "Skills", "num": "8", "pill": "3 Strong \u00b7 5 To Improve"},
    {"icon": "cap", "title": "Courses Completed", "num": "2", "pill": "\u2191 1 this month"},
]

SKILL_GAP_OVERVIEW = [
    {"name": "Python", "level": 45, "gap": 20},
    {"name": "SQL", "level": 70, "gap": 10},
    {"name": "Data Analysis", "level": 50, "gap": 30},
    {"name": "Machine Learning", "level": 30, "gap": 40},
    {"name": "Communication", "level": 80, "gap": 5},
]

TOP_JOBS = [
    {"title": "Data Analyst", "company": "ABC Analytics \u00b7 Delhi, India", "match": "85%",
     "tags": ["Python", "SQL", "Data Analysis"]},
    {"title": "Business Intelligence Developer", "company": "TechCorp \u00b7 Bangalore, India", "match": "78%",
     "tags": ["SQL", "Power BI", "Python"]},
    {"title": "Junior Data Scientist", "company": "Insights Pvt. Ltd. \u00b7 Mumbai, India", "match": "72%",
     "tags": ["Python", "ML", "Statistics"]},
]

ALL_JOBS = TOP_JOBS + [
    {"title": "Software Developer", "company": "Digital Labs \u00b7 Hyderabad, India", "match": "68%",
     "tags": ["Java", "SQL", "Problem Solving"]},
]

RECOMMENDED_COURSES = [
    {"name": "Python for Data Science", "provider": "Coursera \u00b7 Beginner", "percent": 20},
    {"name": "SQL Fundamentals", "provider": "Great Learning \u00b7 Beginner", "percent": 50},
]

TRAINING_COURSES = RECOMMENDED_COURSES + [
    {"name": "Power BI Essentials", "provider": "Microsoft Learn \u00b7 Intermediate", "percent": 10},
]

LEARNING_PATH = [
    {"step": 1, "name": "SQL Fundamentals", "percent": "50%"},
    {"step": 2, "name": "Python for Data Science", "percent": "20%"},
    {"step": 3, "name": "Machine Learning Basics", "percent": "0%"},
]

SKILLS_DISTRIBUTION = [
    {"label": "Strong", "value": 35},
    {"label": "Average", "value": 40},
    {"label": "Needs Improvement", "value": 25},
]

PROFILE = {
    "name": "User Name",
    "role": "Computer Science Student",
    "completion": 80,
    "fields": [
        {"label": "Full Name", "value": "User Name"},
        {"label": "Email", "value": "user@example.com"},
        {"label": "Phone", "value": "+91 XXXXX XXXXX"},
        {"label": "Location", "value": "Lucknow, India"},
        {"label": "Education", "value": "B.Tech Computer Science"},
        {"label": "Experience", "value": "Fresher"},
    ],
}

# Mutable — the Add/Update Skill forms edit this list directly.
MY_SKILLS = [
    {"name": "Python", "category": "Technical", "score": 4},
    {"name": "SQL", "category": "Technical", "score": 4},
    {"name": "Data Analysis", "category": "Technical", "score": 3},
    {"name": "Machine Learning", "category": "Professional", "score": 2},
    {"name": "Communication", "category": "Professional", "score": 4},
    {"name": "Power BI", "category": "Professional", "score": 3},
    {"name": "Java", "category": "Professional", "score": 3},
    {"name": "Problem Solving", "category": "Professional", "score": 4},
]

GAP_STATS = [
    {"label": "Overall Gap", "value": "65%"},
    {"label": "Skills Analyzed", "value": "8"},
    {"label": "Priority Skills", "value": "3"},
]

GAP_TABLE = [
    {"skill": "Machine Learning", "your": "2/5", "required": "4/5", "gap": "40%", "priority": "High"},
    {"skill": "Data Analysis", "your": "3/5", "required": "5/5", "gap": "30%", "priority": "High"},
    {"skill": "Python", "your": "3/5", "required": "4/5", "gap": "20%", "priority": "Medium"},
    {"skill": "SQL", "your": "4/5", "required": "5/5", "gap": "10%", "priority": "Low"},
]

REPORTS_KPIS = [
    {"icon": "trend", "title": "Employment Readiness", "num": "72%", "pill": "\u2191 8% this quarter"},
    {"icon": "chart", "title": "Market Demand", "num": "High", "pill": "Data & AI"},
    {"icon": "briefcase", "title": "Applications", "num": "18", "pill": "4 interviews"},
    {"icon": "award", "title": "Profile Strength", "num": "80%", "pill": "Good"},
]

MARKET_INSIGHTS = [
    "Python demand increased 18%.",
    "SQL remains a top requirement across analytics roles.",
    "AI/ML skills show strong growth.",
]

EMPLOYERS = [
    {"name": "ABC Analytics", "industry": "Analytics", "roles": "12", "skills": "Python, SQL", "status": "Active"},
    {"name": "TechCorp", "industry": "IT Services", "roles": "25", "skills": "Java, Cloud", "status": "Active"},
    {"name": "Insights Pvt. Ltd.", "industry": "AI & Data", "roles": "8", "skills": "ML, Python", "status": "Active"},
    {"name": "Digital Labs", "industry": "Software", "roles": "16", "skills": "React, Java", "status": "Pending"},
]

ADMIN_KPIS = [
    {"icon": "users", "title": "Users", "num": "2,480", "pill": "\u2191 12%"},
    {"icon": "briefcase", "title": "Jobs", "num": "8,420", "pill": "\u2191 9%"},
    {"icon": "award", "title": "Skills", "num": "315", "pill": "Mapped"},
    {"icon": "cap", "title": "Courses", "num": "186", "pill": "Active"},
]

ADMIN_MANAGEMENT = ["User Management", "Skill Taxonomy", "Employer Verification"]
ADMIN_ALERTS = ["12 employer profiles need verification.", "3 skill mappings need review."]

FAQS = [
    {"q": "How is my skill gap calculated?",
     "a": "We compare the skill levels on your profile against the levels most employers ask for in your target roles, and the difference becomes your gap percentage."},
    {"q": "How are jobs matched?",
     "a": "Job matches are ranked by how closely your current skills overlap with each job's required skills \u2014 the higher the overlap, the higher the match score."},
    {"q": "How do I update my skills?",
     "a": "Go to the Skills page, click \u201cAssess\u201d next to any skill to change its score, or \u201c+ Add Skill\u201d to add a new one."},
    {"q": "How do I enroll in a course?",
     "a": "Open Training & Courses and pick any recommended course \u2014 your progress is tracked automatically as you go."},
]


def render_page(page, **context):
    """Render a page template inside the shared shell, with nav highlighting."""
    return render_template(
        f"{page}.html",
        active_page=page,
        nav_items=NAV_ITEMS,
        bottom_nav_items=BOTTOM_NAV_ITEMS,
        user=USER,
        **context,
    )


# ---------------------------------------------------------------------------
# App pages
# ---------------------------------------------------------------------------

@app.route("/")
@app.route("/dashboard")
def dashboard():
    return render_page(
        "dashboard",
        kpis=DASHBOARD_KPIS,
        skill_gap_overview=SKILL_GAP_OVERVIEW,
        top_jobs=TOP_JOBS,
        recommended_courses=RECOMMENDED_COURSES,
        skills_distribution=SKILLS_DISTRIBUTION,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        for f in PROFILE["fields"]:
            new_value = request.form.get(f["label"])
            if new_value is not None and new_value.strip():
                f["value"] = new_value.strip()
        for f in PROFILE["fields"]:
            if f["label"] == "Full Name":
                PROFILE["name"] = f["value"]
        flash("Profile updated.", "success")
        return redirect(url_for("profile"))

    return render_page("profile", profile=PROFILE)


@app.route("/skills")
def skills():
    return render_page("skills", skills=MY_SKILLS)


@app.route("/skills/add", methods=["POST"])
def add_skill():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "Technical").strip()
    try:
        score = int(request.form.get("score", 3))
    except ValueError:
        score = 3
    score = max(1, min(5, score))

    if not name:
        flash("Skill name can't be empty.", "error")
        return redirect(url_for("skills"))

    for s in MY_SKILLS:
        if s["name"].lower() == name.lower():
            flash(f"\u201c{name}\u201d is already on your list \u2014 use Assess to update it.", "error")
            return redirect(url_for("skills"))

    MY_SKILLS.append({"name": name, "category": category, "score": score})
    flash(f"Added \u201c{name}\u201d to your skills.", "success")
    return redirect(url_for("skills"))


@app.route("/skills/update", methods=["POST"])
def update_skill():
    name = request.form.get("name", "").strip()
    try:
        score = int(request.form.get("score", 3))
    except ValueError:
        score = 3
    score = max(1, min(5, score))

    for s in MY_SKILLS:
        if s["name"] == name:
            s["score"] = score
            flash(f"Updated \u201c{name}\u201d to {score}/5.", "success")
            return redirect(url_for("skills"))

    flash("Couldn't find that skill.", "error")
    return redirect(url_for("skills"))


@app.route("/skills/delete", methods=["POST"])
def delete_skill():
    name = request.form.get("name", "").strip()
    before = len(MY_SKILLS)
    MY_SKILLS[:] = [s for s in MY_SKILLS if s["name"] != name]
    if len(MY_SKILLS) < before:
        flash(f"Removed \u201c{name}\u201d.", "success")
    return redirect(url_for("skills"))


@app.route("/jobs")
def jobs():
    return render_page("jobs", jobs=ALL_JOBS)


@app.route("/training")
def training():
    return render_page("training", courses=TRAINING_COURSES, learning_path=LEARNING_PATH)


@app.route("/gap")
def gap():
    return render_page("gap", stats=GAP_STATS, table=GAP_TABLE)


@app.route("/reports")
def reports():
    return render_page("reports", kpis=REPORTS_KPIS, insights=MARKET_INSIGHTS)


@app.route("/employers")
def employers():
    return render_page("employers", employers=EMPLOYERS)


@app.route("/admin")
def admin():
    return render_page(
        "admin", kpis=ADMIN_KPIS, management=ADMIN_MANAGEMENT, alerts=ADMIN_ALERTS
    )


@app.route("/support")
def support():
    return render_page("support", faqs=FAQS)


@app.route("/support/submit", methods=["POST"])
def support_submit():
    subject = request.form.get("subject", "").strip()
    if not subject:
        flash("Please add a subject before submitting.", "error")
    else:
        flash("Your message has been sent \u2014 our team will get back to you soon.", "success")
    return redirect(url_for("support"))


if __name__ == "__main__":
    app.run(debug=True)
