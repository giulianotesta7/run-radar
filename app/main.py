import asyncio
from datetime import datetime
from dateutil.relativedelta import relativedelta

from agents import Runner, trace
from app_agents import search_manager_agent


def get_next_months(count: int) -> str:
    """Get the next <count> months as a formatted string."""
    today = datetime.now()
    months = []
    for i in range(1, count + 1):
        future_date = today + relativedelta(months=i)
        months.append(f"{future_date.strftime('%B')} {future_date.year}")
    return " and ".join(months)


search_period = get_next_months(2)


async def main():
    """Orchestrate the workflow via search_manager_agent with handoff to email_manager_agent."""
    with trace("runradar_workflow"):
        print("[LOG] Starting workflow...")
        print(f"[LOG] Running search_manager_agent for: {search_period}")

        result = await Runner.run(
            search_manager_agent,
            f"Find running events for {search_period}",
            max_turns=30,
        )

        print(f"[LOG] Workflow completed: {result.final_output}")
        print("[LOG] Workflow finished.")


if __name__ == "__main__":
    asyncio.run(main())
