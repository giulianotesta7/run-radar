import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
import resend

from agents import function_tool
from config import (
    brave_api_key,
    resend_api_key,
    sender_name,
    sender_email,
    recipient_email,
    email_provider,
    gmail_email,
    gmail_app_password,
)

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


def _send_with_resend(subject: str, html_content: str) -> str:
    """Send email using Resend API."""
    resend.api_key = resend_api_key
    from_field = f"{sender_name} <{sender_email}>" if sender_name else sender_email
    params = {
        "from": from_field,
        "to": [recipient_email],
        "subject": subject,
        "html": html_content,
    }
    email = resend.Emails.send(params)
    return f"Email sent successfully to {recipient_email}. Message ID: {email['id']}"


def _send_with_gmail(subject: str, html_content: str) -> str:
    """Send email using Gmail SMTP."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{gmail_email}>" if sender_name else gmail_email
    msg["To"] = recipient_email

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_email, gmail_app_password)
        server.sendmail(gmail_email, recipient_email, msg.as_string())

    return f"Email sent successfully to {recipient_email} via Gmail."


@function_tool
def send_email(subject: str, html_content: str) -> str:
    """
    Send a transactional email.
    Args:
        subject: Email subject line.
        html_content: HTML content of the email body.
    Returns:
        A string with the result or error message.
    """
    try:
        if email_provider == "gmail":
            return _send_with_gmail(subject, html_content)
        else:
            return _send_with_resend(subject, html_content)
    except Exception as e:
        return f"Error sending email: {e}"
