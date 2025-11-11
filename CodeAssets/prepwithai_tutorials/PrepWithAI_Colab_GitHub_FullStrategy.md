
# 🧠 PrepWithAI Notebook Sharing Strategy

This document outlines the strategy for sharing PrepWithAI AI Agent content using GitHub and Google Colab.

---

## ✅ Use Case Summary

| Use Case                         | Strategy                           | Colab Experience      |
|----------------------------------|------------------------------------|------------------------|
| Single Notebook Only            | Use **direct GitHub → Colab link** | Instant open + run     |
| Multiple Files (agents/utils)   | **`git clone` inside Colab**       | Structured, scalable   |
| Full Courses or Series          | GitHub repo + Colab launch buttons | Professional delivery  |

---

## 📁 Recommended GitHub Repo Structure

```
prepwithai_tutorials/
├── agents/
│   ├── content_planner.py
│   └── research_agent.py
├── utils/
│   └── logger.py
├── notebooks/
│   ├── content_agent_demo.ipynb
│   └── ai_team_architecture.ipynb
├── datasets/
│   └── example.csv
├── README.md
```

---

## 📌 Single Notebook Sharing (Direct Colab Link)

Use this structure when you’re only sharing a single `.ipynb` file and no other modules:

### Format:
```
https://colab.research.google.com/github/<username>/<repo>/blob/main/<path-to-notebook>.ipynb
```

### Example:
```
https://colab.research.google.com/github/Shubham-vish/prepwithai_tutorials/blob/main/notebooks/content_agent_demo.ipynb
```

Embed this in:
- Instagram Reels/Comments
- README.md
- Course pages

---

## 📦 Multi-file Project (Using `git clone` in Notebooks)

Use this when your notebook needs supporting files like custom Python modules (`agents/`, `utils/`, etc).

### Paste this block at the start of your notebook:

```python
# Step 1: Clone your GitHub repo
!git clone https://github.com/Shubham-vish/prepwithai_tutorials.git

# Step 2: Add the cloned folder to Python path
import sys
sys.path.append('/content/prepwithai_tutorials')

# Step 3: Import your modules normally
from agents.content_planner import generate_plan
from utils.logger import log_info

# Step 4: Use them
log_info("Running agent...")
generate_plan("AI Reels Automation")
```

---

## 🧾 Markdown Cell to Include in Every Multi-File Notebook

This block should be added as a **Markdown cell** at the top of every notebook using `git clone`, so users understand what's happening.

```markdown
### 📦 This Notebook Uses External Files

To keep things clean, we're using GitHub to store supporting files like:

- Agent scripts (in `/agents/`)
- Utility functions (in `/utils/`)
- Sample data (in `/datasets/`)

When you run the first code cell, it will:

1. Clone the full GitHub repo (one-time)
2. Add it to the Python path
3. Allow you to import and use everything cleanly 🎯

Let’s go 🚀
```

---

## 🪄 Optional: “Open in Colab” Button for README.md

Paste the following markdown in your repo’s README file to add a launch button:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shubham-vish/prepwithai_tutorials/blob/main/notebooks/content_agent_demo.ipynb)
```

---

## 🔒 Future-Proofing & Paid Content (Optional)

- Use private GitHub repos for premium notebooks
- Lock Colab links behind SkillTown purchases
- Use watermarks/headers in shared `.ipynb` for branding
- Auto-update links or repo names using a content script

---

This is the foundation for building a clean, professional, and scalable content system around PrepWithAI.
