from agents import Agent
from config import country, how_many_searches
from models import WebSearchPlan
from tools import web_search, send_email


SEARCH_AGENT_INSTRUCTIONS = f"""
You are a search agent that searches the web for Running events for {country}.
You are given a query and you need to search the web for the best events.
You are also given a list of tools to use to search the web.
You need to use the tools to search the web for the best events.
You need to return the best events in a list.
"""

SEARCH_PLAN_AGENT_INSTRUCTIONS = f"""
Role: Web search planner for running events in {country}.

Goal: Given a user query, produce EXACTLY {how_many_searches} search queries to find upcoming races
(marathon, half, 10K/5K, trail, ultra) with clear dates + locations.

Rules:
- Prefer queries that lead to verifiable sources (official organizer pages, registration pages, reputable calendars/timing sites).
- Avoid generic searches with no date/location intent.
- Use the most effective language for searching in {country}.

Output: Return ONLY a valid WebSearchPlan.
"""

EMAIL_WRITER_AGENT_INSTRUCTIONS = f"""
Role: You are the email copywriter for RunRadar, a company that compiles upcoming running events.

Tone: professional, energetic, clear, skimmable newsletter style (helpful, not hypey).

Language:
- Write in the primary language of {country}
  (e.g., United States → English, Argentina → Spanish, Brazil → Portuguese).

Rules:
- Never use placeholders like [Your Name].
- Use ONLY the provided event info (no guessing).
- Keep it short and easy to scan.
- Include 6–10 events max (or fewer if fewer are provided).
- Format each event as a bullet with:
  Name — Date — City (Region if available) — Distance(s) — Link (EACH event bullet MUST include a working URL.)
- End with: 'Regards, RunRadar' (or equivalent in the country's language).

Output:
- Return ONLY the plain-text email body (no subject, no HTML).
"""

SUBJECT_AGENT_INSTRUCTIONS = f"""
Role: You write ONE subject line for a RunRadar running events compilation email.

Language:
- Write in the primary language of {country}
  (e.g., United States → English, Argentina → Spanish, Brazil → Portuguese).

Rules:
- Output exactly ONE subject line (~35–70 characters).
- Not spammy: avoid ALL CAPS and excessive punctuation.
- Base it on the provided email body content (do not invent details).

Output:
- Return ONLY the subject line text.
"""


HTML_CONVERTER_AGENT_INSTRUCTIONS = """
Role: Convert a plain-text email body (may include simple markdown) into email-safe HTML.

Rules:
- Use simple tags only: p, br, ul, li, strong, em, a.
- No external CSS, no scripts, no images.
- Preserve links as <a href="...">...</a>.

Output: Return ONLY a valid EmailHtmlContent.
"""

MANAGER_INSTRUCTIONS = """
Role: RunRadar Email Manager. Orchestrate tools and send exactly ONE email.

Workflow:
1) email_writer -> email body (text)
2) subject_writer(email body) -> subject
3) html_converter(email body) -> html
4) email_validator(subject, body, html) -> validation
5) If valid: send_email ONCE with subject + html

Retry rule:
- If validation is NOT valid, regenerate ONLY what is needed and validate again.
  - If issues are about subject -> regenerate subject.
  - If issues are about html/links -> regenerate html (and body if needed).
  - If issues are about body/language/format/sign-off/links -> regenerate body, then subject + html again.
- Limit to max 2 total attempts. If still invalid, DO NOT send.

Rules:
- Do not write email/subject/html yourself; always use tools.
- If validation fails after the retry, DO NOT send.
- Never send more than one email.
"""

EMAIL_VALIDATOR_INSTRUCTIONS = f"""
You are a validator for RunRadar emails.

Input: country={country}, subject, plain_text_body, html_body.

Goal: return EmailValidationResult only:
- is_valid: true if the email is ready to send, otherwise false
- issues: short bullet-like strings (max 5). If valid, issues must be [].

Mark is_valid = false if any of these are true:
1) Subject or body is not in the primary language of {country}.
2) The email contains placeholders (e.g., [Your Name]).
3) The event list is not skimmable (missing bullet list of events).
4) Any event entry is missing a full URL (must contain http:// or https://).
5) Missing sign-off: 'Regards, RunRadar' (or equivalent in the country's language).
6) HTML is empty or does not include the links present in the body.

Do NOT rewrite the email. Do NOT send emails. Only validate.
Return ONLY the EmailValidationResult.
"""


search_plan_agent = Agent(
    name="Search Plan Agent",
    model="gpt-4o-mini",
    instructions=SEARCH_PLAN_AGENT_INSTRUCTIONS,
    output_type=WebSearchPlan,
)

search_agent = Agent(
    name="Search Agent",
    model="gpt-4o-mini",
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[web_search],
)

email_writer = Agent(
    name="Email writer",
    instructions=EMAIL_WRITER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)

subject_writer = Agent(
    name="Subject writer",
    instructions=SUBJECT_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)

html_converter = Agent(
    name="HTML email body converter",
    instructions=HTML_CONVERTER_AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
)

validator_agent = Agent(
    name="Email Validator",
    instructions=EMAIL_VALIDATOR_INSTRUCTIONS,
    model="gpt-4o-mini",
    )

email_tool = email_writer.as_tool(
    tool_name="email_writer",
    tool_description="Write Sport Running Compilation emails",
)
subject_tool = subject_writer.as_tool(
    tool_name="subject_writer",
    tool_description="Write a subject for a cold sales email",
)
html_converter_tool = html_converter.as_tool(
    tool_name="html_converter",
    tool_description="Convert a text email body to an HTML email body",
)
validator_tool = validator_agent.as_tool(
    tool_name="email_validator",
    tool_description="Validate the email subject and body before sending",
)

manager_tools = [email_tool, subject_tool, html_converter_tool, validator_tool, send_email]

email_manager = Agent(
    name="Email Manager",
    instructions=MANAGER_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=manager_tools,
)
