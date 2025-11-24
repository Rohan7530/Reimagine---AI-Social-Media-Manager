import streamlit as st
import os
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Import our backend logic
from brain.analyzer import ContentAnalyzer
from brain.generator import CampaignGenerator
from models import Campaign, Post
from server import post_to_twitter, post_to_linkedin, post_to_instagram

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Setup directories
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Amplifier | AI Campaign Manager",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for "Premium" feel
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #ff3333;
    }
    .card {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border: 1px solid #363945;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

def save_uploaded_file(uploaded_file):
    try:
        with open(INPUT_DIR / uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return INPUT_DIR / uploaded_file.name
    except Exception as e:
        return None

def load_campaigns():
    campaigns = []
    for file in OUTPUT_DIR.glob("*_campaign.json"):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                campaigns.append((file.name, Campaign(**data)))
        except:
            pass
    return campaigns

def main():
    st.sidebar.title("🚀 Amplifier")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Create Campaign", "Manage Campaigns"])

    if page == "Dashboard":
        st.title("Welcome back, Rohan 👋")
        st.markdown("### Campaign Overview")
        
        campaigns = load_campaigns()
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Campaigns", len(campaigns))
        col2.metric("Posts Scheduled", sum(len(c[1].posts) for c in campaigns))
        col3.metric("Pending Approvals", len([c for c in campaigns if c[1].status == "draft"]))

        st.markdown("---")
        st.markdown("### Recent Activity")
        for filename, camp in campaigns[-3:]:
            st.markdown(f"""
            <div class="card">
                <h4>{camp.title}</h4>
                <p>{camp.goal}</p>
                <small>Status: {camp.status} | Posts: {len(camp.posts)}</small>
            </div>
            """, unsafe_allow_html=True)

    elif page == "Create Campaign":
        st.title("✨ Create New Campaign")
        st.write("Upload a PDF Report or an Image to generate a social media campaign.")
        
        uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'png', 'jpg', 'jpeg'])
        
        if uploaded_file is not None:
            if st.button("Generate Campaign"):
                with st.spinner("Analyzing file and crafting content..."):
                    # Save file
                    file_path = save_uploaded_file(uploaded_file)
                    
                    if file_path:
                        # Analyze
                        analyzer = ContentAnalyzer(API_KEY)
                        analysis = analyzer.analyze_file(file_path)
                        
                        # Generate
                        generator = CampaignGenerator(API_KEY)
                        title = file_path.stem.replace("_", " ").title()
                        campaign = generator.generate_campaign(analysis, title)
                        
                        # Save
                        output_file = OUTPUT_DIR / f"{title.replace(' ', '_')}_campaign.json"
                        with open(output_file, "w") as f:
                            f.write(campaign.model_dump_json(indent=2))
                        
                        st.success(f"Campaign '{title}' generated successfully!")
                        st.balloons()

    elif page == "Manage Campaigns":
        st.title("📢 Manage Campaigns")
        
        campaigns = load_campaigns()
        if not campaigns:
            st.info("No campaigns found. Go create one!")
            return

        selected_filename, selected_campaign = st.selectbox(
            "Select Campaign", 
            campaigns, 
            format_func=lambda x: x[1].title
        )

        st.markdown(f"## {selected_campaign.title}")
        st.write(f"**Goal:** {selected_campaign.goal}")
        
        st.markdown("### Posts")
        
        for i, post in enumerate(selected_campaign.posts):
            with st.expander(f"{post.platform.value.title()} Post", expanded=True):
                new_content = st.text_area(f"Content", post.content, key=f"content_{i}", height=150)
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button(f"Publish to {post.platform.value.title()}", key=f"btn_{i}"):
                        # Call FastMCP tools directly
                        if post.platform == "twitter":
                            result = post_to_twitter(new_content, post.hashtags)
                        elif post.platform == "linkedin":
                            result = post_to_linkedin(new_content, post.hashtags)
                        elif post.platform == "instagram":
                            result = post_to_instagram(new_content, "image_placeholder.jpg", post.hashtags)
                        
                        st.success(result)

if __name__ == "__main__":
    main()
