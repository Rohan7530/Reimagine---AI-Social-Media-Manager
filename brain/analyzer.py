import os
import google.generativeai as genai
from pathlib import Path
from typing import Dict, Any

class ContentAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if path.suffix.lower() == '.pdf':
            return self._analyze_pdf(path)
        elif path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            return self._analyze_image(path)
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

    def _analyze_pdf(self, path: Path) -> Dict[str, Any]:
        # Upload the file to Gemini
        sample_file = genai.upload_file(path=path, display_name=path.name)
        
        prompt = """
        Analyze this document for a non-profit social media campaign.
        Extract the following:
        1. The main "Call to Action" (what do we want people to do?)
        2. 3-5 Key Statistics or shocking facts.
        3. A brief, emotional summary of the problem.
        4. Who is the target audience?
        
        Return the result as a JSON object.
        """
        
        response = self.model.generate_content([sample_file, prompt])
        return response.text # In a real app, we'd parse JSON here

    def _analyze_image(self, path: Path) -> Dict[str, Any]:
        sample_file = genai.upload_file(path=path, display_name=path.name)
        
        prompt = """
        Analyze this image for a social media post.
        Describe:
        1. The emotional tone (e.g., hopeful, urgent, devastating).
        2. Key visual elements.
        3. A suggested caption hook.
        
        Return the result as a JSON object.
        """
        
        response = self.model.generate_content([sample_file, prompt])
        return response.text
