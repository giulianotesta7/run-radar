import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta

from agents import Runner, trace
from app_agents import search_plan_agent, search_agent, email_manager
from models import WebSearchPlan


def get_next_months(count: int = 2) -> str:
    """Get the next N months as a formatted string."""
    today = datetime.now()
    months = []
    for i in range(1, count + 1):
        future_date = today + relativedelta(months=i)
        months.append(f"{future_date.strftime('%B')} {future_date.year}")
    return " and ".join(months)


search_period = get_next_months(2)


async def main():
    with trace("runradar_workflow"):
        # search plan
        plan_result = await Runner.run(
            search_plan_agent,
            f"Find running events for {search_period}"
        )
        search_plan: WebSearchPlan = plan_result.final_output
        print(f"Generated {len(search_plan.searches)} search queries")

        # execute search
        all_results = []
        for item in search_plan.searches:
            print(f"Searching: {item.query}")
            search_result = await Runner.run(search_agent, item.query)
            all_results.append(search_result.final_output)

        # compile results and send email
        compiled_events = "\n\n".join(all_results)
        email_prompt = f"""
        Here are the running events found for {search_period}:

        {compiled_events}

        Please create and send a professional email summarizing these events.
        """
        email_result = await Runner.run(email_manager, email_prompt, max_turns=20)
        print(f"Email workflow completed: {email_result.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
