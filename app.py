import os
import sys
import html
import json
from urllib.parse import quote_plus
from datetime import datetime

import streamlit as st
import pandas as pd
import plotly.graph_objects as go_plotly
import plotly.express as px

# ============================================================
# CAREER ENGINE INTEGRATION (PRESERVED)
# ============================================================
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# pyrefly: ignore [missing-import]
from career_engine import recommend_careers  # noqa: E402

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="RoadmapX AI · Next-Gen AI Career Roadmap Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# SESSION STATE INITIALIZATION (PRESERVED & EXTENDED)
# ============================================================
DEFAULTS = {
    "page": "home",
    "profile": None,
    "recommendations": None,
    "selected_career": None,
    "quiz_topic": "Statistics",
    "quiz_submitted": False,
    "quiz_score": None,
    "quiz_answers": {},
    "active_project_tab": 0,
    "roadmap_duration": "6 months",
}
for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ============================================================
# CONSTANTS & OPTIONS (PRESERVED)
# ============================================================
EDUCATION_OPTIONS = [
    "B.Tech", "B.E", "B.Sc", "BCA", "MCA", "M.Tech", "M.Sc",
    "MBA", "B.Com", "M.Com", "BBA", "12th", "Diploma",
]

SPECIALIZATION_OPTIONS = [
    "Computer Science", "Information Technology", "Artificial Intelligence",
    "Data Science", "Machine Learning", "Electronics", "Electrical Engineering",
    "Mechanical Engineering", "Civil Engineering", "Business Administration",
    "Commerce", "Mathematics", "Statistics", "Physics", "Chemistry", "Other",
]

SKILL_OPTIONS = [
    "Python", "Java", "C", "C++", "JavaScript", "HTML", "CSS", "React",
    "Node.js", "Express.js", "MongoDB", "SQL", "MySQL", "PostgreSQL", "Git",
    "GitHub", "Data Structures", "Algorithms", "Machine Learning",
    "Deep Learning", "Artificial Intelligence", "Data Analysis", "Statistics",
    "Excel", "Power BI", "Tableau", "TensorFlow", "Scikit-learn",
    "Communication", "Problem Solving", "Leadership", "Teamwork", "Marketing",
    "Sales", "Financial Analysis", "Accounting", "Research", "Teaching",
]

CERTIFICATION_OPTIONS = [
    "NPTEL", "AWS", "Microsoft Azure", "Google Cloud", "Google Data Analytics",
    "IBM", "Cisco", "Java Certification", "Python Certification",
    "SQL Certification", "Machine Learning Certification",
    "Power BI Certification", "Excel Certification",
]

SIDE_NAV = [
    ("dashboard", "🏠", "Dashboard"),
    ("home", "👤", "My Profile"),
    ("recommendations", "🎯", "Career Recommendations"),
    ("multipath", "🌿", "Multi-Path Tree"),
    ("gaps", "🧩", "Skill Gap Analysis"),
    ("roadmap", "🗺️", "My Roadmap"),
    ("assessments", "📝", "Assessments"),
    ("projects", "💼", "Portfolio Projects"),
    ("resume", "📄", "Resume Builder"),
    ("progress", "📊", "Progress & Analytics"),
    ("resources", "📚", "Learning Resources"),
    ("settings", "⚙️", "Settings"),
]

# ============================================================
# RICH STUDY CURRICULUM (PRESERVED & EXPANDED)
# ============================================================
MONTH_PLANS = {
    "Programming Fundamentals": {
        "learn": ["Variables, data types and memory management", "Control structures and algorithmic loops",
                  "Modular functions, scope and recursion", "Basic problem solving patterns"],
        "practice": ["Solve 5 algorithmic questions every week on LeetCode", "Build clean CLI scripts without referencing notes"],
        "project": "Build an interactive CLI student management or finance tracker system.",
    },
    "Java / Python": {
        "learn": ["Syntax standards and core library ecosystem", "Object-oriented architecture (Polymorphism, Inheritance)",
                  "Collections, iterators, and lambdas", "Robust exception handling and file I/O operations"],
        "practice": ["Implement design patterns (Factory, Singleton)", "Complete 20 OOP interview challenges"],
        "project": "Build an asynchronous multi-threaded web scraper or log parser.",
    },
    "Data Structures and Algorithms": {
        "learn": ["Arrays, dynamic strings and hash tables", "Linked lists, stacks, queues and heaps",
                  "Trees, binary search trees and graphs", "Time and space complexity (Big-O analysis)"],
        "practice": ["Solve 2-3 LeetCode Medium problems daily", "Implement standard algorithms from scratch"],
        "project": "Develop a custom graph-based pathfinding visualizer.",
    },
    "SQL": {
        "learn": ["Relational schemas and primary/foreign keys", "Complex SELECT, filtering, and aggregated GROUP BY",
                  "Multi-table INNER, LEFT, FULL JOINs", "Window functions (RANK, ROW_NUMBER, LAG/LEAD) and CTEs"],
        "practice": ["Write daily queries against realistic synthetic datasets", "Optimize slow query plans with EXPLAIN ANALYZE"],
        "project": "Design a relational schema and performance analytics suite for an e-commerce platform.",
    },
    "Python Programming": {
        "learn": ["Advanced Pythonic idioms and list/dict comprehensions", "Generators, decorators and context managers",
                  "Virtual environments, poetry and package management", "Unit testing with pytest and typing"],
        "practice": ["Refactor legacy scripts to functional Pythonic patterns", "Write 90%+ coverage unit tests"],
        "project": "Build an open-source Python utility package and publish to PyPI test environment.",
    },
    "NumPy and Pandas": {
        "learn": ["Multi-dimensional ndarrays, vectorization and broadcasting", "Pandas DataFrames, Series and indexing",
                  "Handling missing values, data cleaning and transformation", "High-performance aggregations and pivot tables"],
        "practice": ["Clean and normalize messy real-world CSV/JSON datasets", "Vectorize algorithmic operations to eliminate Python loops"],
        "project": "Perform comprehensive Exploratory Data Analysis (EDA) on a 1M+ row financial dataset.",
    },
    "Statistics": {
        "learn": ["Descriptive statistics (Mean, Median, Variance, Std Dev)", "Probability distributions (Normal, Binomial, Poisson)",
                  "Hypothesis testing (p-values, z-test, t-test, ANOVA)", "Correlation, covariance and regression fundamentals"],
        "practice": ["Calculate statistical tests in Python using scipy.stats", "Formulate and validate A/B testing hypotheses"],
        "project": "Conduct an end-to-end A/B test analysis and business recommendation report.",
    },
    "Machine Learning": {
        "learn": ["Supervised learning (Linear/Logistic Regression, Trees, Ensembles)", "Unsupervised learning (K-Means, PCA, Hierarchical Clustering)",
                  "Feature engineering, scaling and encoding", "Cross-validation and hyperparameter optimization"],
        "practice": ["Train and compare baseline models with Scikit-Learn", "Diagnose overfitting/underfitting via learning curves"],
        "project": "Build a predictive customer churn prediction model with SHAP explainability.",
    },
    "Deep Learning": {
        "learn": ["Artificial Neural Networks, backpropagation and optimizers", "Convolutional Neural Networks (CNNs) for vision",
                  "Recurrent Networks (RNNs, LSTMs) and Transformers", "Transfer learning and fine-tuning pretrained models"],
        "practice": ["Train small neural nets on GPU via PyTorch/TensorFlow", "Implement data augmentation pipelines"],
        "project": "Train an image classification or sentiment analysis transformer model.",
    },
    "TensorFlow / PyTorch": {
        "learn": ["Tensors, computation graphs and automatic differentiation", "Building custom layers and loss functions in PyTorch",
                  "DataLoaders, dataset streaming and GPU acceleration", "Exporting models to ONNX and TorchScript"],
        "practice": ["Replicate a published computer vision or NLP research paper", "Benchmark PyTorch vs TensorFlow latency"],
        "project": "Build an end-to-end computer vision pipeline with real-time inference.",
    },
    "Model Deployment": {
        "learn": ["REST API development with FastAPI", "Containerization with Docker",
                  "Model serialization (Joblib, ONNX)", "Cloud deployment to AWS/GCP"],
        "practice": ["Dockerize ML microservices", "Deploy containerized APIs with latency < 50ms"],
        "project": "Deploy an interactive ML model with FastAPI backend and Streamlit UI.",
    },
    "MLOps": {
        "learn": ["Experiment tracking with MLflow / Weights & Biases", "Data version control with DVC",
                  "CI/CD pipelines with GitHub Actions", "Model monitoring, data drift and automated retraining"],
        "practice": ["Track 10+ experiment iterations with parameter logs", "Set up automated test and build workflows"],
        "project": "Build an automated continuous delivery ML pipeline that redeploys on code push.",
    },
    "Projects & Portfolio": {
        "learn": ["Production code structuring and documentation", "Writing compelling GitHub READMEs",
                  "System architecture diagrams", "Technical storytelling and interview demo presentation"],
        "practice": ["Record 2-minute Loom project walkthroughs", "Engage in peer code reviews"],
        "project": "Ship a polished capstone project live with a public demo and GitHub repository.",
    },
}

