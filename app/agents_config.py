from agents import Agent
from models import WebSearchPlan, SearchResult, EmailSubject, EmailBody, EmailHtmlContent, EmailValidationResult
from tools import web_search, send_email
from config import openai_model
from instructions import (
    SEARCH_AGENT_INSTRUCTIONS,
    SEARCH_PLAN_AGENT_INSTRUCTIONS,
    EMAIL_WRITER_AGENT_INSTRUCTIONS,
    SUBJECT_AGENT_INSTRUCTIONS,
    HTML_CONVERTER_AGENT_INSTRUCTIONS,
    MANAGER_INSTRUCTIONS,
    EMAIL_VALIDATOR_INSTRUCTIONS,
    SEARCH_MANAGER_INSTRUCTIONS,
)


search_plan_agent = Agent(
    name="Search Plan Agent",
    model=openai_model,
    instructions=SEARCH_PLAN_AGENT_INSTRUCTIONS,
    output_type=WebSearchPlan,
)

search_agent = Agent(
    name="Search Agent",
    model=openai_model,
    instructions=SEARCH_AGENT_INSTRUCTIONS,
    tools=[web_search],
    output_type=SearchResult,
)

search_plan_tools = search_plan_agent.as_tool(tool_name="search_planner",tool_description="Generate web search plans for running events.")
search_tool = search_agent.as_tool(tool_name="web_searcher",tool_description="Search the web for running events.")

email_writer = Agent(
    name="Email writer",
    instructions=EMAIL_WRITER_AGENT_INSTRUCTIONS,
    model=openai_model,
    output_type=EmailBody,
)

subject_writer = Agent(
    name="Subject writer",
    instructions=SUBJECT_AGENT_INSTRUCTIONS,
    model=openai_model,
    output_type=EmailSubject,
)

html_converter = Agent(
    name="HTML email body converter",
    instructions=HTML_CONVERTER_AGENT_INSTRUCTIONS,
    model=openai_model,
    output_type=EmailHtmlContent,
)

validator_agent = Agent(
    name="Email Validator",
    instructions=EMAIL_VALIDATOR_INSTRUCTIONS,
    model=openai_model,
    output_type=EmailValidationResult,
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

email_manager_tools = [email_tool, subject_tool, html_converter_tool, validator_tool, send_email]

email_manager_agent = Agent(
    name="Email Manager",
    instructions=MANAGER_INSTRUCTIONS,
    model=openai_model,
    tools=email_manager_tools,
)

search_manager_tools = [search_plan_tools, search_tool]

search_manager_agent = Agent(
    name="Search Manager Agent",
    model=openai_model,
    instructions=SEARCH_MANAGER_INSTRUCTIONS,
    tools=search_manager_tools,
    handoffs=[email_manager_agent],
)
