from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# -----------------------------------
# SPLIT LONG TRANSCRIPTS
# -----------------------------------

def chunk_text(
    text,
    chunk_size=5000
):

    chunks = []

    for i in range(
        0,
        len(text),
        chunk_size
    ):

        chunks.append(
            text[i:i + chunk_size]
        )

    return chunks


# -----------------------------------
# ANALYZE SINGLE CHUNK
# -----------------------------------

def analyze_chunk(chunk):

    system_prompt = """
You are an advanced AI Meeting Intelligence and Video Conversation Analysis System.

Your task is to deeply analyze meeting/video transcripts and extract operational, technical, and business intelligence.

IMPORTANT RULES:
- Return ONLY valid raw JSON
- Do NOT use markdown
- Do NOT wrap response in ```json
- Use professional language
- Avoid duplicate information
- Extract meaningful engineering and business insights
- Infer logical action items from discussions
- Preserve important context
"""

    user_prompt = f"""
Analyze this transcript exhaustively.

Do not summarize briefly.

Extract every technical detail, business discussion, architecture decision,
coding discussion, deployment topic, API discussion, testing discussion,
database discussion, AI discussion, performance concern, security concern,
future plan, blocker, and action item.

When participants explain a concept, include the explanation in detail.
Do not omit repetitive information if it contributes to understanding.

Your goal:
- understand discussions
- detect technical conversations
- detect business conversations
- detect plans
- detect engineering tasks
- detect deployment discussions
- detect frontend/backend/database/API discussions
- detect AI discussions
- detect blockers and risks
- detect future plans
- detect important decisions
- detect questions and answers

IMPORTANT ACTION ITEM RULES:

- Extract BOTH explicit and implied tasks
- Convert discussions into actionable tasks when logically appropriate
- If participants discuss implementing, improving, fixing, creating, integrating, deploying, optimizing, testing, designing, scaling, or planning something, convert it into an action item
- Never return empty action_items if meaningful work was discussed
- Every action item MUST contain:
  - task
  - priority
  - owner
  - status
- status should default to "Pending"

Return ONLY valid JSON.

Required JSON structure:

{{
  "important_points": [],

  "detailed_discussions": [
    {{
      "topic": "",
      "details": ""
    }}
  ],

  "technical_topics_discussed": [],

  "business_topics_discussed": [],

  "frontend_discussions": [],

  "backend_discussions": [],

  "database_discussions": [],

  "api_discussions": [],

  "deployment_discussions": [],

  "security_discussions": [],

  "testing_discussions": [],

  "ai_or_ml_discussions": [],

  "performance_scalability_discussions": [],

  "action_items": [
    {{
      "task": "",
      "priority": "High"
    }}
  ],

  "decisions_made": [],

  "questions_and_answers": [
    {{
      "question": "",
      "answer": ""
    }}
  ],

  "problems_or_risks": [],

  "future_plans": [],

  "important_notes": [],

  "next_steps": []
}}

Transcript Chunk:
{chunk}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.3
    )

    content = (
        response
        .choices[0]
        .message.content
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Invalid JSON received from analyze_chunk:")
        print(content)
        raise


# -----------------------------------
# FINAL REPORT GENERATION
# -----------------------------------

def generate_final_report(

    transcript,

    chunk_results
):

    system_prompt = """
You are an enterprise AI meeting intelligence engine.

You combine chunk analyses into ONE final complete meeting intelligence report.

Preserve:
- chronology
- engineering discussions
- business discussions
- technical depth
- architecture
- action items
- decisions
- risks
- future plans
"""

    user_prompt = f"""
Generate ONE final enterprise meeting intelligence report.

Requirements:
- Do not summarize briefly.
- Capture every important discussion.
- Explain each technical topic in detail.
- Preserve chronological order.
- Include all frontend, backend, database, API, deployment and AI discussions.
- Produce comprehensive action items.
- Include every decision made.
- Include every risk and blocker.
- Expand the meeting overview into multiple paragraphs.
- The overall_summary should be detailed and at least 500 words when the transcript contains sufficient information.
- Do not omit information simply to make the response shorter.

IMPORTANT:
- Merge duplicate information
- Preserve all major discussions
- Generate rich detailed summaries
- Keep action items detailed and useful

Return ONLY valid JSON.

Required JSON structure:

{{
  "meeting_overview": {{
    "title": "",
    "main_objective": "",
    "meeting_type": "",
    "overall_summary": ""
  }},

  "participants_detected": [],

  "chronological_flow": [
    {{
      "meeting_phase": "",
      "discussion": "",
      "technical_topics": [],
      "decisions": [],
      "action_items": []
    }}
  ],

  "important_points": [
     {{
        "title": "",
        "description": ""
      }}
  ],

  "detailed_discussions": [],

  "technical_topics_discussed": [],

  "business_topics_discussed": [],

  "frontend_discussions": [],

  "backend_discussions": [],

  "database_discussions": [],

  "api_discussions": [],

  "deployment_discussions": [],

  "security_discussions": [],

  "testing_discussions": [],

  "ai_or_ml_discussions": [],

  "performance_scalability_discussions": [],

  "action_items": [],

  "decisions_made": [],

  "questions_and_answers": [],

  "problems_or_risks": [],

  "future_plans": [],

  "important_notes": [],

  "next_steps": [],

  "final_conclusion": ""
}}

FULL TRANSCRIPT:
{transcript}

CHUNK ANALYSIS:
{json.dumps(chunk_results)}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": user_prompt
            }
        ],

        temperature=0.3
    )

    content = (
        response
        .choices[0]
        .message.content
    )

    content = (
        content
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("Invalid JSON received:")
        print(content)
        raise


# -----------------------------------
# MAIN FUNCTION
# -----------------------------------

def generate_summary(
    transcript
):
    try:

        # SPLIT LARGE TRANSCRIPT

        chunks = chunk_text(
            transcript
        )

        chunk_results = []

        # ANALYZE EACH CHUNK

        for chunk in chunks:

            result = analyze_chunk(
                chunk
            )

            chunk_results.append(
                result
            )

        # GENERATE FINAL REPORT

        final_report = (
            generate_final_report(

                transcript,

                chunk_results
            )
        )

        return final_report

    except Exception as e:

        print(str(e))
        return {

            "meeting_overview": {},

            "participants_detected": [],

            "chronological_flow": [],

            "important_points": [],

            "detailed_discussions": [],

            "technical_topics_discussed": [],

            "business_topics_discussed": [],

            "frontend_discussions": [],

            "backend_discussions": [],

            "database_discussions": [],

            "api_discussions": [],

            "deployment_discussions": [],

            "security_discussions": [],

            "testing_discussions": [],

            "ai_or_ml_discussions": [],

            "performance_scalability_discussions": [],

            "action_items": [],

            "decisions_made": [],

            "questions_and_answers": [],

            "problems_or_risks": [],

            "future_plans": [],

            "important_notes": [],

            "next_steps": [],

            "final_conclusion": ""
        }
