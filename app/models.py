from pydantic import BaseModel, Field

class WebSearchItem(BaseModel):
    query: str = Field(description="The search term to use for the web search.")

    reason: str = Field(description="Your reasoning for why this search is important to the query.")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")

class EmailSubject(BaseModel):
    subject: str = Field(description="A concise, engaging email subject line that summarizes the running events.")
    
class EmailHtmlContent(BaseModel):
    html_content: str = Field(description="The HTML body of the email containing a formatted list of running events with event names, dates, locations, and registration links.")