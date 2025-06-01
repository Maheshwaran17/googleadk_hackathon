import asyncio
from spade import quit_spade

async def main():
    # Instantiate each agent with dummy passwords
    context = ContextAgent("context_agent@localhost", "password")
    sentiment = SentimentAgent("sentiment_agent@localhost", "password")
    engagement = EngagementAgent("engagement_agent@localhost", "password")
    upsell = UpsellAgent("upsell_agent@localhost", "password")
    comm = CommunicationAgent("comm_agent@localhost", "password")
    retention = RetentionAgent("retention_agent@localhost", "password")

    # Start them
    await context.start()
    await sentiment.start()
    await engagement.start()
    await upsell.start()
    await comm.start()
    await retention.start()

    await asyncio.sleep(10)
    await quit_spade()

if __name__ == "__main__":
    asyncio.run(main())
