import pandas as pd
import re


# ==========================================================
# ROADMAPX AI
# PERSONALIZED MULTI-PATH CAREER ROADMAP RECOMMENDATION
# ==========================================================


# ==========================================================
# 1. CAREER KNOWLEDGE BASE
# ==========================================================

CAREER_PROFILES = {

    "ML Engineer": {
        "specializations": [
            "computer science",
            "engineering",
            "science"
        ],

        "education": [
            "bachelor's",
            "master's",
            "phd"
        ],

        "skills": [
            "python",
            "machine learning",
            "data analysis",
            "sql"
        ],

        "certifications": [
            "aws certified",
            "google data analytics"
        ],

        "roadmap": [
            "Python Programming",
            "NumPy and Pandas",
            "Statistics",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow / PyTorch",
            "Model Deployment",
            "MLOps",
            "Build ML Projects"
        ]
    },


    "Software Engineer": {
        "specializations": [
            "computer science",
            "engineering"
        ],

        "education": [
            "bachelor's",
            "master's",
            "phd"
        ],

        "skills": [
            "python",
            "sql"
        ],

        "certifications": [
            "aws certified"
        ],

        "roadmap": [
            "Programming Fundamentals",
            "Java / Python",
            "Data Structures and Algorithms",
            "Object Oriented Programming",
            "SQL and Databases",
            "Git and GitHub",
            "REST APIs",
            "Backend Development",
            "Build Full Stack Projects"
        ]
    },


    "Data Scientist": {
        "specializations": [
            "computer science",
            "engineering",
            "science",
            "business"
        ],

        "education": [
            "bachelor's",
            "master's",
            "phd"
        ],

        "skills": [
            "python",
            "data analysis",
            "machine learning",
            "sql"
        ],

        "certifications": [
            "google data analytics"
        ],

        "roadmap": [
            "Python",
            "Statistics",
            "Probability",
            "Pandas and NumPy",
            "Data Visualization",
            "Machine Learning",
            "Feature Engineering",
            "Model Evaluation",
            "Advanced ML Projects"
        ]
    },


    "Data Analyst": {
        "specializations": [
            "computer science",
            "engineering",
            "business",
            "commerce",
            "finance",
            "science"
        ],

        "education": [
            "bachelor's",
            "master's"
        ],

        "skills": [
            "data analysis",
            "sql",
            "ms office",
            "python"
        ],

        "certifications": [
            "google data analytics"
        ],

        "roadmap": [
            "Excel",
            "SQL",
            "Data Cleaning",
            "Python",
            "Pandas",
            "Statistics",
            "Power BI",
            "Data Visualization",
            "Dashboard Projects"
        ]
    },


    "Business Analyst": {
        "specializations": [
            "business",
            "commerce",
            "finance",
            "computer science",
            "engineering"
        ],

        "education": [
            "bachelor's",
            "master's"
        ],

        "skills": [
            "data analysis",
            "communication",
            "ms office",
            "sql"
        ],

        "certifications": [
            "google data analytics"
        ],

        "roadmap": [
            "Business Fundamentals",
            "Excel",
            "SQL",
            "Data Analysis",
            "Business Communication",
            "Requirements Gathering",
            "Power BI",
            "Business Intelligence",
            "Case Study Projects"
        ]
    },


    "Financial Analyst": {
        "specializations": [
            "finance",
            "commerce",
            "business"
        ],

        "education": [
            "bachelor's",
            "master's"
        ],

        "skills": [
            "financial analysis",
            "accounting",
            "data analysis",
            "ms office"
        ],

        "certifications": [
            "cfa level 1",
            "tally erp"
        ],

        "roadmap": [
            "Accounting Fundamentals",
            "Excel",
            "Financial Statements",
            "Financial Analysis",
            "Financial Modeling",
            "Investment Analysis",
            "Power BI",
            "CFA Preparation",
            "Financial Analysis Projects"
        ]
    },


    "Junior Accountant": {
        "specializations": [
            "finance",
            "commerce",
            "business"
        ],

        "education": [
            "intermediate",
            "bachelor's",
            "master's"
        ],

        "skills": [
            "accounting",
            "ms office",
            "data analysis"
        ],

        "certifications": [
            "tally erp",
            "cfa level 1"
        ],

        "roadmap": [
            "Accounting Basics",
            "Journal Entries",
            "Ledger and Trial Balance",
            "Excel",
            "Tally ERP",
            "Financial Statements",
            "GST Basics",
            "Accounting Projects"
        ]
    },


    "Marketing Executive": {
        "specializations": [
            "business",
            "commerce",
            "arts"
        ],

        "education": [
            "intermediate",
            "bachelor's",
            "master's"
        ],

        "skills": [
            "marketing",
            "communication",
            "ms office"
        ],

        "certifications": [
            "digital marketing",
            "creative writing"
        ],

        "roadmap": [
            "Marketing Fundamentals",
            "Communication Skills",
            "Digital Marketing",
            "SEO",
            "Social Media Marketing",
            "Content Marketing",
            "Google Analytics",
            "Advertising",
            "Marketing Campaign Project"
        ]
    },


    "Sales Assistant": {
        "specializations": [
            "business",
            "commerce",
            "arts"
        ],

        "education": [
            "intermediate",
            "bachelor's"
        ],

        "skills": [
            "communication",
            "marketing",
            "ms office"
        ],

        "certifications": [
            "digital marketing"
        ],

        "roadmap": [
            "Communication Skills",
            "Sales Fundamentals",
            "Customer Relationship Management",
            "MS Office",
            "Negotiation",
            "Digital Marketing",
            "CRM Tools",
            "Sales Analytics",
            "Sales Project"
        ]
    },


    "School Counselor": {
        "specializations": [
            "psychology",
            "arts",
            "science"
        ],

        "education": [
            "bachelor's",
            "master's",
            "phd"
        ],

        "skills": [
            "counseling",
            "communication"
        ],

        "certifications": [
            "mental health basics"
        ],

        "roadmap": [
            "Psychology Fundamentals",
            "Counseling Skills",
            "Communication",
            "Child Psychology",
            "Mental Health Basics",
            "Counseling Techniques",
            "Ethics",
            "Practical Counseling",
            "Counseling Internship"
        ]
    },


    "Professor": {
        "specializations": [
            "computer science",
            "engineering",
            "science",
            "finance",
            "commerce",
            "business",
            "psychology",
            "arts"
        ],

        "education": [
            "master's",
            "phd"
        ],

        "skills": [
            "communication",
            "data analysis"
        ],

        "certifications": [
            "creative writing"
        ],

        "roadmap": [
            "Subject Specialization",
            "Advanced Degree",
            "Research Methodology",
            "Academic Writing",
            "Teaching Skills",
            "Presentation Skills",
            "Research Publications",
            "NET / Eligibility Preparation",
            "Teaching Experience"
        ]
    },


    "Research Scientist": {
        "specializations": [
            "science",
            "engineering",
            "computer science"
        ],

        "education": [
            "master's",
            "phd"
        ],

        "skills": [
            "python",
            "data analysis",
            "machine learning"
        ],

        "certifications": [
            "aws certified",
            "google data analytics"
        ],

        "roadmap": [
            "Research Fundamentals",
            "Statistics",
            "Python",
            "Literature Review",
            "Research Methodology",
            "Machine Learning",
            "Experiment Design",
            "Academic Writing",
            "Research Publication"
        ]
    },


    "Clerk": {
        "specializations": [
            "commerce",
            "business",
            "arts",
            "finance"
        ],

        "education": [
            "intermediate",
            "bachelor's"
        ],

        "skills": [
            "ms office",
            "accounting",
            "communication"
        ],

        "certifications": [
            "tally erp"
        ],

        "roadmap": [
            "MS Office",
            "Excel",
            "Typing Skills",
            "Office Administration",
            "Basic Accounting",
            "Tally ERP",
            "Communication",
            "Documentation",
            "Office Management"
        ]
    },


    "Data Entry Operator": {
        "specializations": [
            "commerce",
            "business",
            "arts"
        ],

        "education": [
            "intermediate",
            "bachelor's"
        ],

        "skills": [
            "ms office",
            "communication",
            "data analysis"
        ],

        "certifications": [
            "google data analytics"
        ],

        "roadmap": [
            "Typing Skills",
            "MS Word",
            "MS Excel",
            "Data Entry",
            "Data Validation",
            "Documentation",
            "Spreadsheet Management",
            "Basic Data Analysis",
            "Office Tools"
        ]
    }
}