# ============================================================
# CURATED RESOURCE DIRECTORY (PRESERVED & EXPANDED)
# ============================================================
RESOURCES = {
    "python": ("Python Official Tutorial & Docs", "https://docs.python.org/3/tutorial/"),
    "sql": ("SQL Tutorial (W3Schools)", "https://www.w3schools.com/sql/"),
    "machine learning": ("Kaggle Learn: Machine Learning", "https://www.kaggle.com/learn"),
    "deep learning": ("Kaggle Learn: Deep Learning", "https://www.kaggle.com/learn"),
    "data structures": ("Practice DSA Problems on LeetCode", "https://leetcode.com/problemset/"),
    "algorithms": ("Practice DSA Problems on LeetCode", "https://leetcode.com/problemset/"),
    "git": ("Git Official Documentation", "https://git-scm.com/doc"),
    "javascript": ("MDN JavaScript Guide", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"),
    "html": ("MDN HTML Learning Area", "https://developer.mozilla.org/en-US/docs/Learn/HTML"),
    "css": ("MDN CSS Learning Area", "https://developer.mozilla.org/en-US/docs/Learn/CSS"),
    "react": ("React Official Documentation", "https://react.dev/learn"),
    "statistics": ("Khan Academy Statistics & Probability", "https://www.khanacademy.org/math/statistics-probability"),
    "data analysis": ("freeCodeCamp Data Analysis with Python", "https://www.freecodecamp.org/learn/data-analysis-with-python/"),
    "numpy": ("NumPy Official Quickstart Guide", "https://numpy.org/doc/stable/user/quickstart.html"),
    "pandas": ("Pandas Official Getting Started", "https://pandas.pydata.org/docs/getting_started/"),
    "tensorflow": ("TensorFlow Official Core Tutorials", "https://www.tensorflow.org/tutorials"),
    "pytorch": ("PyTorch Official Deep Learning Tutorials", "https://pytorch.org/tutorials/"),
    "power bi": ("Microsoft Learn: Power BI Fundamentals", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"),
    "tableau": ("Tableau Free Training Videos", "https://www.tableau.com/learn/training"),
    "excel": ("Microsoft Excel Video Training", "https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-977d-773303288438"),
    "java": ("Oracle Java Tutorials & Guide", "https://docs.oracle.com/javase/tutorial/"),
    "c++": ("Learn C++ Tutorials", "https://www.learncpp.com/"),
}

# ============================================================
# ADAPTIVE ASSESSMENTS DATA
# ============================================================
ASSESSMENT_TOPICS = {
    "Statistics": {
        "title": "Statistics & Probability Diagnostic",
        "description": "Evaluate your foundation in descriptive stats, distributions, correlation, and standard deviation.",
        "questions": [
            {
                "id": 1, "topic": "Probability",
                "question": "If two fair dice are rolled, what is the probability of getting a sum equal to 7?",
                "options": ["1 / 12", "1 / 6", "5 / 36", "1 / 4"],
                "answer": "1 / 6",
                "explanation": "There are 6 favorable outcomes (1+6, 2+5, 3+4, 4+3, 5+2, 6+1) out of 36 total possibilities. 6/36 = 1/6.",
            },
            {
                "id": 2, "topic": "Correlation",
                "question": "A Pearson correlation coefficient of r = -0.85 between variables X and Y signifies:",
                "options": ["A weak inverse relationship", "A strong inverse linear relationship", "No linear relationship", "A causality where X causes Y"],
                "answer": "A strong inverse linear relationship",
                "explanation": "Values close to -1 indicate a strong negative linear correlation, though correlation does not imply causation.",
            },
            {
                "id": 3, "topic": "Variance",
                "question": "What is the mathematical relationship between Variance and Standard Deviation?",
                "options": ["Variance is the square root of Standard Deviation", "Variance is the square of Standard Deviation", "Variance is twice the Standard Deviation", "They are identical measures"],
                "answer": "Variance is the square of Standard Deviation",
                "explanation": "Standard deviation is defined as the square root of the variance: σ = √(Var).",
            },
            {
                "id": 4, "topic": "Standard Deviation",
                "question": "In a standard normal distribution (mean=0, std=1), what percentage of data falls within ±1 standard deviation?",
                "options": ["Approximately 50%", "Approximately 68%", "Approximately 95%", "Approximately 99.7%"],
                "answer": "Approximately 68%",
                "explanation": "By the empirical 68-95-99.7 rule, roughly 68.27% of observations fall within ±1 standard deviation of the mean.",
            },
            {
                "id": 5, "topic": "Standard Deviation",
                "question": "If every value in a dataset is increased by adding 10, what happens to the Standard Deviation?",
                "options": ["Increases by 10", "Multiplies by 10", "Remains unchanged", "Becomes zero"],
                "answer": "Remains unchanged",
                "explanation": "Adding a constant shifts the entire distribution without altering the dispersion or spread around the new mean.",
            },
        ],
    },
    "Python": {
        "title": "Python & Systems Architecture Diagnostic",
        "description": "Assess proficiency in data structures, decorators, memory references, and algorithmic complexity.",
        "questions": [
            {
                "id": 1, "topic": "Data Structures",
                "question": "What is the average time complexity for checking membership (`item in collection`) in a Python set?",
                "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
                "answer": "O(1)",
                "explanation": "Python sets use hash tables under the hood, enabling average O(1) constant time lookups.",
            },
            {
                "id": 2, "topic": "Decorators",
                "question": "What does the `@functools.wraps` decorator do when applied to a wrapper function?",
                "options": ["Prevents the wrapped function from raising errors", "Preserves the original function's name, docstring, and metadata", "Makes the function run asynchronously", "Caches function return values"],
                "answer": "Preserves the original function's name, docstring, and metadata",
                "explanation": "`functools.wraps` copies `__name__`, `__doc__`, and annotations from the original function to the wrapper.",
            },
            {
                "id": 3, "topic": "Generators",
                "question": "What is the primary advantage of using a Generator expression instead of a List comprehension?",
                "options": ["Faster syntax parsing", "Lazy evaluation with minimal memory footprint", "Ability to index items by key", "Automatic multithreading"],
                "answer": "Lazy evaluation with minimal memory footprint",
                "explanation": "Generators yield elements on demand rather than storing the entire dataset in memory.",
            },
        ],
    },
}

# ============================================================
# PORTFOLIO PROJECT BLUEPRINTS
# ============================================================
CAREER_PROJECTS = {
    "ML Engineer": [
        {
            "tier": "Production Capstone",
            "badge": "Advanced",
            "title": "End-to-End Customer Churn Predictor with FastAPI & Docker",
            "desc": "Architect and deploy an enterprise-grade churn prediction service with real-time inference endpoints, Docker containerization, and model monitoring.",
            "stack": ["Python", "Scikit-Learn", "FastAPI", "Docker", "Streamlit", "PostgreSQL"],
            "deliverables": [
                "Feature engineering pipeline handling categorical encoding and scaling",
                "Trained XGBoost / LightGBM model with cross-validated ROC-AUC > 0.88",
                "FastAPI REST endpoints with Pydantic request validation",
                "Dockerfile and docker-compose.yml for one-command deployment",
            ],
            "impact": "Demonstrates mastery of model serialization, REST API architecture, and containerized deployment.",
        },
        {
            "tier": "Deep Learning Pipeline",
            "badge": "Intermediate",
            "title": "Real-Time Object Detection & Tracking Visualizer",
            "desc": "Build a computer vision web app leveraging YOLOv8 and PyTorch to perform object counting, inference streaming, and bounding-box overlay.",
            "stack": ["PyTorch", "YOLOv8", "OpenCV", "Streamlit", "NumPy"],
            "deliverables": [
                "Dataset annotation and transfer learning on custom classes",
                "Real-time webcam or video upload inference pipeline",
                "Interactive UI with confidence threshold and class filtering sliders",
            ],
            "impact": "Highlights practical deep learning, tensor manipulation, and interactive CV frontends.",
        },
    ],
    "Data Scientist": [
        {
            "tier": "Analytics Capstone",
            "badge": "Advanced",
            "title": "Credit Risk Scoring Engine with SHAP Model Explainability",
            "desc": "Build an explainable machine learning risk assessment engine that predicts loan default probability and generates regulatory SHAP explanations.",
            "stack": ["Python", "Pandas", "Scikit-Learn", "SHAP", "Plotly", "Streamlit"],
            "deliverables": [
                "Rigorous exploratory analysis of credit bureau data and weight-of-evidence encoding",
                "Ensemble model calibrated with Platt Scaling / Isotonic Regression",
                "Interactive waterfall chart explaining why an individual applicant was approved or denied",
            ],
            "impact": "Proves ability to communicate complex machine learning decisions to business stakeholders.",
        },
    ],
    "Software Engineer": [
        {
            "tier": "Distributed Systems",
            "badge": "Advanced",
            "title": "High-Throughput Scalable URL Shortener & Analytics Service",
            "desc": "Design a resilient URL shortening architecture capable of handling high write throughput using base62 encoding, Redis caching, and PostgreSQL persistence.",
            "stack": ["Python", "FastAPI", "Redis", "PostgreSQL", "Docker", "Nginx"],
            "deliverables": [
                "Distributed ID generation algorithm avoiding race conditions",
                "Redis write-through caching layer yielding sub-10ms redirect latency",
                "Click tracking analytics pipeline with geographical and referer telemetry",
            ],
            "impact": "Demonstrates backend scalability, caching strategies, and robust database design.",
        },
    ],
}

# ============================================================
# DESIGN SYSTEM & GLOBAL CSS
# ============================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@600;700;800&display=swap');

:root {
  --bg-page: #f8fafc;
  --bg-card: #ffffff;
  --ink-900: #0a0f1d;
  --ink-800: #141f36;
  --ink-700: #233354;
  --ink-500: #54658a;
  --ink-300: #94a3b8;
  --brand-indigo: #4f46e5;
  --brand-purple: #7c3aed;
  --brand-cyan: #06b6d4;
  --brand-blue: #2563eb;
  --emerald: #10b981;
  --amber: #f59e0b;
  --rose: #f43f5e;
  --border-subtle: #e2e8f0;
  --border-card: rgba(226, 232, 240, 0.9);
  --shadow-sm: 0 2px 6px rgba(15, 23, 42, 0.04);
  --shadow-md: 0 10px 25px -4px rgba(15, 23, 42, 0.07);
  --shadow-lg: 0 20px 40px -10px rgba(15, 23, 42, 0.1);
  --radius-xl: 20px;
  --radius-lg: 16px;
  --radius-md: 12px;
}

/* Base resets & typography */
html, body, .stApp, [class*="css"] {
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif !important;
  color: var(--ink-800);
}
.stApp {
  background: var(--bg-page);
}
header[data-testid="stHeader"] {
  background: transparent !important;
}
footer {
  display: none !important;
}
.block-container {
  max-width: 1440px !important;
  padding: 1.2rem 2rem 3.5rem !important;
}

/* Headings */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Sora', sans-serif !important;
  color: var(--ink-900) !important;
  letter-spacing: -0.02em !important;
}

/* ============================================================
   SIDEBAR (STARTUP DEEP NAVY / INDIGO)
   ============================================================ */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #070a14 0%, #0c1222 40%, #111a33 100%) !important;
  border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
  min-width: 290px !important;
}
section[data-testid="stSidebar"] * {
  color: #e2e8f8 !important;
}
section[data-testid="stSidebar"] .stButton > button {
  background: transparent !important;
  border: 1px solid transparent !important;
  justify-content: flex-start !important;
  text-align: left !important;
  color: #b0bfdc !important;
  padding: 0.65rem 1rem !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  font-size: 13.5px !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  margin-bottom: 2px !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #ffffff !important;
  transform: translateX(3px) !important;
  border-color: rgba(255, 255, 255, 0.12) !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
  color: #ffffff !important;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.35) !important;
}

/* Standard Buttons */
.stButton > button {
  border-radius: 12px !important;
  font-weight: 600 !important;
  padding: 0.55rem 1.1rem !important;
  transition: all 0.2s ease !important;
  border: 1.5px solid var(--border-subtle) !important;
  background: #ffffff !important;
  color: var(--ink-800) !important;
}
.stButton > button:hover {
  border-color: var(--brand-indigo) !important;
  color: var(--brand-indigo) !important;
  transform: translateY(-2px) !important;
  box-shadow: var(--shadow-sm) !important;
}
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
  border: 1px solid #4f46e5 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
}
.stButton > button[kind="primary"]:hover {
  background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
  color: #ffffff !important;
  box-shadow: 0 8px 24px rgba(79, 70, 229, 0.45) !important;
}

/* Inputs & Form controls */
div[data-baseweb="select"] > div, .stTextInput input, .stNumberInput input, .stMultiSelect {
  border-radius: 12px !important;
  background: #ffffff !important;
  border-color: var(--border-subtle) !important;
  font-size: 14px !important;
}
}
div[data-testid="stExpander"] {
  background: #ffffff !important;
  border: 1.5px solid var(--border-subtle) !important;
  border-radius: 16px !important;
  margin-bottom: 0.85rem !important;
  box-shadow: var(--shadow-sm) !important;
  overflow: hidden !important;
}

div[data-testid="stMetric"] {
  background: #ffffff !important;
  border: 1.5px solid var(--border-subtle) !important;
  border-radius: 14px !important;
  padding: 14px 18px !important;
  box-shadow: var(--shadow-sm) !important;
}
div[data-testid="stMetricLabel"] p {
  color: var(--ink-500) !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}
