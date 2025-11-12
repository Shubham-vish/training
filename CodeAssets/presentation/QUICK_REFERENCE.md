# 🎤 Quick Reference Card - Demo Day

## ⏱️ Critical Timing
- **Total:** 30 minutes
- **Must-hit:** 28-30 min finish
- **Demo:** 4-5 min max
- **Code:** 3 min walkthrough

---

## 🎯 Must-Show Code Pieces

### **1. State Schema (45 sec)**
```python
class ContentCreationState(TypedDict):
    topic: str
    content_outline: str
    research_queries: List[str]
    script: str
    quality_score: float
    hashtags: List[str]
```
**Say:** "This flows through every node. Simple, typed, automatic."

---

### **2. Node Pattern (45 sec)**
```python
def planner_node(state: ContentCreationState):
    llm_client = get_llm_client()
    content_outline = llm_client.generate_response(...)
    return {"content_outline": content_outline}
```
**Say:** "Get state, call LLM, return update. LangGraph handles the rest."

---

### **3. Conditional Routing (45 sec)** ⭐ **MOST IMPORTANT**
```python
workflow.add_conditional_edges(
    "reflection", should_revise,
    {"research_planner": "research_planner",
     "hashtag_generator": "hashtag_generator"}
)

def should_revise(state):
    return "research_planner" if state.quality_score < 7.0 
           else "hashtag_generator"
```
**Say:** "Quality below 7? Loop back. Above 7? Proceed. Automatic quality control in 10 lines."

---

## 🚨 Emergency Shortcuts

**If running behind:**
- Skip "Beyond Content Creation" (-45 sec)
- Cut learning path to bullet points (-30 sec)
- Shorter Q&A (-2 min)

**If demo breaks:**
- Show pre-recorded output screenshots
- Jump straight to code walkthrough
- Say: "I ran this 10 minutes ago - here's the output"

---

## 💡 Key Phrases to Memorize

### **Opening:**
> "In 4 months, I grew to 8,000 followers with a fully automated Instagram system. Today, I'm showing you the core engine."

### **LangGraph Analogy:**
> "LangGraph is like an interconnected system - components connect, data flows, conditions route."

### **Conditional Routing:**
> "This is the magic - quality score triggers automatic routing. Loop back or proceed. System-level control."

### **Closing:**
> "Multi-agent systems are powerful - you just saw proof. Specialists beat generalists. Start with the demo code!"

---

## ✅ Pre-Stage Checklist (2 min before)

**Technical:**
- [ ] VS Code open at demo_project folder
- [ ] Terminal ready: `cd /home/shubham/training/demo_project`
- [ ] Font sizes: VS Code 16+, Terminal 14+
- [ ] Close unnecessary tabs
- [ ] Slides ready in browser

**Mental:**
- [ ] Deep breath
- [ ] Water ready
- [ ] Positive mindset
- [ ] Timer started (30 min)

---

## 🎯 Success = These 3 Things

1. ✅ **Live demo runs** (even if imperfect)
2. ✅ **Show conditional routing code** (the "magic")
3. ✅ **Finish in 28-30 min** (with Q&A buffer)

Everything else is bonus!

---

## 🚀 Opening Line (Memorize This)

> "Good evening! Four months ago, I was overwhelmed with content creation. Today, I have an AI system that posts 2 Instagram reels daily while I sleep - and grew to 8,000 followers. Let me show you how to build this."

**Pause. Smile. Begin.**

---

## 📞 Backup Contact (If Tech Fails)

- Screenshots folder ready
- Pre-recorded demo video (if available)
- Slide deck works standalone
- Can explain code without running it

---

## 🎬 Last Reminder

**You've got this!**
- You built the system
- You know the code
- You have a real success story
- Just show what works!

**Energy high, delivery fast, code clear.** 🚀