# ==========================================================
# 2. NORMALIZE TEXT
# ==========================================================

def normalize(text):

    if pd.isna(text):
        return ""

    text = str(text).lower().strip()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# ==========================================================
# 3. CONVERT USER SKILLS
# ==========================================================

def extract_items(text):

    if not text:
        return []

    items = []

    for item in text.split(","):

        item = normalize(item)

        if item:
            items.append(item)

    return list(set(items))


# ==========================================================
# 4. SKILL MATCH SCORE
# ==========================================================

def calculate_skill_score(
    user_skills,
    required_skills
):

    if not required_skills:
        return 0

    matched = 0

    for skill in required_skills:

        if skill in user_skills:
            matched += 1

    return (
        matched / len(required_skills)
    ) * 100


# ==========================================================
# 5. CERTIFICATION SCORE
# ==========================================================

def calculate_certification_score(
    user_certifications,
    required_certifications
):

    if not required_certifications:
        return 0

    matched = 0

    for cert in required_certifications:

        if cert in user_certifications:
            matched += 1

    return (
        matched / len(required_certifications)
    ) * 100


# ==========================================================
# 6. SPECIALIZATION SCORE
# ==========================================================

def calculate_specialization_score(
    specialization,
    career_specializations
):

    specialization = normalize(
        specialization
    )

    if specialization in career_specializations:
        return 100

    return 0


