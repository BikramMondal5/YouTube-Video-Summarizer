import os
import re
from flask import Flask, render_template, request, redirect, url_for, jsonify
from markupsafe import Markup
import markdown
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev_secret_key_for_testing_only')

# Hardcoded API token - replace with your actual token
GITHUB_PAT = os.environ.get('youtube-summarizer')  # Replace with your GitHub PAT
ENDPOINT = "https://models.github.ai/inference"
MODEL_NAME = "openai/gpt-4o"

# OpenAI client configuration
client = OpenAI(
    base_url=ENDPOINT,
    api_key=GITHUB_PAT,
)

def extract_video_id(youtube_url):
    """Extract the video ID from a YouTube URL."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # Standard and short URLs
        r'(?:embed\/)([0-9A-Za-z_-]{11})',   # Embed URLs
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'  # youtu.be URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    
    return None

def get_transcript(video_id):
    """Get transcript from YouTube video."""
    try:
        # Try to get transcript in multiple languages
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi', 'bn'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return {"success": True, "transcript": full_text}
    except NoTranscriptFound:
        return {"success": False, "error": "No transcript found for this video."}
    except TranscriptsDisabled:
        return {"success": False, "error": "Transcripts are disabled for this video."}
    except Exception as e:
        return {"success": False, "error": str(e)}

def summarize_transcript(transcript):
    """Use GPT-4o to summarize the transcript."""
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You're an advanced AI designed to summarize YouTube videos. Extract key information from the transcript including Title of the video, speaker, main topics, key takeaways, Timestamps for Notable Moments, Quotes and Impactful Statements, Analysis Sentiment if possible and notable insights. Format your response using Markdown with proper headings, bullet points, add interactive & appropriate emojis and sections for easy reading. Include a brief overview, key points, and conclusion."
                },
                {
                    "role": "user",
                    "content": transcript,
                }
            ],
            temperature=0.7,
            top_p=1.0,
            max_tokens=1500,
            model=MODEL_NAME
        )
        
        return {"success": True, "summary": response.choices[0].message.content}
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    youtube_url = request.form.get('youtube_url', '')
    
    if not youtube_url:
        return jsonify({"success": False, "error": "Please enter a YouTube URL"})
    
    video_id = extract_video_id(youtube_url)
    if not video_id:
        return jsonify({"success": False, "error": "Invalid YouTube URL. Please check and try again."})
    
    # Get transcript
    transcript_result = get_transcript(video_id)
    if not transcript_result["success"]:
        return jsonify({"success": False, "error": transcript_result["error"]})
    
    # Summarize transcript
    summary_result = summarize_transcript(transcript_result["transcript"])
    if not summary_result["success"]:
        return jsonify({"success": False, "error": summary_result["error"]})
    
    # Convert markdown to HTML
    summary_html = markdown.markdown(summary_result["summary"])
    
    return jsonify({
        "success": True,
        "video_id": video_id,
        "summary_html": summary_html
    })

if __name__ == "__main__":
    # Ensure directories exist
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    app.run(debug=True)