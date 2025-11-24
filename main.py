import os
import time
import json
from dotenv import load_dotenv
from pathlib import Path

from monitor import FolderMonitor
from brain.analyzer import ContentAnalyzer
from brain.generator import CampaignGenerator

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY not found in .env file")
    # We don't exit here to allow the user to fix it while running, 
    # but in a real app we might.

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

def process_file(file_path: str):
    print(f"Processing {file_path}...")
    
    try:
        # 1. Analyze
        analyzer = ContentAnalyzer(API_KEY)
        analysis = analyzer.analyze_file(file_path)
        print("Analysis complete.")
        
        # 2. Generate Campaign
        generator = CampaignGenerator(API_KEY)
        # Use filename as default title
        title = Path(file_path).stem.replace("_", " ").title()
        campaign = generator.generate_campaign(analysis, title)
        print("Campaign generated.")
        
        # 3. Save Draft
        output_file = OUTPUT_DIR / f"{title.replace(' ', '_')}_campaign.json"
        with open(output_file, "w") as f:
            f.write(campaign.model_dump_json(indent=2))
            
        print(f"Draft saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    # Ensure directories exist
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    monitor = FolderMonitor(str(INPUT_DIR), process_file)
    monitor.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()

if __name__ == "__main__":
    main()