div[data-testid="stMetricValue"] {
  font-family: 'Sora', sans-serif !important;
  color: var(--ink-900) !important;
  font-size: 21px !important;
  white-space: normal !important;
  overflow: visible !important;
  text-overflow: clip !important;
}

/* Cards & Components */
.rx-card {
  background: #ffffff;
  border: 1.5px solid var(--border-card);
  border-radius: 18px;
  padding: 22px 24px;
  margin-bottom: 16px;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s ease;
}
.rx-card:hover {
  box-shadow: var(--shadow-md);
}

/* Hero Banner */
.rx-hero-banner {
  background: linear-gradient(135deg, #0b1120 0%, #151d38 50%, #1c274c 100%);
  border-radius: 22px;
  padding: 34px 40px;
  color: #ffffff;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-lg);
  margin-bottom: 22px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.rx-hero-banner h1 {
  color: #ffffff !important;
  font-size: 30px;
  margin: 0 0 10px;
}
.rx-hero-banner p {
  color: #cbd5e1;
  font-size: 15.5px;
  line-height: 1.6;
  max-width: 680px;
  margin: 0;
}
.rx-hero-badges {
  display: flex;
  gap: 12px;
  margin-top: 20px;
  flex-wrap: wrap;
}
.rx-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid rgba(255, 255, 255, 0.18);
  color: #e2e8f0;
}

/* Loop Flow: LEARN -> ASSESS -> ANALYZE -> ADAPT */
.rx-flow-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}
.rx-flow-step {
  background: #ffffff;
  border: 1.5px solid var(--border-card);
  border-radius: 16px;
  padding: 16px 18px;
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  transition: all 0.25s ease;
  box-shadow: var(--shadow-sm);
}
.rx-flow-step:hover {
  transform: translateY(-2px);
  border-color: var(--brand-indigo);
  box-shadow: var(--shadow-md);
}
.rx-flow-step.active {
  background: linear-gradient(135deg, #eef2ff 0%, #ffffff 100%);
  border-color: #6366f1;
  box-shadow: 0 4px 18px rgba(99, 102, 241, 0.18);
}
.rx-flow-num {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: 16px;
  flex: none;
  color: var(--brand-indigo);
}
.rx-flow-step.active .rx-flow-num {
  background: var(--brand-indigo);
  color: #ffffff;
}
.rx-flow-content b {
  display: block;
  font-size: 13.5px;
  color: var(--ink-900);
}
.rx-flow-content span {
  font-size: 12px;
  color: var(--ink-500);
}

/* KPI Stat Cards */
.rx-kpis {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
  margin-bottom: 20px;
}
.rx-kpi {
  background: #ffffff;
  border: 1.5px solid var(--border-card);
  border-radius: 18px;
  padding: 18px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: var(--shadow-sm);
  transition: all 0.25s ease;
}
.rx-kpi:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-md);
}
.rx-kpi-ico {
  width: 50px;
  height: 50px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  flex: none;
}
.rx-kpi-num {
  font-family: 'Sora', sans-serif;
  font-size: 24px;
  font-weight: 800;
  line-height: 1.1;
  color: var(--ink-900);
}
.rx-kpi-lbl {
  font-size: 12px;
  font-weight: 600;
  color: var(--ink-500);
  margin-top: 3px;
}

/* Multi-Path Tree Visualization */
.rx-tree-box {
  background: #ffffff;
  border: 1.5px solid var(--border-card);
  border-radius: 20px;
  padding: 26px 28px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
}
.rx-tree-root {
  text-align: center;
  margin-bottom: 24px;
}
.rx-tree-node-root {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 10px 22px;
  background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
  color: #ffffff !important;
  border-radius: 99px;
  font-family: 'Sora', sans-serif;
  font-size: 15px;
  font-weight: 700;
  box-shadow: 0 6px 20px rgba(49, 46, 129, 0.28);
}
.rx-tree-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  position: relative;
}
.rx-tree-branch {
  background: #ffffff;
  border: 1.5px solid var(--border-card);
  border-radius: 16px;
  padding: 18px 20px;
  transition: all 0.25s ease;
  position: relative;
  cursor: pointer;
}
.rx-tree-branch:hover {
  transform: translateY(-4px);
  border-color: #6366f1;
  box-shadow: 0 12px 28px -4px rgba(99, 102, 241, 0.2);
}
.rx-tree-branch.active {
  background: linear-gradient(135deg, #f5f3ff 0%, #ffffff 100%);
  border: 2px solid #6366f1;
  box-shadow: 0 10px 30px -4px rgba(99, 102, 241, 0.25);
}
.rx-tree-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.rx-tree-badge {
  font-family: 'Sora', sans-serif;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 99px;
}
.rx-tree-nodes {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 10px;
}
.rx-tree-substep {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  color: var(--ink-700);
}
.rx-tree-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--brand-indigo);
}

/* Timeline / Roadmap */
.rx-timeline {
  position: relative;
  padding-left: 20px;
  margin: 14px 0;
}
.rx-timeline::before {
  content: '';
  position: absolute;
  left: 27px;
  top: 15px;
  bottom: 25px;
  width: 3px;
  background: #e2e8f0;
  border-radius: 99px;
}
.rx-t-item {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  position: relative;
}
.rx-t-node {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #ffffff;
  border: 3px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 13px;
  flex: none;
  z-index: 2;
  transition: all 0.2s ease;
}
.rx-t-item.completed .rx-t-node {
  background: #10b981;
  border-color: #10b981;
  color: #ffffff;
  box-shadow: 0 0 0 5px rgba(16, 185, 129, 0.2);
}
.rx-t-item.active .rx-t-node {
  background: #4f46e5;
  border-color: #4f46e5;
  color: #ffffff;
  box-shadow: 0 0 0 6px rgba(79, 70, 229, 0.25);
  animation: pulse-ring 2s infinite;
}
@keyframes pulse-ring {
  0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.5); }
  70% { box-shadow: 0 0 0 10px rgba(79, 70, 229, 0); }
  100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
}

