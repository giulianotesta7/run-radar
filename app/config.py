from dotenv import load_dotenv
import os
load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
brave_api_key = os.getenv('BRAVE_API_KEY')
resend_api_key = os.getenv('RESEND_API_KEY')
how_many_searches = os.getenv('HOW_MANY_SEARCHES')
country = os.getenv('COUNTRY')
sender_name = os.getenv('SENDER_NAME')
sender_email = os.getenv('SENDER_EMAIL')
recipient_name = os.getenv('RECIPIENT_NAME')
recipient_email = os.getenv('RECIPIENT_EMAIL')
email_provider = os.getenv('EMAIL_PROVIDER')
gmail_email = os.getenv('GMAIL_EMAIL')
gmail_app_password = os.getenv('GMAIL_APP_PASSWORD')

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

if not brave_api_key:
    raise ValueError("BRAVE_API_KEY is not set in environment variables.")

if not how_many_searches:
    raise ValueError("HOW_MANY_SEARCHES is not set in environment variables.")

if not country:
    raise ValueError("COUNTRY is not set in environment variables.")

if not resend_api_key:
    raise ValueError("RESEND_API_KEY is not set in environment variables.")

if not sender_email:
    raise ValueError("SENDER_EMAIL is not set in environment variables. Use 'onboarding@resend.dev' for testing.")

if not recipient_email:
    raise ValueError("RECIPIENT_EMAIL is not set in environment variables.")

if email_provider == "gmail":
    if not gmail_email:
        raise ValueError("GMAIL_EMAIL is not set in environment variables for Gmail provider.")
    if not gmail_app_password:
        raise ValueError("GMAIL_APP_PASSWORD is not set in environment variables for Gmail provider.")

