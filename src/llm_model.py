import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key="",
)

class LLM_Model:
    def generate_sentiment(self, reviews: list) -> str:
        reviews_text = "\n----<REVIEW>----\n".join(reviews)
        prompt =prompt = f"""
        Summarize the overall sentiment of these game reviews.
        Each review is separated by the tag <REVIEW>.

        {reviews_text}
        """
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-70B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        return completion.choices[0].message.content