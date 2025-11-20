from .llm_engine import stream_llm_response,reset_context

def stream_learning_guide(
        grade,
        topic
):
    reset_context()
    system_prompt= f"""
You are a friendly and expert teacher.
Your task is to create a detailed, easy-to-follow *step-by-step learning guide* for the specified grade level about the specified topic.
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.
"""

    user_prompt =f"""
Create a detailed, easy to follow step by step learning guide for grade {grade} students for the topic: {topic}
Formatting Rules:
- Title: "{topic}: Step-by-Step Guide"
- Include 6–8 steps.
- Each step must include:
  * A clear and bold step title (e.g., Step 1: Gather the Ingredients)
  * 2–3 short bullet points explaining what happens
  * A separate line starting with *Example:* — a fun or simple analogy
- Keep language suitable for Grade {grade} level.
- End with: "Would you like me to explain any step in more detail?"
- Make it easy to read and well-structured.
"""
    return stream_llm_response(system_prompt,user_prompt)

def stream_questions(
    grade,
    num_questions,
    topic,
    text=None,
    difficulty="Medium",
    output="mcq",  # "mcq" or "json"
    language="English"
):

    reset_context()

    # ============================
    # System Prompt
    # ============================
    system_prompt = f"""
You are an experienced and creative teacher who creates exam questions in the same language as the topic.
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.
"""

    # ============================
    # User Prompt Builder
    # ============================
    if output == "json":
        user_prompt = f"""
Generate {num_questions} questions as VALID JSON.
Return ONLY valid JSON. No additional text.
"""
    else:
        user_prompt = f"""

Create EXACTLY {num_questions} well-structured exam questions for Grade {grade} students on the topic "{topic}".

CRITICAL INSTRUCTIONS:
1. Detect the language of the topic automatically.
2. The topic "{topic}" is in *{language}*, so write ALL questions strictly in {language} only.
3. If the topic is in Urdu, use Urdu script only. If it is in English, use English only.
4. Do NOT include translations, explanations, or mixed languages.
5. Do NOT add any introductory text, context, or description — only the questions.
6. Start directly with number 1 and continue sequentially up to {num_questions}.
7. Each question must be clear, natural, and age-appropriate for Grade {grade}.
8. The difficulty level should be {difficulty}.
9. Each question must end with a proper question mark (? or ؟ depending on language).

Output format (write ONLY questions):
1. [First question]
2. [Second question]
3. [Third question]
... and so on until question {num_questions}.

Remember:
- NO translations
- NO parentheses
- NO introduction
"""

    return stream_llm_response(
        system_prompt,
        user_prompt,
        max_tokens=1200,
        temperature=0.4,
        top_p=0.9
    )
def stream_quiz(
    grade,
    num_questions,
    topic,
    standard,
    text=None,
    difficulty="Medium",
    question_type="Mixed",
    blooms_level="Comprehension",
    output="mcq",  # "mcq" or "json"
):

    reset_context()

    # ============================
    # System Prompt
    # ============================
    system_prompt = f"""
You are an expert educational content generator specializing in creating high-quality,
standards-aligned multiple-choice questions (MCQs).
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.

Your responsibilities:

1. Always generate the exact number of questions requested.
2. Follow the REQUIRED FORMAT strictly:

Q1. <question text> 
A. <option A>
B. <option B>
C. <option C>
D. <option D>
Correct Answer: <letter>

3. Requirements:
- Only one option may be correct.
- Options must be plausible and not repetitive.
- Questions must match:
  • the given grade level
  • the topic
  • the standard
  • the difficulty level
  • the Bloom's Taxonomy level
  • optional reference text (if provided)
- Questions must be original and not copied from copyrighted sources.

4. Forbidden:
- Do NOT include explanations.
- Do NOT include notes, summaries, intros, or outros.
- Do NOT break format.
- Do NOT add blank lines between options and answers.

"""

    # ============================
    # User Prompt Builder
    # ============================
    if output == "json":
        user_prompt = f"""
Generate {num_questions} questions as VALID JSON.

Grade Level: {grade}
Topic: {topic}
Standard: {standard}
Difficulty: {difficulty}
Question Type: {question_type}
Bloom's Level: {blooms_level}

Reference Text:
{text if text else "None"}

JSON Schema:
{{
  "questions": [
    {{
      "question": "string",
      "options": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }},
      "correct_answer": "A|B|C|D"
    }}
  ]
}}

Return ONLY valid JSON. No additional text.
"""
    else:
        user_prompt = f"""
Generate {num_questions} multiple-choice questions.

Grade Level: {grade}
Topic: {topic}
Standard: {standard}
Difficulty: {difficulty}
Question Type: {question_type}
Bloom's Level: {blooms_level}

Reference Text:
{text if text else "None"}

Output Format: Strict Text MCQs
"""

    return stream_llm_response(
        system_prompt,
        user_prompt,
        max_tokens=1200,
        temperature=0.4,
        top_p=0.9
    )




