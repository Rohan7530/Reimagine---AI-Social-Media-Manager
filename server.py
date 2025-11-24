from fastmcp import FastMCP
from typing import List

# Initialize FastMCP server
mcp = FastMCP("Amplifier Social Tools")

@mcp.tool()
def post_to_twitter(content: str, hashtags: List[str] = []) -> str:
    """
    Post a tweet to Twitter.
    Args:
        content: The text of the tweet.
        hashtags: A list of hashtags to append.
    """
    full_content = f"{content}\n\n{' '.join(hashtags)}"
    # Mock implementation
    print(f"\n[MOCK TWITTER] Posting:\n{full_content}\n")
    return "Tweet posted successfully (Mock)"

@mcp.tool()
def post_to_linkedin(content: str, hashtags: List[str] = []) -> str:
    """
    Post an article or update to LinkedIn.
    Args:
        content: The text of the post.
        hashtags: A list of hashtags to append.
    """
    full_content = f"{content}\n\n{' '.join(hashtags)}"
    # Mock implementation
    print(f"\n[MOCK LINKEDIN] Posting:\n{full_content}\n")
    return "LinkedIn post published successfully (Mock)"

@mcp.tool()
def post_to_instagram(caption: str, image_path: str, hashtags: List[str] = []) -> str:
    """
    Post a photo to Instagram.
    Args:
        caption: The caption for the photo.
        image_path: Absolute path to the image file.
        hashtags: A list of hashtags to append.
    """
    full_content = f"{caption}\n\n{' '.join(hashtags)}"
    # Mock implementation
    print(f"\n[MOCK INSTAGRAM] Posting Image: {image_path}\nCaption: {full_content}\n")
    return "Instagram post published successfully (Mock)"

if __name__ == "__main__":
    mcp.run()
