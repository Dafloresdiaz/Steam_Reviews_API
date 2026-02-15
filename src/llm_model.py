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
        Give the result without paragraph breaks, special characters just give
        text.
        IMPORTANT: Give the result in 150 characters, no more.
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

    def batch_sentiment(self, reviews: List[str]) -> str:
        """
        Process reviews in batches and return joined sentiment summaries.
        Args:
            reviews (List[str]): List of review texts to analyze.
        Returns:
            str: Sentiment summaries joined by <SENTIMENT> tag, one per batch.
        Note:
            Uses batch size of 15 reviews per LLM call.
        """
        batch_size = 15
        batches = [reviews[i:i+batch_size] for i in range(0, len(reviews), batch_size)]
        sentiments = []
        for batch in batches:
            sentiments.append(self.generate_sentiment(batch))
        return "\n----<SENTIMENT>----\n".join(sentiments)

    def generate_general_sentiment(self, reviews: List[str]) -> str:
        """
        Generate overall sentiment analysis for a list of game reviews using batch processing.
        Args:
            reviews (List[str]): List of review texts to analyze.
        Returns:
            str: Overall sentiment analysis summary in 150 characters or less.
        """
        sentiments = self.batch_sentiment(reviews)
        prompt = f"""
        With the list of sentiments create an overall sentiment with positives and negatives aspects.
        Also add if the game is worth playing or not and to buy or not.
        Each sentiment is separated by the tag <SENTIMENT>.
        Give the result without paragraph breaks, special characters just give
        text, don't use markdown, don't create a list, pure text.
        IMPORTANT: Give the result in 150 characters, no more.
        Include positive and negative aspects if applicable.

        Sentiments summaries:

        {sentiments}
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