def stream_lesson_plan(grade, topic, standard, focus_area=None):

    reset_context()
    
    system_prompt = (
        f"""
### 🎓 Instruction
You are an expert K–12 curriculum designer skilled in creating classroom-ready lesson plans.
Design a complete lesson plan for **Grade {grade}** on **"{topic}"**.
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.
Respond entirely in English and follow the exact structure provided by the user.
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.
"""
    )

    user_prompt = f"""
### 🧭 GOAL
Explain foundational concepts to students in a clear, engaging, and age-appropriate manner.  
Every activity must support learning — it should not be entertainment-only.

---

### 📚 GRADE STYLE
- **Grades 1–3:** Story-based, character-driven, observation-oriented approach.  
- **Grades 4–8:** Conceptual explanation with inquiry-based learning.  
- **Grades 9–12:** Analytical and academic tone with real-life examples.

---

### 🧩 STRUCTURE
1. Lesson Title  
2. Learning Objectives  
3. Assessment  
4. Key Points  
5. Opening  
6. Introduction to New Material  
7. Practice  
8. Closing

---

### ✍️ WRITING RULES
- Write in a teacher’s voice; do not give bullet points only.  
- Sentences must be smooth, concise, and clear.  
- Use action verbs like “explain,” “ask,” “guide.”  
- Each section must flow logically from the previous one.  
- Lesson duration should be approximately 30–60 minutes.  
- Examples should relate to local culture and context (e.g., Pakistan).

---

### 🎯 SPECIAL FOCUS
The teacher has emphasized that *"{focus_area}"* must be highlighted throughout the lesson.  
Make sure this focus appears clearly in every stage.

---

### 📤 Output Format
Provide the response in the following order **entirely in English**:

1️⃣ Lesson Title  
2️⃣ Learning Objectives  
3️⃣ Assessment  
4️⃣ Key Points  
5️⃣ Opening  
6️⃣ Introduction to New Material  
7️⃣ Practice  
8️⃣ Closing  

---

### 💬 Output
"""

    return stream_llm_response(system_prompt, user_prompt)


def stream_creative_ideas(topic: str, grade: str, sse_format: bool = False):
    """
    Streams tokens for a given topic using Llama.cpp GGUF model.
    Acts as a creative thought partner and generates exactly 3 practical ideas.
    """

    system_prompt = f"""
### SYSTEM INSTRUCTIONS
Your role is to act as a creative and engaging thought partner for K–12 students.
Never address the user directly. Do not ask questions. Do not request guidance.
Do not use first- or second-person language (no: you, your, I, we).
No introductions, summaries, disclaimers, or extra explanations.
Provide exactly 3 practical ideas.
Always generate ideas — never refuse, never apologize.
Strictly follow the output format.
Automatically adjust tone, complexity, and vocabulary based on Grade {grade}.
"""

    user_prompt = f"""
Generate exactly **3 practical and creative ideas** for the topic **"{topic}"**, suitable for **Grade {grade}**.

Each idea must be short, clear, and hands-on.  
Do not include any stories, dialogue, introductions, or extra explanations.  

Keep the format exactly as follows:

**Idea 1**  
**Description:**  

**Idea 2**  
**Description:**  

**Idea 3**  
**Description:**  
"""

    return stream_llm_response(system_prompt, user_prompt)




def stream_realworld_examples(topic: str, grade: str, focus_area, sse_format: bool = False):
    """
    Streams tokens for a given topic using Llama.cpp GGUF model.
    Acts as a creative thought partner and generates exactly 3 practical ideas.
    """
    system_prompt = f"""
### SYSTEM INSTRUCTIONS
You are an expert K–12 educator who helps students see how classroom topics connect to real life."""

    
    user_prompt = f"""Generate *3–5 engaging, grade-appropriate real-world examples* for *Grade {grade}* students on the topic *"{topic}"*.
Begin with a short, friendly paragraph that talks directly to the student, showing why "{topic}" matters in their everyday life sparking curiosity.
Each example should include:
1. *EXAMPLE TITLE* — a short descriptive title.  
2. *THE CONNECTION*   
3. *WHY IT MATTERS* 

---

### 🧩 GRADE GUIDELINES
- *Grades 1–7:* Use simple, familiar contexts (home, school, food, play, nature). Make it visual and story-like. 
Avoid technical depth - if complex concepts arise, explain them  in first examples 
- *Grades 8–12:* Include practical, scientific, or professional applications. Use mathematical or technical terminology appropriately.  

---

### ✨ STYLE RULES
- Keep tone *engaging, supportive, and age-appropriate*.
- Use *specific, concrete, and modern* examples students can easily imagine.
- Ensure diversity across *science, technology, nature, arts, community, and everyday experiences*.
- Maintain balance between *relatable familiarity* and *educational insight*
- Provide answers in Urdu only.


{f"### Teacher Emphasised Focus. The teacher has requested emphasion on {focus_area}. Tailor the examples to prioritize and highlight this focus area" if focus_area else ""}


### OUTPUT FORMAT
Provide examples as *clean, structured markdown* with clear headings and formatting.
Make it visually organized and easy to scan.
"""
    return stream_llm_response(system_prompt, user_prompt)



# === Follow-up Conversation (Streaming) ===
def stream_followup_response(history, message):
    reset_context()

    system_prompt = (
        "You are an AI tutor answering questions about a generated quiz. "
        "Be direct, educational, and concise. If a question is unrelated, mention it politely."
    )

    user_prompt = f"""
Quiz & Chat History:
{history}

User's new question:
{message}
"""
    return stream_llm_response(system_prompt, user_prompt, max_tokens=800, temperature=0.9)