/* Skill Gap Badges */
.rx-pill {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 12.5px;
  font-weight: 700;
  margin: 3px 6px 3px 0;
}
.rx-pill-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.rx-pill-blue { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
.rx-pill-amber { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }
.rx-pill-rose { background: #ffe4e6; color: #be123c; border: 1px solid #fecdd3; }

/* Responsive adjustments */
@media(max-width: 1024px) {
  .rx-flow-container { grid-template-columns: repeat(2, 1fr); }
  .rx-kpis { grid-template-columns: repeat(2, 1fr); }
}
@media(max-width: 650px) {
  .rx-flow-container { grid-template-columns: 1fr; }
  .rx-kpis { grid-template-columns: 1fr; }
  .rx-hero-banner { padding: 22px 24px; }
}
</style>
"""

# ============================================================
# COMPONENT STYLES (CARD_CSS & COLOR THEMES)
# ============================================================
CARD_CSS = """
<style>
.rx { font-family: 'Plus Jakarta Sans', system-ui, sans-serif; color: #141f36; }
.rx-cblock {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 15px 18px;
  border-radius: 16px;
  margin-bottom: 12px;
  text-decoration: none !important;
  color: inherit;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.rx-cblock:hover { transform: translateY(-3px); text-decoration: none !important; }
.rx-cblock-ico {
  width: 46px; height: 46px; border-radius: 13px; display: flex; align-items: center;
  justify-content: center; font-size: 22px; flex: none; box-shadow: 0 4px 12px rgba(0,0,0,0.07);
}
.rx-cblock-info { flex: 1; min-width: 0; }
.rx-cblock-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 3px; }
.rx-cblock-title { font-family: 'Sora', sans-serif; font-weight: 700; font-size: 15px; letter-spacing: -0.01em; }
.rx-cblock-tag { font-size: 10.5px; font-weight: 700; padding: 2px 8px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.04em; }
.rx-cblock-sub { font-size: 12.5px; font-weight: 500; line-height: 1.4; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.rx-cblock-action { flex: none; display: flex; align-items: center; }
.rx-cblock-btn {
  font-size: 12px; font-weight: 700; padding: 6px 12px; border-radius: 10px; display: inline-flex;
  align-items: center; gap: 4px; background: rgba(255,255,255,0.88); backdrop-filter: blur(6px);
  border: 1px solid rgba(255,255,255,0.95); box-shadow: 0 2px 6px rgba(0,0,0,0.04); transition: all 0.2s ease;
}
.rx-cblock:hover .rx-cblock-btn { background: #ffffff; transform: translateX(3px); box-shadow: 0 4px 10px rgba(0,0,0,0.08); }

/* 10 Themed Gradients */
.rx-c-violet { background: linear-gradient(135deg,#f5f3ff 0%,#ede9fe 100%); border: 1.5px solid #c4b5fd; border-left: 5px solid #8b5cf6; }
.rx-c-violet:hover { border-color: #8b5cf6; box-shadow: 0 12px 28px -4px rgba(139,92,246,0.28); }
.rx-c-violet .rx-cblock-ico { background: linear-gradient(135deg,#8b5cf6,#6d28d9); }
.rx-c-violet .rx-cblock-title { color: #3b0764; } .rx-c-violet .rx-cblock-sub { color: #5b21b6; }
.rx-c-violet .rx-cblock-tag { background: #ddd6fe; color: #5b21b6; } .rx-c-violet .rx-cblock-btn { color: #6d28d9; }

.rx-c-emerald { background: linear-gradient(135deg,#ecfdf5 0%,#d1fae5 100%); border: 1.5px solid #6ee7b7; border-left: 5px solid #10b981; }
.rx-c-emerald:hover { border-color: #10b981; box-shadow: 0 12px 28px -4px rgba(16,185,129,0.28); }
.rx-c-emerald .rx-cblock-ico { background: linear-gradient(135deg,#10b981,#047857); }
.rx-c-emerald .rx-cblock-title { color: #064e3b; } .rx-c-emerald .rx-cblock-sub { color: #047857; }
.rx-c-emerald .rx-cblock-tag { background: #a7f3d0; color: #065f46; } .rx-c-emerald .rx-cblock-btn { color: #059669; }

.rx-c-blue { background: linear-gradient(135deg,#f0f9ff 0%,#e0f2fe 100%); border: 1.5px solid #7dd3fc; border-left: 5px solid #0284c7; }
.rx-c-blue:hover { border-color: #0284c7; box-shadow: 0 12px 28px -4px rgba(2,132,199,0.28); }
.rx-c-blue .rx-cblock-ico { background: linear-gradient(135deg,#0284c7,#0369a1); }
.rx-c-blue .rx-cblock-title { color: #082f49; } .rx-c-blue .rx-cblock-sub { color: #075985; }
.rx-c-blue .rx-cblock-tag { background: #bae6fd; color: #0369a1; } .rx-c-blue .rx-cblock-btn { color: #0284c7; }

.rx-c-amber { background: linear-gradient(135deg,#fffbeb 0%,#fef3c7 100%); border: 1.5px solid #fcd34d; border-left: 5px solid #f59e0b; }
.rx-c-amber:hover { border-color: #f59e0b; box-shadow: 0 12px 28px -4px rgba(245,158,11,0.28); }
.rx-c-amber .rx-cblock-ico { background: linear-gradient(135deg,#f59e0b,#b45309); }
.rx-c-amber .rx-cblock-title { color: #451a03; } .rx-c-amber .rx-cblock-sub { color: #92400e; }
.rx-c-amber .rx-cblock-tag { background: #fde68a; color: #92400e; } .rx-c-amber .rx-cblock-btn { color: #d97706; }

.rx-c-rose { background: linear-gradient(135deg,#fff1f2 0%,#ffe4e6 100%); border: 1.5px solid #fda4af; border-left: 5px solid #f43f5e; }
.rx-c-rose:hover { border-color: #f43f5e; box-shadow: 0 12px 28px -4px rgba(244,63,94,0.28); }
.rx-c-rose .rx-cblock-ico { background: linear-gradient(135deg,#f43f5e,#be123c); }
.rx-c-rose .rx-cblock-title { color: #4c0519; } .rx-c-rose .rx-cblock-sub { color: #9f1239; }
.rx-c-rose .rx-cblock-tag { background: #fecdd3; color: #9f1239; } .rx-c-rose .rx-cblock-btn { color: #e11d48; }

.rx-c-cyan { background: linear-gradient(135deg,#ecfeff 0%,#cffafe 100%); border: 1.5px solid #67e8f9; border-left: 5px solid #06b6d4; }
.rx-c-cyan:hover { border-color: #06b6d4; box-shadow: 0 12px 28px -4px rgba(6,182,212,0.28); }
.rx-c-cyan .rx-cblock-ico { background: linear-gradient(135deg,#06b6d4,#0e7490); }
.rx-c-cyan .rx-cblock-title { color: #083344; } .rx-c-cyan .rx-cblock-sub { color: #155e75; }
.rx-c-cyan .rx-cblock-tag { background: #a5f3fc; color: #155e75; } .rx-c-cyan .rx-cblock-btn { color: #0891b2; }

.rx-c-fuchsia { background: linear-gradient(135deg,#fdf4ff 0%,#fae8ff 100%); border: 1.5px solid #f0abfc; border-left: 5px solid #d946ef; }
.rx-c-fuchsia:hover { border-color: #d946ef; box-shadow: 0 12px 28px -4px rgba(217,70,239,0.28); }
.rx-c-fuchsia .rx-cblock-ico { background: linear-gradient(135deg,#d946ef,#a21caf); }
.rx-c-fuchsia .rx-cblock-title { color: #4a044e; } .rx-c-fuchsia .rx-cblock-sub { color: #86198f; }
.rx-c-fuchsia .rx-cblock-tag { background: #f5d0fe; color: #86198f; } .rx-c-fuchsia .rx-cblock-btn { color: #c026d3; }

.rx-c-orange { background: linear-gradient(135deg,#fff7ed 0%,#ffedd5 100%); border: 1.5px solid #fdba74; border-left: 5px solid #f97316; }
.rx-c-orange:hover { border-color: #f97316; box-shadow: 0 12px 28px -4px rgba(249,115,22,0.28); }
.rx-c-orange .rx-cblock-ico { background: linear-gradient(135deg,#f97316,#c2410c); }
.rx-c-orange .rx-cblock-title { color: #431407; } .rx-c-orange .rx-cblock-sub { color: #9a3412; }
.rx-c-orange .rx-cblock-tag { background: #fed7aa; color: #9a3412; } .rx-c-orange .rx-cblock-btn { color: #ea580c; }

.rx-c-indigo { background: linear-gradient(135deg,#eef2ff 0%,#e0e7ff 100%); border: 1.5px solid #a5b4fc; border-left: 5px solid #6366f1; }
.rx-c-indigo:hover { border-color: #6366f1; box-shadow: 0 12px 28px -4px rgba(99,102,241,0.28); }
.rx-c-indigo .rx-cblock-ico { background: linear-gradient(135deg,#6366f1,#4338ca); }
.rx-c-indigo .rx-cblock-title { color: #1e1b4b; } .rx-c-indigo .rx-cblock-sub { color: #3730a3; }
.rx-c-indigo .rx-cblock-tag { background: #c7d2fe; color: #3730a3; } .rx-c-indigo .rx-cblock-btn { color: #4f46e5; }

.rx-c-teal { background: linear-gradient(135deg,#f0fdfa 0%,#ccfbf1 100%); border: 1.5px solid #5eead4; border-left: 5px solid #14b8a6; }
.rx-c-teal:hover { border-color: #14b8a6; box-shadow: 0 12px 28px -4px rgba(20,184,166,0.28); }
.rx-c-teal .rx-cblock-ico { background: linear-gradient(135deg,#14b8a6,#0f766e); }
.rx-c-teal .rx-cblock-title { color: #042f2e; } .rx-c-teal .rx-cblock-sub { color: #115e59; }
.rx-c-teal .rx-cblock-tag { background: #99f6e4; color: #115e59; } .rx-c-teal .rx-cblock-btn { color: #0d9488; }
</style>
"""

COLOR_THEMES = ["violet", "emerald", "blue", "amber", "rose", "cyan", "fuchsia", "orange", "indigo", "teal"]

TOPIC_META = {
    "python": ("🐍", "Programming"),
    "machine learning": ("🤖", "AI & ML"),
    "deep learning": ("🧠", "Neural Nets"),
    "data analysis": ("📊", "Analytics"),
    "sql": ("🗄️", "Database"),
    "numpy": ("🐼", "Data Science"),
    "pandas": ("🐼", "Data Science"),
    "statistics": ("📈", "Math & Stats"),
    "tensorflow": ("🔥", "Deep Learning"),
    "pytorch": ("⚡", "Deep Learning"),
    "data structures": ("🧩", "CS Core"),
    "algorithms": ("🌳", "CS Core"),
    "git": ("🐙", "Version Control"),
    "javascript": ("⚡", "Web Dev"),
    "html": ("🌐", "Frontend"),
    "css": ("🎨", "Styling"),
    "react": ("⚛️", "Frontend"),
    "java": ("☕", "Language"),
    "c++": ("⚙️", "Systems"),
    "cloud": ("☁️", "Cloud"),
    "aws": ("☁️", "Cloud"),
    "azure": ("☁️", "Cloud"),
    "power bi": ("📊", "BI Tool"),
    "tableau": ("📉", "BI Tool"),
    "excel": ("📗", "Spreadsheets"),
}

CAREER_PALETTES = [
    ("#6366f1", "#eef2ff", "📊"),
    ("#06b6d4", "#ecfeff", "🧠"),
    ("#10b981", "#ecfdf5", "📈"),
    ("#f59e0b", "#fffbeb", "🗄️"),
    ("#f43f5e", "#fff1f2", "💻"),
]

# Apply Global CSS
st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS (PRESERVED & EXPANDED)
# ============================================================
def card_html(inner: str) -> None:
    st.html(CARD_CSS + f'<div class="rx">{inner}</div>')


def esc(value) -> str:
    return html.escape(str(value))


def normalize_recommendations(data):
    if isinstance(data, dict):
        return list(data.items())
    if isinstance(data, list):
        return data
    return []


def get_career_name(item):
    if isinstance(item, tuple):
        return str(item[0])
    if isinstance(item, dict):
        return str(item.get("career", item.get("career_name", "Career")))
    return "Career"


def get_career_result(item):
    if isinstance(item, tuple):
        return item[1] if isinstance(item[1], dict) else {}
    if isinstance(item, dict):
        return item
    return {}


def get_score(result):
    try:
        return float(result.get("score", result.get("match_score", 0)))
    except (TypeError, ValueError):
        return 0.0


def clean_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [x.strip() for x in value.split(",") if x.strip()]
    return []


def split_custom(text):
    return [x.strip() for x in text.split(",") if x.strip()]


def dedupe(items):
    return list(dict.fromkeys(items))


def default_roadmap():
    return ["Programming Fundamentals", "Data Structures and Algorithms", "SQL",
            "Java / Python", "Projects & Portfolio"]


def current_career():
    """Return (name, result, score, missing, roadmap) for the selected career."""
    recs = normalize_recommendations(st.session_state.recommendations)
    sel = st.session_state.selected_career or (recs[0] if recs else None)
    result = get_career_result(sel) if sel else {}
    roadmap = clean_list(result.get("roadmap", [])) or default_roadmap()
    return (get_career_name(sel) if sel else "Career", result, get_score(result),
            clean_list(result.get("missing_skills", [])), roadmap)


def step_key(career, step):
    return f"done::{career}::{step}"


def progress_for(career, roadmap):
    done = sum(1 for s in roadmap if st.session_state.get(step_key(career, s), False))
    return done, len(roadmap)


def go(page):
    st.session_state.page = page
    st.rerun()


def reset_profile():
    st.session_state.profile = None
    st.session_state.recommendations = None
    st.session_state.selected_career = None
    for k in [k for k in st.session_state if str(k).startswith("done::")]:
        del st.session_state[k]
    go("home")


def match_label(score):
    return "Exceptional Fit" if score >= 80 else "Strong Match" if score >= 65 else "Promising Fit"


def resource_for(skill):
    key = skill.lower()
    for name, (title, url) in RESOURCES.items():
        if name in key:
            return title, url
    return (f"Free {skill} courses and tutorials",
            "https://www.youtube.com/results?search_query=" + quote_plus(f"{skill} full course for beginners"))


def get_topic_meta(topic: str, index: int):
    t_lower = str(topic).lower().strip()
    for key, (ico, tag) in TOPIC_META.items():
        if key in t_lower:
            return ico, tag
    return "📘", "Resource"


def render_color_block(topic: str, title: str, url: str, index: int, custom_tag=None, custom_ico=None) -> str:
    ico, tag = get_topic_meta(topic, index)
    if custom_tag:
        tag = custom_tag
    if custom_ico:
        ico = custom_ico

    theme = COLOR_THEMES[index % len(COLOR_THEMES)]
    display_topic = str(topic).strip()
    if display_topic.islower():
        display_topic = display_topic.title()

    return (
        f'<a class="rx-cblock rx-c-{theme}" href="{esc(url)}" target="_blank" rel="noopener">'
        f'<div class="rx-cblock-ico">{ico}</div>'
        f'<div class="rx-cblock-info">'
        f'<div class="rx-cblock-head">'
        f'<span class="rx-cblock-title">{esc(display_topic)}</span>'
        f'<span class="rx-cblock-tag">{esc(tag)}</span>'
        f'</div>'
        f'<div class="rx-cblock-sub" title="{esc(title)}">{esc(title)}</div>'
        f'</div>'
        f'<div class="rx-cblock-action">'
        f'<span class="rx-cblock-btn">Explore ↗</span>'
        f'</div>'
        f'</a>'
    )


def calculate_career_readiness(profile, score, done_steps, total_steps):
    """Calculates multidimensional career readiness score."""
    skills_count = len(profile.get("skills", []))
    certs_count = len(profile.get("certifications", []))
    
    # 4 dimensions
    skills_pct = min(100, int((skills_count / 8.0) * 100))
    roadmap_pct = int((done_steps / total_steps * 100)) if total_steps else 0
    projects_pct = min(100, int(roadmap_pct * 0.8 + 20 if done_steps > 0 else 30))
    certs_pct = min(100, certs_count * 35 + 30)

    overall = int(skills_pct * 0.35 + roadmap_pct * 0.30 + projects_pct * 0.20 + certs_pct * 0.15)
    return {
        "overall": max(15, min(98, overall)),
        "skills": skills_pct,
        "roadmap": roadmap_pct,
        "projects": projects_pct,
        "certs": certs_pct,
    }


def require_profile():
    if not st.session_state.profile or not normalize_recommendations(st.session_state.recommendations):
        st.info("💡 Create your student profile first to unlock all AI roadmaps and analytics.")
        if st.button("🚀 Create My Profile Now", type="primary"):
            go("home")
        st.stop()


# ============================================================
# MODERN SIDEBAR NAVIGATION
# ============================================================
def render_nav():
    with st.sidebar:
        st.html("""
        <div style="padding:10px 6px 14px;border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:14px">
          <div style="display:flex;align-items:center;gap:10px">
            <div style="width:38px;height:38px;border-radius:11px;background:linear-gradient(135deg,#6366f1,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 4px 14px rgba(99,102,241,0.4)">🚀</div>
            <div>
              <div style="font-family:'Sora',sans-serif;font-weight:800;font-size:20px;color:#fff;letter-spacing:-0.02em">
                Roadmap<span style="color:#38bdf8">X</span> <span style="font-size:12px;background:#312e81;padding:2px 7px;border-radius:6px;border:1px solid #6366f1">AI</span>
              </div>
              <div style="color:#94a3b8;font-size:11.5px;margin-top:-2px">Multi-Path Career Engine</div>
            </div>
          </div>
        </div>
        """)

        for page, icon, label in SIDE_NAV:
            active = st.session_state.page == page
            if st.button(f"{icon}  {label}", key=f"nav_{page}", use_container_width=True,
                         type="primary" if active else "secondary"):
                if page != "home" and page != "settings" and not st.session_state.profile:
                    st.session_state.page = "home"
                    st.toast("Create your profile first to unlock this feature.")
                    st.rerun()
                elif not active:
                    go(page)

        # Bottom Profile Card
        profile = st.session_state.profile
        if profile:
            cname, _, score, _, _ = current_career()
            st.html(f"""
            <div style="margin-top:28px;padding:14px;border-radius:14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1)">
              <div style="display:flex;align-items:center;gap:10px">
                <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#8b5cf6,#3b82f6);display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px;color:#fff">{profile['name'][:1].upper()}</div>
                <div style="flex:1;min-width:0">
                  <div style="font-size:13px;font-weight:700;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{esc(profile['name'])}</div>
                  <div style="font-size:11px;color:#94a3b8">{esc(cname)} ({score:.0f}%)</div>
                </div>
              </div>
            </div>
            """)
        else:
            st.html("""
            <div style="margin-top:24px;padding:14px;border-radius:14px;background:linear-gradient(135deg,#1e1b4b,#312e81);border:1px solid #4338ca">
              <b style="font-size:13px;color:#fff">Placement Ready? 🚀</b>
              <p style="color:#c7d2fe;font-size:11.5px;margin:6px 0 0;line-height:1.4">
                Input your coursework and skills to generate personalized multi-path career roadmaps.
              </p>
            </div>
            """)


# ============================================================
# PAGE: PROFILE (HOME)
# ============================================================
def page_home():
    st.html("""
    <div class="rx-hero-banner">
      <div style="display:inline-block;padding:4px 12px;background:rgba(99,102,241,0.25);border:1px solid rgba(99,102,241,0.4);border-radius:99px;font-size:12px;font-weight:700;color:#a5b4fc;margin-bottom:12px">
        ⚡ AI-POWERED CAREER MAPPING
      </div>
      <h1>Accelerate your career with personalized multi-path roadmaps.</h1>
      <p>Tell us what you study and what you can do. RoadmapX AI matches you to high-demand careers, detects exact skill gaps, and synthesizes week-by-week actionable preparation plans.</p>
      <div class="rx-hero-badges">
        <span class="rx-hero-badge">⚡ 5-Minute Setup</span>
        <span class="rx-hero-badge">🎯 Top 5 Career Match Vectors</span>
        <span class="rx-hero-badge">🗺️ 3 to 12 Month Dynamic Timelines</span>
        <span class="rx-hero-badge">💼 Production Portfolio Projects</span>
      </div>
    </div>
    """)

    st.subheader("Student Career Profile")
    st.caption("Provide your academic background and current skillset to train your personalized recommendations.")

    existing = st.session_state.profile or {}

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown("##### 🎓 Academic Background")
        name = st.text_input("Full Name", value=existing.get("name", ""), placeholder="e.g. Alex Sharma")
        education = st.selectbox(
            "Education Level", EDUCATION_OPTIONS,
            index=EDUCATION_OPTIONS.index(existing["education"]) if existing.get("education") in EDUCATION_OPTIONS else 0)
        specialization = st.selectbox("Specialization / Branch", SPECIALIZATION_OPTIONS)
        final_spec = specialization
        if specialization == "Other":
            final_spec = st.text_input("Specify Specialization", placeholder="e.g. Cyber Security").strip()
        percentage = st.number_input("CGPA or Percentage", 0.0, 100.0,
                                     float(existing.get("cgpa", 82.5)), 0.1,
                                     help="Enter your CGPA out of 10, or overall percentage score.")

    with c2:
        st.markdown("##### 🛠️ Skills & Industry Credentials")
        sel_skills = st.multiselect("Core Skills (Select all you know)", SKILL_OPTIONS,
                                    default=[s for s in existing.get("skills", []) if s in SKILL_OPTIONS],
                                    placeholder="Select skills...")
        other_skills = st.text_input("Other Custom Skills", placeholder="FastAPI, Docker, PyTorch, PySpark",
                                     help="Separate additional skills with commas.")
        sel_certs = st.multiselect("Completed Certifications", CERTIFICATION_OPTIONS,
                                   default=[c for c in existing.get("certifications", []) if c in CERTIFICATION_OPTIONS],
                                   placeholder="Select certifications...")
        other_certs = st.text_input("Other Certifications", placeholder="Coursera Deep Learning Specialization",
                                    help="Separate additional certifications with commas.")

    skills = dedupe(sel_skills + split_custom(other_skills))
    certs = dedupe(sel_certs + split_custom(other_certs))

    st.write("")
    # Row 1: Degree and Specialization in one line
    row1_c1, row1_c2 = st.columns([1, 2], gap="medium")
    row1_c1.metric("Degree", education)
    row1_c2.metric("Specialization", final_spec or "-")

    # Row 2 (next down): Other two metrics
    row2_c1, row2_c2 = st.columns(2, gap="medium")
    row2_c1.metric("Selected Skills", len(skills))
    row2_c2.metric("Certifications", len(certs))

    st.write("")
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("🚀 Analyze & Generate Multi-Path Roadmaps", type="primary", use_container_width=True):
            if not name.strip():
                st.warning("Please enter your name to proceed.")
            elif not final_spec:
                st.warning("Please enter your specialization.")
            elif not skills:
                st.warning("Add at least one technical or professional skill.")
            else:
                profile = {
                    "name": name.strip(), "education": education,
                    "specialization": final_spec, "cgpa": percentage,
                    "skills": skills, "certifications": certs,
                }
                with st.spinner("Executing Career Recommendation Engine..."):
                    try:
                        recs = recommend_careers(
                            education=education, specialization=final_spec,
                            skills=", ".join(skills), certifications=", ".join(certs),
                            cgpa=percentage)
                    except Exception as err:  # noqa: BLE001
                        st.error("Error generating recommendations. Please check inputs.")
                        with st.expander("Details"):
                            st.code(str(err))
                    else:
                        normalized = normalize_recommendations(recs)
                        if not normalized:
                            st.warning("No matches found. Try adding additional skills.")
                        else:
                            st.session_state.profile = profile
                            st.session_state.recommendations = recs
                            st.session_state.selected_career = normalized[0]
                            st.toast("Career profile generated successfully! 🎉")
                            go("dashboard")


# ============================================================
# PAGE: DASHBOARD (MAIN SHOWCASE CENTERPIECE)
# ============================================================
def page_dashboard():
    require_profile()
    profile = st.session_state.profile
    recs = normalize_recommendations(st.session_state.recommendations)
    top = recs[:5]
    name, result, score, missing, roadmap = current_career()
    known = profile["skills"]
    done_flags = [st.session_state.get(step_key(name, r), False) for r in roadmap]
    done, total = sum(done_flags), len(roadmap)
    current_idx = next((i for i, d in enumerate(done_flags) if not d), None)
    pct_progress = (done / total * 100) if total else 0

    readiness = calculate_career_readiness(profile, score, done, total)

    # Top search and user status bar
    initial = esc(profile["name"][:1].upper())
    today = datetime.now().strftime("%B %d, %Y")

    st.html(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;flex-wrap:wrap;gap:12px">
      <div style="display:flex;align-items:center;gap:12px">
        <span style="font-size:13.5px;color:#64748b">📅 {today}</span>
        <span style="background:#e0e7ff;color:#4338ca;font-size:12px;font-weight:700;padding:3px 10px;border-radius:99px">Active Track: {esc(name)}</span>
      </div>
      <div style="display:flex;align-items:center;gap:14px">
        <span style="font-size:13px;font-weight:600;color:#64748b">🔔 2 Notifications</span>
        <div style="display:flex;align-items:center;gap:8px;font-weight:700;font-size:14px">
          <div style="width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#3b82f6);color:#fff;display:flex;align-items:center;justify-content:center">{initial}</div>
          <span>{esc(profile['name'])}</span>
        </div>
      </div>
    </div>
    """)

    # Welcome Banner
    learn_topic = roadmap[current_idx] if current_idx is not None else roadmap[-1]
    st.html(f"""
    <div class="rx-hero-banner" style="margin-bottom:20px">
      <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px">
        <div>
          <div style="display:inline-flex;align-items:center;gap:6px;background:rgba(16,185,129,0.2);border:1px solid rgba(16,185,129,0.4);border-radius:99px;padding:3px 12px;font-size:12px;font-weight:700;color:#6ee7b7;margin-bottom:10px">
            🔥 5-DAY ACTIVE LEARNING STREAK
          </div>
          <h1 style="font-size:28px">Welcome back, {esc(profile['name'])}!</h1>
          <p>AI Career Engine has synthesized multiple career trajectories. Your primary track is <b>{esc(name)}</b> with a <b>{score:.0f}%</b> match fit.</p>
        </div>
        <div style="background:rgba(255,255,255,0.1);backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.2);padding:14px 20px;border-radius:16px;text-align:right">
          <div style="font-size:12px;color:#cbd5e1;font-weight:600">CURRENT MILESTONE</div>
          <div style="font-family:'Sora',sans-serif;font-size:18px;font-weight:700;color:#fff;margin:3px 0">{esc(learn_topic)}</div>
          <div style="font-size:12px;color:#38bdf8;font-weight:600">Step { (current_idx or 0) + 1} of {total} · {pct_progress:.0f}% Complete</div>
        </div>
      </div>
    </div>
    """)

    # Flow Banner: LEARN -> ASSESS -> ANALYZE -> ADAPT ROADMAP
    st.html("""
    <div class="rx-flow-container">
      <div class="rx-flow-step active">
        <div class="rx-flow-num">1</div>
        <div class="rx-flow-content">
          <b>LEARN</b>
          <span>Milestone Curriculum</span>
        </div>
      </div>
      <div class="rx-flow-step">
        <div class="rx-flow-num">2</div>
        <div class="rx-flow-content">
          <b>ASSESS</b>
          <span>Adaptive Quizzes</span>
        </div>
      </div>
      <div class="rx-flow-step">
        <div class="rx-flow-num">3</div>
        <div class="rx-flow-content">
          <b>ANALYZE</b>
          <span>Skill Gap Engine</span>
        </div>
      </div>
      <div class="rx-flow-step">
        <div class="rx-flow-num">4</div>
        <div class="rx-flow-content">
          <b>ADAPT</b>
          <span>Evolving Roadmap</span>
        </div>
      </div>
    </div>
    """)

    # 5 KPI Cards
    st.html(f"""
    <div class="rx-kpis">
      <div class="rx-kpi">
        <div class="rx-kpi-ico" style="background:#eef2ff;color:#6366f1">🎯</div>
        <div>
          <div class="rx-kpi-num">{score:.0f}%</div>
          <div class="rx-kpi-lbl">Top Career Match</div>
        </div>
      </div>
      <div class="rx-kpi">
        <div class="rx-kpi-ico" style="background:#ecfdf5;color:#10b981">🏆</div>
        <div>
          <div class="rx-kpi-num">{readiness['overall']}%</div>
          <div class="rx-kpi-lbl">Career Readiness</div>
        </div>
      </div>
      <div class="rx-kpi">
        <div class="rx-kpi-ico" style="background:#f0f9ff;color:#0284c7">✅</div>
        <div>
          <div class="rx-kpi-num">{len(known)}</div>
          <div class="rx-kpi-lbl">Skills Mastered</div>
        </div>
      </div>
      <div class="rx-kpi">
        <div class="rx-kpi-ico" style="background:#fffbeb;color:#d97706">⚠️</div>
        <div>
          <div class="rx-kpi-num">{len(missing)}</div>
          <div class="rx-kpi-lbl">Skills to Acquire</div>
        </div>
      </div>
      <div class="rx-kpi">
        <div class="rx-kpi-ico" style="background:#fdf4ff;color:#c026d3">⏳</div>
        <div>
          <div class="rx-kpi-num">{done}/{total}</div>
          <div class="rx-kpi-lbl">Milestones Cleared</div>
        </div>
      </div>
    </div>
    """)

    # Multi-Path Branching Tree Preview
    st.html(f"""
    <div class="rx-tree-box">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px">
        <div>
          <h3 style="font-size:18px;margin:0 0 4px">🌿 Multi-Path Career Trajectories</h3>
          <span style="font-size:13px;color:#64748b">Branching exploration paths generated based on your academic profile and skills.</span>
        </div>
        <span style="background:#eef2ff;color:#4f46e5;padding:5px 12px;border-radius:99px;font-size:12px;font-weight:700">Top {len(top)} Trajectories</span>
      </div>
      <div class="rx-tree-root">
        <div class="rx-tree-node-root">
          <span>🎓</span> {esc(profile['name'])} · {esc(profile['education'])} in {esc(profile['specialization'])}
        </div>
      </div>
      <div class="rx-tree-grid">
    """ + "".join([
        f"""
        <div class="rx-tree-branch {'active' if get_career_name(item) == name else ''}">
          <div class="rx-tree-head">
            <span style="font-family:'Sora',sans-serif;font-weight:700;font-size:15px">{esc(get_career_name(item))}</span>
            <span class="rx-tree-badge" style="background:{'#dcfce7;color:#15803d' if get_score(get_career_result(item))>=70 else '#e0f2fe;color:#0284c7'}">
              {get_score(get_career_result(item)):.0f}% Match
            </span>
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:10px">
            {'⭐ Primary Selected Career' if get_career_name(item) == name else 'Alternative Branch'}
          </div>
          <div class="rx-tree-nodes">
            <div class="rx-tree-substep"><span class="rx-tree-dot" style="background:#10b981"></span> Core Skills Match</div>
            <div class="rx-tree-substep"><span class="rx-tree-dot" style="background:#6366f1"></span> Curated Roadmap Path</div>
            <div class="rx-tree-substep"><span class="rx-tree-dot" style="background:#f59e0b"></span> Capstone Placement Prep</div>
          </div>
        </div>
        """ for item in top
    ]) + """
      </div>
    </div>
    """)

    # Grid: Career Options Switcher + Roadmap Timeline
    c_left, c_right = st.columns([1.1, 1], gap="large")

    with c_left:
        st.markdown("##### 🎯 Switch Active Career Path")
        opt_cols = st.columns(len(top))
        for idx, item in enumerate(top):
            c_name = get_career_name(item)
            c_score = get_score(get_career_result(item))
            with opt_cols[idx]:
                if st.button(f"{c_name}\n({c_score:.0f}%)", key=f"dash_switch_{idx}", use_container_width=True,
                             type="primary" if c_name == name else "secondary"):
                    st.session_state.selected_career = item
                    st.rerun()

        # Selected Career Spotlight
        req_pills = "".join(f'<span class="rx-pill rx-pill-green">✓ {esc(s)}</span>' for s in known[:5]) + \
                    "".join(f'<span class="rx-pill rx-pill-rose">✗ {esc(s)}</span>' for s in missing[:5])
        st.html(f"""
        <div class="rx-card" style="margin-top:14px;border-left:5px solid #4f46e5">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <span style="font-family:'Sora',sans-serif;font-size:18px;font-weight:700">🎯 {esc(name)}</span>
            <span style="background:#eef2ff;color:#4f46e5;padding:4px 10px;border-radius:8px;font-weight:700;font-size:12px">{match_label(score)}</span>
          </div>
          <p style="color:#64748b;font-size:13.5px;line-height:1.55;margin-bottom:14px">
            Target pathway customized for your academic parameters. Focus on bridging your key missing competencies while continuing the milestone roadmap.
          </p>
          <div style="margin-bottom:8px;font-size:13px;font-weight:700">Competency Verification Snapshot:</div>
          <div>{req_pills}</div>
        </div>
        """)

        # Next Best Action Card (Guiding UX Principle)
        st.html(f"""
        <div class="rx-card" style="background:linear-gradient(135deg,#eff6ff 0%,#f5f3ff 100%);border:1.5px solid #c7d2fe">
          <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
            <span style="font-size:20px">💡</span>
            <b style="font-size:14px;color:#1e1b4b">RECOMMENDED NEXT ACTION</b>
          </div>
          <div style="font-size:13.5px;color:#334155;line-height:1.5;margin-bottom:14px">
            You're currently on <b>{esc(learn_topic)}</b>. Complete this milestone's exercises, then take the diagnostic assessment to update your skill readiness quotient.
          </div>
        </div>
        """)
        n1, n2 = st.columns(2)
        with n1:
            if st.button("🗺️ Continue Roadmap", type="primary", use_container_width=True):
                go("roadmap")
        with n2:
            if st.button("📝 Take Diagnostic Quiz", use_container_width=True):
                go("assessments")

    with c_right:
        st.markdown("##### 🗺️ Milestone Roadmap Progress")
        t_nodes = ""
        for i, step in enumerate(roadmap[:6]):
            is_done = done_flags[i] if i < len(done_flags) else False
            is_active = (i == current_idx)
            state_cls = "completed" if is_done else ("active" if is_active else "locked")
            status_txt = "Completed ✓" if is_done else ("In Progress ⚡" if is_active else "Locked 🔒")
            t_nodes += f"""
            <div class="rx-t-item {state_cls}">
              <div class="rx-t-node">{i+1}</div>
              <div style="flex:1">
                <div style="font-weight:700;font-size:14px;color:#0f172a">{esc(step)}</div>
                <div style="font-size:12px;color:{'#10b981' if is_done else ('#4f46e5' if is_active else '#94a3b8')};font-weight:600">{status_txt}</div>
              </div>
            </div>
            """
        st.html(f"""
        <div class="rx-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <b style="font-size:14px">Overall Progress: {done}/{total} Steps</b>
            <span style="font-size:12px;font-weight:700;color:#4f46e5">{pct_progress:.0f}%</span>
          </div>
          <div style="height:8px;background:#e2e8f0;border-radius:99px;overflow:hidden;margin-bottom:16px">
            <div style="width:{pct_progress}%;height:100%;background:linear-gradient(90deg,#4f46e5,#06b6d4);border-radius:99px"></div>
          </div>
          <div class="rx-timeline">{t_nodes}</div>
        </div>
        """)

        # Career Readiness breakdown
        st.html(f"""
        <div class="rx-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
            <b style="font-size:15px">📊 Placement Readiness: {readiness['overall']}%</b>
            <span style="font-size:11.5px;color:#10b981;font-weight:700">Target: 85%+</span>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:4px">
              <span>Skills Verified</span><b>{readiness['skills']}%</b>
            </div>
            <div style="height:6px;background:#f1f5f9;border-radius:99px"><div style="width:{readiness['skills']}%;height:100%;background:#10b981;border-radius:99px"></div></div>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:4px">
              <span>Roadmap Completion</span><b>{readiness['roadmap']}%</b>
            </div>
            <div style="height:6px;background:#f1f5f9;border-radius:99px"><div style="width:{readiness['roadmap']}%;height:100%;background:#4f46e5;border-radius:99px"></div></div>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:4px">
              <span>Project Deliverables</span><b>{readiness['projects']}%</b>
            </div>
            <div style="height:6px;background:#f1f5f9;border-radius:99px"><div style="width:{readiness['projects']}%;height:100%;background:#06b6d4;border-radius:99px"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;font-size:12.5px;margin-bottom:4px">
              <span>Certifications</span><b>{readiness['certs']}%</b>
            </div>
            <div style="height:6px;background:#f1f5f9;border-radius:99px"><div style="width:{readiness['certs']}%;height:100%;background:#f59e0b;border-radius:99px"></div></div>
          </div>
        </div>
        """)


# ============================================================
# PAGE: CAREER RECOMMENDATIONS
# ============================================================
def page_recommendations():
    require_profile()
    recs = normalize_recommendations(st.session_state.recommendations)
    active_name = get_career_name(st.session_state.selected_career)

    st.subheader("🎯 Recommended Career Pathways")
    st.caption("AI match scores calculated by cross-analyzing your degree, specialization, CGPA, and technical skillset.")

    cols = st.columns(2, gap="large")
    for idx, item in enumerate(recs):
        cname = get_career_name(item)
        cres = get_career_result(item)
        cscore = get_score(cres)
        missing_skills = clean_list(cres.get("missing_skills", []))
        roadmap_len = len(clean_list(cres.get("roadmap", [])))
        is_active = (cname == active_name)

        with cols[idx % 2]:
            st.html(f"""
            <div class="rx-card" style="border-left:5px solid {'#4f46e5' if is_active else '#94a3b8'};background:{'#f8faff' if is_active else '#ffffff'}">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
                <div>
                  <h3 style="font-size:18px;margin:0 0 4px">{esc(cname)}</h3>
                  <span style="font-size:12px;color:#64748b">Demand Tier: 🔥 Very High · ₹8-20 LPA</span>
                </div>
                <div style="width:48px;height:48px;border-radius:50%;background:conic-gradient(#4f46e5 {cscore*3.6:.0f}deg,#e2e8f0 0);display:flex;align-items:center;justify-content:center">
                  <div style="width:38px;height:38px;background:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:13px;font-family:'Sora',sans-serif">
                    {cscore:.0f}%
                  </div>
                </div>
              </div>
              <div style="margin:12px 0 16px">
                <div style="font-size:12px;font-weight:700;color:#64748b;margin-bottom:6px">SKILL GAPS TO CLOSE ({len(missing_skills)}):</div>
                <div>
                  {"".join(f'<span class="rx-pill rx-pill-rose">{esc(s)}</span>' for s in missing_skills[:4]) or '<span class="rx-pill rx-pill-green">Zero Major Gaps!</span>'}
                </div>
              </div>
            </div>
            """)
            b1, b2 = st.columns(2)
            with b1:
                if st.button("⭐ Select as Primary", key=f"sel_rec_{idx}", type="primary" if is_active else "secondary", use_container_width=True):
                    st.session_state.selected_career = item
                    st.rerun()
            with b2:
                if st.button("🗺️ View Full Roadmap", key=f"rec_map_{idx}", use_container_width=True):
                    st.session_state.selected_career = item
                    go("roadmap")


# ============================================================
# PAGE: MULTI-PATH TREE VISUALIZATION
# ============================================================
def page_multipath():
    require_profile()
    profile = st.session_state.profile
    recs = normalize_recommendations(st.session_state.recommendations)
    active_name, _, _, _, _ = current_career()

    st.subheader("🌿 Interactive Multi-Path Career Tree")
    st.caption("Visually trace how your profile branches into specialized high-demand trajectories.")

    st.html(f"""
    <div class="rx-tree-box">
      <div class="rx-tree-root">
        <div class="rx-tree-node-root">
          <span>🎓</span> {esc(profile['name'])} · {esc(profile['education'])} in {esc(profile['specialization'])}
        </div>
      </div>
      <div style="text-align:center;font-size:24px;color:#6366f1;margin:-10px 0 16px">↓</div>
      <div class="rx-tree-grid">
    """ + "".join([
        f"""
        <div class="rx-tree-branch {'active' if get_career_name(item) == active_name else ''}">
          <div class="rx-tree-head">
            <b style="font-size:16px">{esc(get_career_name(item))}</b>
            <span style="font-weight:800;font-size:13px;color:#4f46e5">{get_score(get_career_result(item)):.0f}% Match</span>
          </div>
          <div style="font-size:12px;color:#64748b;margin-bottom:12px">
            {'⭐ ACTIVE FOCUS CAREER' if get_career_name(item) == active_name else 'ALTERNATIVE TRAJECTORY'}
          </div>
          <div class="rx-tree-nodes">
            <div class="rx-tree-substep">
              <span class="rx-tree-dot" style="background:#10b981"></span>
              <span><b>Stage 1:</b> Core Programming & Data</span>
            </div>
            <div class="rx-tree-substep">
              <span class="rx-tree-dot" style="background:#6366f1"></span>
              <span><b>Stage 2:</b> Advanced Domain Competency</span>
            </div>
            <div class="rx-tree-substep">
              <span class="rx-tree-dot" style="background:#06b6d4"></span>
              <span><b>Stage 3:</b> Production Capstone Project</span>
            </div>
            <div class="rx-tree-substep">
              <span class="rx-tree-dot" style="background:#f59e0b"></span>
              <span><b>Stage 4:</b> Technical Interviews & Placement</span>
            </div>
          </div>
        </div>
        """ for item in recs[:4]
    ]) + """
      </div>
    </div>
    """)

    st.write("")
    st.markdown("##### 🚀 Fast-Switch Selected Branch")
    cols = st.columns(len(recs[:4]))
    for idx, item in enumerate(recs[:4]):
        cname = get_career_name(item)
        with cols[idx]:
            if st.button(f"Focus on {cname}", key=f"mp_switch_{idx}",
                         type="primary" if cname == active_name else "secondary", use_container_width=True):
                st.session_state.selected_career = item
                st.rerun()


# ============================================================
# PAGE: SKILL GAP ANALYSIS
# ============================================================
def page_gaps():
    require_profile()
    profile = st.session_state.profile
    name, _, score, missing, _ = current_career()

    st.subheader(f"🧩 Skill Gap Diagnostic for {name}")
    st.caption("Side-by-side gap matrix comparing skills you possess against target industry expectations.")

    h1, h2, h3 = st.columns(3)
    h1.metric("Mastered Skills", len(profile["skills"]))
    h2.metric("Missing Gaps", len(missing))
    h3.metric("Match Factor", f"{score:.0f}%")

    st.write("")
    c_have, c_need = st.columns(2, gap="large")

    with c_have:
        chips = "".join(f'<span class="rx-pill rx-pill-green">✓ {esc(s)}</span>' for s in profile["skills"])
        card_html(f"""
        <div class="rx-card" style="border-top:4px solid #10b981">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <h3 style="font-size:16px;margin:0">✅ CURRENT SKILLS ({len(profile["skills"])})</h3>
            <span style="font-size:12px;color:#10b981;font-weight:700">Verified</span>
          </div>
          <div>{chips}</div>
        </div>
        """)

    with c_need:
        chips = "".join(f'<span class="rx-pill rx-pill-rose">✗ {esc(s)}</span>' for s in missing) or \
                '<span class="rx-pill rx-pill-green">No major skill gaps identified!</span>'
        card_html(f"""
        <div class="rx-card" style="border-top:4px solid #f43f5e">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <h3 style="font-size:16px;margin:0">⚠️ REQUIRED SKILLS TO ACQUIRE ({len(missing)})</h3>
            <span style="font-size:12px;color:#f43f5e;font-weight:700">Action Required</span>
          </div>
          <div>{chips}</div>
        </div>
        """)

    if missing:
        st.markdown("##### ⚡ How to Close Each Missing Gap")
        left_gap = []
        right_gap = []
        for i, skill in enumerate(missing):
            title, url = resource_for(skill)
            block = render_color_block(skill, title, url, i)
            if i % 2 == 0:
                left_gap.append(block)
            else:
                right_gap.append(block)

        g_cols = st.columns(2, gap="large")
        with g_cols[0]:
            card_html("".join(left_gap))
        with g_cols[1]:
            card_html("".join(right_gap))


# ============================================================
# PAGE: ROADMAP
# ============================================================
def page_roadmap():
    require_profile()
    profile = st.session_state.profile
    name, _, score, missing, roadmap = current_career()

    st.subheader(f"🗺️ Personalized Milestone Roadmap for {name}")
    st.caption(f"Synthesized for {profile['name']}. Match Score: {score:.0f}%.")

    duration = st.radio("Select Preparation Velocity:", ["3 months (Fast Track)", "6 months (Standard Recommended)", "12 months (Comprehensive)"],
                        index=1, horizontal=True)
    months = int(duration.split()[0])
    steps = roadmap[: max(3, min(len(roadmap), months))] if months < 12 else roadmap
    weeks_per = max(1, (months * 4) // len(steps))

    done, total = progress_for(name, steps)
    pct = (done / total * 100) if total else 0

    st.progress(done / total if total else 0, text=f"{done} of {total} Milestones Cleared ({pct:.0f}%)")

    for i, step in enumerate(steps):
        topic = str(step).strip()
        plan = MONTH_PLANS.get(topic, {
            "learn": [f"Core theoretical foundations of {topic}", f"Practical code implementations in {topic}",
                      f"Industry production patterns for {topic}"],
            "practice": [f"Solve 5 practice challenges on {topic}", f"Review common technical interview questions on {topic}"],
            "project": f"Build and document a functional project that incorporates {topic}.",
        })
        start, end = i * weeks_per + 1, (i + 1) * weeks_per
        is_done = st.session_state.get(step_key(name, step), False)

        with st.expander(f"{'✅' if is_done else '📘'}  Weeks {start}-{end}: {topic} {'(Completed)' if is_done else ''}"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**📚 Core Concepts to Master**")
                for t in plan["learn"]:
                    st.markdown(f"- {t}")
            with c2:
                st.markdown("**🛠️ Practical Problem Sets**")
                for t in plan["practice"]:
                    st.markdown(f"- {t}")
            st.info(f"**🚀 Milestone Deliverable:** {plan['project']}")
            title, url = resource_for(topic)
            st.markdown(f"🔗 **Recommended Learning Resource:** [{title}]({url})")
            st.checkbox("Mark milestone as completed", key=step_key(name, step))


# ============================================================
# PAGE: ADAPTIVE LEARNING & ASSESSMENTS
# ============================================================
def page_assessments():
    require_profile()
    name, _, _, missing, _ = current_career()

    st.subheader("📝 Adaptive Learning Assessments")
    st.caption("Diagnose topic strengths and weaknesses. The AI adapts your roadmap to prioritize areas requiring reinforcement.")

    topic_choice = st.selectbox("Select Assessment Track:", list(ASSESSMENT_TOPICS.keys()), index=0)
    quiz_data = ASSESSMENT_TOPICS[topic_choice]

    st.html(f"""
    <div class="rx-card" style="border-left:5px solid #6366f1;background:linear-gradient(135deg,#f8faff 0%,#ffffff 100%)">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
          <h3 style="font-size:18px;margin:0 0 4px">📋 {quiz_data['title']}</h3>
          <span style="font-size:13px;color:#64748b">{quiz_data['description']}</span>
        </div>
        <span style="background:#e0e7ff;color:#4338ca;padding:6px 14px;border-radius:99px;font-size:12px;font-weight:700">
          ⏱️ 10 Mins · {len(quiz_data['questions'])} Questions
        </span>
      </div>
    </div>
    """)

    # Interactive Quiz Form
    with st.form("quiz_form"):
        user_answers = {}
        for q in quiz_data["questions"]:
            st.markdown(f"**Question {q['id']}: {q['question']}** (`Topic: {q['topic']}`)")
            user_answers[q["id"]] = st.radio(
                f"Options for Q{q['id']}", q["options"], key=f"q_{topic_choice}_{q['id']}",
                label_visibility="collapsed")
            st.write("")

        submitted = st.form_submit_button("Submit Diagnostic Assessment", type="primary")

    if submitted:
        correct_count = 0
        topic_stats = {}

        for q in quiz_data["questions"]:
            t = q["topic"]
            if t not in topic_stats:
                topic_stats[t] = {"correct": 0, "total": 0}
            topic_stats[t]["total"] += 1
            if user_answers[q["id"]] == q["answer"]:
                correct_count += 1
                topic_stats[t]["correct"] += 1

        total_q = len(quiz_data["questions"])
        pct_score = int(correct_count / total_q * 100)

        # Performance Dashboard Showcase
        st.write("")
        st.markdown("### 📊 Diagnostic Performance Breakdown")

        st.html(f"""
        <div class="rx-card" style="background:#ffffff;border:2px solid {'#10b981' if pct_score>=70 else '#f59e0b'}">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:14px">
            <div>
              <div style="font-size:13px;color:#64748b;font-weight:600">OVERALL SCORE</div>
              <div style="font-family:'Sora',sans-serif;font-size:32px;font-weight:800;color:#0f172a">{correct_count} / {total_q} ({pct_score}% Score)</div>
              <div style="font-size:13px;color:{'#10b981' if pct_score>=70 else '#f59e0b'};font-weight:700">
                {'✓ Competency Verified' if pct_score>=70 else '⚠ Skill Reinforcement Recommended'}
              </div>
            </div>
            <div style="text-align:right">
              <span style="background:{'#dcfce7;color:#15803d' if pct_score>=70 else '#fef3c7;color:#b45309'};padding:8px 18px;border-radius:12px;font-weight:800;font-size:15px">
                {'Proficient' if pct_score>=70 else 'Needs Practice'}
              </span>
            </div>
          </div>
        </div>
        """)

        # Topic Breakdown
        st.markdown("##### Topic-Wise Mastery Quotient")
        weak_topics = []
        for t, stat in topic_stats.items():
            t_pct = int(stat["correct"] / stat["total"] * 100)
            is_weak = t_pct < 60
            if is_weak:
                weak_topics.append(t)
            st.html(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 14px;background:#f8fafc;border-radius:10px;margin-bottom:8px">
              <span style="font-weight:700;font-size:13.5px">{t}</span>
              <div style="display:flex;align-items:center;gap:12px">
                <span style="font-weight:700;font-size:14px;color:{'#10b981' if not is_weak else '#e11d48'}">{t_pct}% {'✓' if not is_weak else '⚠'}</span>
              </div>
            </div>
            """)

        # Adaptive Feedback
        if weak_topics:
            weak_str = ", ".join(weak_topics)
            st.html(f"""
            <div class="rx-card" style="background:#fff1f2;border:1.5px solid #fda4af;margin-top:14px">
              <b style="color:#be123c;font-size:14px">💡 AI ADAPTIVE RECOMMENDATION:</b>
              <p style="color:#9f1239;font-size:13.5px;margin:6px 0 0;line-height:1.5">
                Focus on <b>{esc(weak_str)}</b>. Your personalized roadmap has been automatically flagged to reinforce these concepts before advanced machine learning topics.
              </p>
            </div>
            """)
        else:
            st.success("🎉 Outstanding performance! All foundational topics in this track meet proficiency standards.")


# ============================================================
# PAGE: PORTFOLIO PROJECTS
# ============================================================
def page_projects():
    require_profile()
    name, _, _, _, _ = current_career()

    st.subheader(f"💼 Industry-Standard Portfolio Projects for {name}")
    st.caption("Curated, production-grade project blueprints designed to demonstrate end-to-end technical execution.")

    projs = CAREER_PROJECTS.get(name, CAREER_PROJECTS.get("ML Engineer", []))

    for idx, p in enumerate(projs):
        pills = "".join(f'<span class="rx-pill rx-pill-blue">{esc(s)}</span>' for s in p["stack"])
        delivs = "".join(f'<li>{esc(d)}</li>' for d in p["deliverables"])
        st.html(f"""
        <div class="rx-card" style="border-left:5px solid #4f46e5;margin-bottom:18px">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <span style="font-size:12px;font-weight:700;color:#6366f1;text-transform:uppercase">{p['tier']}</span>
            <span style="background:#e0e7ff;color:#4338ca;padding:4px 10px;border-radius:8px;font-weight:700;font-size:11.5px">{p['badge']}</span>
          </div>
          <h3 style="font-size:19px;margin:0 0 8px">{esc(p['title'])}</h3>
          <p style="color:#475569;font-size:14px;line-height:1.6;margin-bottom:12px">{esc(p['desc'])}</p>
          <div style="margin-bottom:12px"><b>Tech Stack:</b> {pills}</div>
          <div style="margin-bottom:12px">
            <b>Core Technical Deliverables:</b>
            <ul style="margin:6px 0 0 18px;color:#334155;font-size:13.5px;line-height:1.5">{delivs}</ul>
          </div>
          <div style="background:#f1f5f9;padding:10px 14px;border-radius:10px;font-size:12.5px;color:#334155">
            <b>🎯 Portfolio Impact:</b> {esc(p['impact'])}
          </div>
        </div>
        """)


# ============================================================
# PAGE: RESUME BUILDER & ATS OPTIMIZER
# ============================================================
def page_resume():
    require_profile()
    profile = st.session_state.profile
    name, _, score, missing, _ = current_career()

    st.subheader("📄 ATS Resume Optimizer")
    st.caption("AI-generated professional summaries and skill bullet points formatted for recruiter screening.")

    summary_text = (
        f"Aspiring {name} with academic background in {profile['education']} ({profile['specialization']}) "
        f"and validated expertise in {', '.join(profile['skills'][:5])}. Strong foundation in algorithmic problem solving, "
        f"data pipeline development, and machine learning architectures with a track match score of {score:.0f}%."
    )

    st.markdown("##### 📝 Tailored Professional Summary")
    st.text_area("Copyable Summary for LinkedIn / CV", value=summary_text, height=120)

    st.markdown("##### 🎯 Targeted Skill Bullets")
    bullets = "\n".join([f"• Engineered scalable solutions using {s} with focus on performance and reliability." for s in profile["skills"][:4]])
    st.text_area("Core Competencies & Achievements", value=bullets, height=140)

    st.info("💡 Tip: Tailor each application by ensuring keywords from the target job description match your listed skills.")


# ============================================================
# PAGE: PROGRESS & ANALYTICS
# ============================================================
def page_progress():
    require_profile()
    profile = st.session_state.profile
    recs = normalize_recommendations(st.session_state.recommendations)[:5]
    name, _, score, missing, roadmap = current_career()
    done, total = progress_for(name, roadmap)

    readiness = calculate_career_readiness(profile, score, done, total)

    st.subheader("📊 Progress & Learning Analytics")
    st.caption("Track milestone velocity, study streak consistency, and multidimensional career readiness.")

    a1, a2 = st.columns([1, 1.2], gap="large")

    with a1:
        st.markdown("##### 🏆 Placement Readiness Breakdown")
        fig_gauge = go_plotly.Figure(go_plotly.Indicator(
            mode="gauge+number",
            value=readiness["overall"],
            title={"text": "Career Readiness Index", "font": {"size": 18, "family": "Sora"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#4f46e5"},
                "steps": [
                    {"range": [0, 50], "color": "#fee2e2"},
                    {"range": [50, 75], "color": "#fef3c7"},
                    {"range": [75, 100], "color": "#dcfce7"},
                ],
                "threshold": {"line": {"color": "#10b981", "width": 4}, "thickness": 0.75, "value": 85},
            },
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with a2:
        st.markdown("##### 📈 Weekly Learning Velocity")
        df_velocity = pd.DataFrame({
            "Week": ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"],
            "Study Hours": [6.5, 8.0, 11.5, 9.0, 14.0, 12.5],
        })
        fig_vel = px.line(df_velocity, x="Week", y="Study Hours", markers=True,
                          title="Weekly Learning Hours (Simulated)")
        fig_vel.update_traces(line_color="#4f46e5", line_width=3, marker_size=8)
        fig_vel.update_layout(height=260, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_vel, use_container_width=True)

    st.markdown("##### 🎯 Multi-Path Match Score Comparison")
    df_compare = pd.DataFrame({
        "Career Path": [get_career_name(i) for i in recs],
        "Match Score (%)": [get_score(get_career_result(i)) for i in recs],
    })
    fig_bar = px.bar(df_compare, x="Career Path", y="Match Score (%)", color="Match Score (%)",
                     color_continuous_scale="Blues", text="Match Score (%)")
    fig_bar.update_layout(height=280, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)


# ============================================================
# PAGE: LEARNING RESOURCES (COLORFUL BLOCKS)
# ============================================================
def page_resources():
    require_profile()
    name, _, _, missing, roadmap = current_career()

    st.subheader("📚 Curated Learning Resources")
    st.caption(f"Verified tutorials and official documentation for skills required in {name}.")

    seen = {}
    for t in (missing + roadmap):
        cleaned = str(t).strip()
        key = cleaned.lower()
        if key not in seen:
            seen[key] = cleaned
        elif cleaned[0].isupper() and not seen[key][0].isupper():
            seen[key] = cleaned
    topics = list(seen.values())

    f1, f2 = st.columns([3, 1])
    with f1:
        search_kw = st.text_input("Search resources", placeholder="🔍 Filter resources by keyword...", label_visibility="collapsed")
    with f2:
        all_tags = sorted(list(set(get_topic_meta(t, 0)[1] for t in topics)))
        sel_cat = st.selectbox("Category", ["All Categories"] + all_tags, label_visibility="collapsed")

    filtered = []
    for t in topics:
        ico, tag = get_topic_meta(t, 0)
        title, _ = resource_for(t)
        kw = search_kw.lower().strip()
        match_kw = (not kw) or (kw in t.lower() or kw in title.lower() or kw in tag.lower())
        match_cat = (sel_cat == "All Categories") or (tag == sel_cat)
        if match_kw and match_cat:
            filtered.append(t)

    if not filtered:
        st.info("No learning resources match your current filter.")
    else:
        left_cards = []
        right_cards = []
        for i, topic in enumerate(filtered):
            title, url = resource_for(topic)
            block = render_color_block(topic, title, url, i)
            if i % 2 == 0:
                left_cards.append(block)
            else:
                right_cards.append(block)

        cols = st.columns(2, gap="large")
        with cols[0]:
            card_html("".join(left_cards))
        with cols[1]:
            card_html("".join(right_cards))

    st.markdown("##### 🌐 General Self-Study Platforms")
    platforms = [
        ("NPTEL", "Free video lectures & certifications by IITs / IISc", "https://nptel.ac.in", "🎓", "Certification"),
        ("freeCodeCamp", "Interactive coding curriculum & verified certs", "https://www.freecodecamp.org", "💻", "Interactive"),
        ("roadmap.sh", "Community-driven visual developer roadmaps", "https://roadmap.sh", "🗺️", "Roadmaps"),
    ]
    g = st.columns(3, gap="medium")
    for idx, (col, (t, sub, u, ico, tag)) in enumerate(zip(g, platforms)):
        with col:
            card_html(render_color_block(t, sub, u, idx + len(topics), custom_tag=tag, custom_ico=ico))


# ============================================================
# PAGE: SETTINGS & PREFERENCES
# ============================================================
def page_settings():
    st.subheader("⚙️ Platform Settings")
    st.caption("Manage session data, career profile parameters, and export your study reports.")

    s1, s2 = st.columns(2, gap="large")

    with s1:
        st.markdown("##### 💾 Career Plan Export")
        if st.session_state.profile:
            profile_data = {
                "profile": st.session_state.profile,
                "selected_career": get_career_name(st.session_state.selected_career),
                "generated_at": datetime.now().isoformat(),
            }
            st.download_button(
                "📥 Export Career Roadmap (JSON)",
                data=json.dumps(profile_data, indent=2),
                file_name="roadmapx_career_profile.json",
                mime="application/json",
            )
        else:
            st.info("Create a profile to enable career roadmap export.")

    with s2:
        st.markdown("##### 🔄 Reset Data")
        st.warning("Resetting will clear your current profile, active matches, and roadmap progress.")
        if st.button("Reset Entire Profile", type="secondary"):
            reset_profile()


# ============================================================
# ROUTER
# ============================================================
render_nav()

ROUTER = {
    "home": page_home,
    "dashboard": page_dashboard,
    "recommendations": page_recommendations,
    "multipath": page_multipath,
    "gaps": page_gaps,
    "roadmap": page_roadmap,
    "assessments": page_assessments,
    "projects": page_projects,
    "resume": page_resume,
    "progress": page_progress,
    "resources": page_resources,
    "settings": page_settings,
}

ROUTER.get(st.session_state.page, page_home)()

card_html("""
<div style="text-align:center;color:#94a3b8;font-size:12.5px;padding:32px 0 10px">
  <b>RoadmapX AI</b> · Enterprise-Grade AI Career Roadmap & Placement Acceleration System
</div>
""")
