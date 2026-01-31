from pydantic import BaseModel, Field

class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use for the web search.")


class SearchResult(BaseModel):
    result: str = Field(
        description="The search results containing running events found. "
        "Each event should include: name, date, city, distances, and URL when available."
    )

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

class EmailSubject(BaseModel):
    subject: str = Field(description="A concise, engaging email subject line that summarizes the running events.")
    
class EmailBody(BaseModel):
    body: str = Field(
        description="The complete email body text. Professional, clear, "
        "formatted with paragraphs. No subject line or HTML tags - plain text only."
    )

class EmailHtmlContent(BaseModel):
    html_content: str = Field(description="The HTML body of the email containing a formatted list of running events with event names, dates, locations, and registration links.")

class EmailValidationResult(BaseModel):
    is_valid: bool = Field(description="Indicates whether the email content is valid.")
    issues: list[str] = Field(description="A list of issues found in the email content, if any.")