import requests
import resend

from agents import function_tool
from config import brave_api_key, resend_api_key, sender_name, sender_email, recipient_name, recipient_email

BRAVE_WEB_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"


@function_tool
def web_search(query: str) -> str:
    """
    Search the web using Brave Search API.
    Args:
        query: The search query string to look up
    Returns:
        A formatted string with search results including titles, URLs, and descriptions.
    """
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_api_key,
    }

    params = {
        "q": query,
        "count": 10,
    }

    try:
        response = requests.get(
            BRAVE_WEB_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        results = []
        web_results = data.get("web", {}).get("results", [])

        for result in web_results:
            title = result.get("title", "No title")
            url = result.get("url", "")
            description = result.get("description", "No description")
            results.append(f"Title: {title}\nURL: {url}\nDescription: {description}\n")

        if not results:
            return "No results found for the query."

        return "\n---\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Error performing web search: {str(e)}"


@function_tool
def send_email(subject: str, html_content: str) -> str:
    """
    Send a transactional email using Resend.
    Args:
        subject: Email subject line.
        html_content: HTML content of the email body.
    Returns:
        A string with the result or error message.
    """
    resend.api_key = resend_api_key

    try:
        from_field = f"{sender_name} <{sender_email}>" if sender_name else sender_email
        params = {
            "from": from_field,
            "to": [recipient_email],
            "subject": subject,
            "html": html_content,
        }
        email = resend.Emails.send(params)
        return f"Email sent successfully to {recipient_email}. Message ID: {email['id']}"
    except Exception as e:
        return f"Error sending email: {e}"
