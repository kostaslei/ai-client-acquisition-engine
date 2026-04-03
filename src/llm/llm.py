from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(business_name, website):
    prompt = f"""You are a B2B sales analyst. You will receive scraped website content and produce a structured JSON output.

BUSINESS: {business_name}
WEBSITE CONTENT:
{website}

---

TASK: Analyze the website content and return ONLY the JSON below. No extra text.

RULES (read carefully before answering):

1. ONLY use information explicitly visible in the content above.
2. If something is unclear or not mentioned, write "not mentioned" — do NOT guess.
3. Ignore all slogans, taglines, and marketing claims (e.g. "we are the best", "award-winning").
4. Every field must be grounded in something you can point to in the text.

---

Return this exact JSON:

{{
  "business_analysis": {{
    "what_they_do": "1-2 sentences max. Only what is explicitly stated. No interpretation.",
    "who_they_serve": "Explicitly mentioned clients or industries only. If none mentioned: 'not mentioned'.",
    "concrete_offerings": ["List only specific products/services named. No generic descriptions."],
    "proof_points": ["Specific case studies, client names, metrics, or examples mentioned. If none: leave empty array."]
  }},
  "friction_points": [
    {{
      "observation": "One specific thing that is unclear or missing from the site.",
      "why_it_matters": "One sentence on the business impact of this gap.",
      "anchor": "The exact phrase or section from the content that led to this observation."
    }}
  ],
  "outreach_message": "Write a 3-4 sentence cold outreach message. Rules: (1) Reference one specific thing from the site. (2) Point out one friction. (3) Suggest one concrete idea. (4) No praise, no 'I noticed', no 'just wanted to reach out'. Write like a human, not a template."
}}

FRICTION RULES:
- Maximum 2 friction points.
- Each friction must reference a real item from the content (use the 'anchor' field).
- If you cannot find a clear friction, return: [{{"observation": "No clear friction found", "why_it_matters": "", "anchor": ""}}]
- Do NOT invent problems that aren't grounded in what's actually on the site.

OUTREACH RULES:
- Do NOT use: "I noticed", "it seems", "you guys", "great", "awesome", "happy to", "let me know", "I see"
- Do NOT be generic and remove generic phrases
- Do NOT be vague or very polite
- Be a confident b2b sales person
- End with a human tone like "Happy to share a few ideas if helpful."
- Begin with a confident human tone like "Hey — quick note after checking out.."
- Keep it under 5 sentences
- include 1 specific observation
- Sound like a real human
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user", "content": prompt}
        ]
    )
    return response.choices[0].message.content