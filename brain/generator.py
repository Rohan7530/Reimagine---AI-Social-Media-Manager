import json
import google.generativeai as genai
from typing import Dict, Any
from models import Campaign, Post, SocialPlatform

class CampaignGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def generate_campaign(self, analysis: Dict[str, Any], title: str) -> Campaign:
        prompt = f"""
        Based on the following analysis of a non-profit asset:
        {analysis}

        Create a social media campaign titled "{title}".
        Generate 3 posts:
        1. A Twitter thread (3-5 tweets) focusing on the stats.
        2. A LinkedIn post focusing on the professional/systemic impact.
        3. An Instagram caption focusing on the emotional story.

        Return the result as a JSON object matching this schema:
        {{
            "title": "Campaign Title",
            "goal": "Campaign Goal",
            "posts": [
                {{
                    "platform": "twitter",
                    "content": "Tweet 1... \\n\\n Tweet 2...",
                    "hashtags": ["#tag1", "#tag2"]
                }},
                {{
                    "platform": "linkedin",
                    "content": "Article text...",
                    "hashtags": ["#tag1"]
                }},
                {{
                    "platform": "instagram",
                    "content": "Caption...",
                    "hashtags": ["#tag1"]
                }}
            ]
        }}
        """
        
        response = self.model.generate_content(prompt)
        # In a real app, we need robust JSON parsing here (stripping markdown fences)
        try:
            cleaned_text = response.text.replace('```json', '').replace('```', '')
            data = json.loads(cleaned_text)
            return Campaign(**data)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            # Return a dummy campaign for safety if parsing fails
            return Campaign(title=title, goal="Error generating campaign", posts=[])
