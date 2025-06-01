import openai
import os
import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class SentimentAgent(Agent):
    class AnalyzeSentiment(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                data = json.loads(msg.body)
                user_message = data.get("last_message", "")

                print(f"[SentimentAgent] Analyzing message: {user_message}")

                # Call LLM for sentiment
                sentiment = await self.analyze_with_llm(user_message)
                data["sentiment"] = sentiment

                reply = msg.make_reply()
                reply.set_metadata("performative", "inform")
                reply.body = json.dumps(data)
                await self.send(reply)

        async def analyze_with_llm(self, text):
            try:
                prompt = f"""Classify the sentiment of the following customer message as one of: positive, neutral, or negative.\n\nMessage: \"{text}\"\n\nSentiment:"""

                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.0,
                    max_tokens=10
                )

                sentiment = response.choices[0].message["content"].strip().lower()
                if sentiment not in ["positive", "neutral", "negative"]:
                    sentiment = "neutral"  # fallback
                print(f"[SentimentAgent] LLM returned sentiment: {sentiment}")
                return sentiment
            except Exception as e:
                print(f"[SentimentAgent] Error: {e}")
                return "neutral"

    async def setup(self):
        print(f"[SentimentAgent] Running: {str(self.jid)}")
        self.add_behaviour(self.AnalyzeSentiment())