# ==========================================================
# 7. EDUCATION SCORE
# ==========================================================

def calculate_education_score(
    education,
    career_education
):

    education = normalize(
        education
    )

    if education in career_education:
        return 100

    return 40


# ==========================================================
# 8. CGPA SCORE
# ==========================================================

def calculate_cgpa_score(
    cgpa
):

    try:

        cgpa = float(cgpa)

    except:

        return 50

    if cgpa >= 90:
        return 100

    elif cgpa >= 80:
        return 90

    elif cgpa >= 70:
        return 75

    elif cgpa >= 60:
        return 60

    elif cgpa >= 50:
        return 45

    else:
        return 30


# ==========================================================
# 9. CALCULATE CAREER MATCH
# ==========================================================

def calculate_career_match(
    education,
    specialization,
    skills,
    certifications,
    cgpa,
    career
):

    profile = CAREER_PROFILES[career]

    user_skills = extract_items(
        skills
    )

    user_certifications = extract_items(
        certifications
    )

    skill_score = calculate_skill_score(
        user_skills,
        profile["skills"]
    )

    certification_score = calculate_certification_score(
        user_certifications,
        profile["certifications"]
    )

    specialization_score = calculate_specialization_score(
        specialization,
        profile["specializations"]
    )

    education_score = calculate_education_score(
        education,
        profile["education"]
    )

    cgpa_score = calculate_cgpa_score(
        cgpa
    )

    # ======================================
    # WEIGHTED SCORE
    # ======================================

    final_score = (

        skill_score * 0.45

        + specialization_score * 0.20

        + education_score * 0.15

        + certification_score * 0.10

        + cgpa_score * 0.10

    )

    # Missing skills
    missing_skills = []

    for skill in profile["skills"]:

        if skill not in user_skills:

            missing_skills.append(
                skill
            )

    return {
        "career": career,
        "score": round(
            final_score,
            2
        ),
        "skill_score": round(
            skill_score,
            2
        ),
        "specialization_score": round(
            specialization_score,
            2
        ),
        "education_score": round(
            education_score,
            2
        ),
        "certification_score": round(
            certification_score,
            2
        ),
        "cgpa_score": round(
            cgpa_score,
            2
        ),
        "missing_skills": missing_skills,
        "roadmap": profile["roadmap"]
    }


# ==========================================================
# 10. GET TOP CAREERS
# ==========================================================

def recommend_careers(
    education,
    specialization,
    skills,
    certifications,
    cgpa,
    top_n=3
):

    results = []

    for career in CAREER_PROFILES:

        result = calculate_career_match(
            education,
            specialization,
            skills,
            certifications,
            cgpa,
            career
        )

        results.append(
            result
        )

    # Sort by match score
    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_n]


# ==========================================================
# 11. DISPLAY RESULTS
# ==========================================================

def display_results(results):

    print("\n")
    print("=" * 60)
    print("           ROADMAPX AI")
    print(" PERSONALIZED CAREER RECOMMENDATIONS")
    print("=" * 60)

    for index, result in enumerate(
        results,
        start=1
    ):

        print("\n")
        print(
            f"CAREER PATH {index}: "
            f"{result['career']}"
        )

        print(
            f"Match Score: "
            f"{result['score']}%"
        )

        print(
            f"Skill Match: "
            f"{result['skill_score']}%"
        )

        print(
            f"Specialization Match: "
            f"{result['specialization_score']}%"
        )

        print(
            f"Education Match: "
            f"{result['education_score']}%"
        )

        print(
            f"Certification Match: "
            f"{result['certification_score']}%"
        )

        print(
            f"Academic Score: "
            f"{result['cgpa_score']}%"
        )

        print("\nMissing Skills:")

        if result["missing_skills"]:

            for skill in result["missing_skills"]:

                print(
                    "  •",
                    skill
                )

        else:

            print(
                "  No major skill gaps!"
            )

        print("\nSuggested Roadmap:")

        for month, step in enumerate(
            result["roadmap"],
            start=1
        ):

            print(
                f"  Step {month}: {step}"
            )

        print("-" * 60)


# ==========================================================
# 12. MAIN PROGRAM
# ==========================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("                 ROADMAPX AI")
    print("=" * 60)

    print(
        "\nEnter your profile information.\n"
    )

    education = input(
        "Education Level "
        "(Example: Bachelor's): "
    )

    specialization = input(
        "Specialization "
        "(Example: Computer Science): "
    )

    cgpa = input(
        "CGPA / Percentage "
        "(Example: 83): "
    )

    skills = input(
        "Skills "
        "(Example: Python, SQL, Machine Learning): "
    )

    certifications = input(
        "Certifications "
        "(Example: Google Data Analytics): "
    )

    print(
        "\nAnalyzing your profile..."
    )

    results = recommend_careers(
        education,
        specialization,
        skills,
        certifications,
        cgpa,
        top_n=3
    )

    display_results(
        results
    )