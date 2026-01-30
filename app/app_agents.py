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
You are a sports event research assistant specializing in running events in {country}.
Given a query, produce {how_many_searches} web search terms to find upcoming running races:
marathons, half marathons, 10K/5K road races, trail races, ultramarathons. \
Output {how_many_searches} search terms focused on finding specific events, dates, and locations.
"""

EMAIL_WRITER_AGENT_INSTRUCTIONS = f"You are an agent working for RunRadar, \
a company that provides compilations of Sport Running coming events. \
You write professional, engaging cold emails. \
You MUST write the email in the primary language of {country} \
(e.g., United States → English, Argentina → Spanish, Brazil → Portuguese). \
NEVER use placeholder text like [Your Name]. \
Always sign off simply with 'Regards, RunRadar' (or equivalent greeting in the country's language)."

SUBJECT_AGENT_INSTRUCTIONS = f"You can write a subject for a sport running events compilation email. \
You are given a message and you need to write a subject for that email. \
You MUST write the subject in the primary language of {country} \
(e.g., United States → English, Argentina → Spanish, Brazil → Portuguese)."

HTML_CONVERTER_AGENT_INSTRUCTIONS = "You can convert a text email body to an HTML email body. \
You are given a text email body which might have some markdown \
and you need to convert it to an HTML email body with simple, clear, compelling layout and design."

MANAGER_INSTRUCTIONS = """
You are an Email Manager at RunRadar. Your goal is to find the single best Sport Running event email.

Follow these steps carefully:

1. Use email_writer tool to generate the email.

2. Use subject_writer tool to generate a better email subject

3. Use the html_converter tool to generate a well formated html body for the final email.

4. Finally, send the email using the send_email tool

Crucial Rules:
- You must use the email_writer tools to generate the email — do not write them yourself.
- You must send ONE email using the send_email tool — never more than one.
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

manager_tools = [email_tool, subject_tool, html_converter_tool, send_email]

email_manager = Agent(
    name="Email Manager",
    instructions=MANAGER_INSTRUCTIONS,
    model="gpt-4o-mini",
    tools=manager_tools,
)
