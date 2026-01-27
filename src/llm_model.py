import os
from typing import List
from huggingface_hub import InferenceClient

client = InferenceClient(
    api_key=os.getenv("HUGGINGFACE_API_KEY", ""), #Add you huggingface API KEY here
)

class LLM_Model:
    """
    Class to generate sentiment analysis using LLM models.
    This class uses HuggingFace's InferenceClient to analyze the sentiment
    of game reviews using large language models.
    """

    def generate_sentiment(self, reviews: List[str]) -> str:
        """
        Generate sentiment analysis for a list of game reviews.
        Args:
            reviews (List[str]): List of review texts to analyze.
        Returns:
            str: Sentiment analysis summary from the LLM.
        Raises:
            ValueError: If reviews list is empty.
            Exception: If API call fails.
        Note:
            Uses cardiffnlp/twitter-roberta-base-sentiment model for analysis.
        """
        if not reviews:
            raise ValueError("Reviews list cannot be empty")
        reviews_text = "\n----<REVIEW>----\n".join(reviews)
        prompt = f"""
        Summarize the overall sentiment of these game reviews.
        Each review is separated by the tag <REVIEW>.
        Give the result without paragraph breaks.
        Give the result in 250 words, no more.
        Include positive and negative aspects if applicable.
        Reviews:

        {reviews_text}
        """
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct:hyperbolic",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
        )

        sentiment = completion.choices[0].message.content or "No sentiment analysis available"
        return sentiment.replace('\n', ' ').strip()