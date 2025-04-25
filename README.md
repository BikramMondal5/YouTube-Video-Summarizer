# 🎬 YouTube-Video-Summarizer

A streamlined, lightweight, web application that summarizes YouTube videos using OpenAI gpt-4o API. User can get concise, well-structured summaries by entering a YouTube URL.

## 🌟 Features

-   **Multi-Language Transcript Extraction:** Extracts transcripts from YouTube videos in English, Hindi, and Bengali.
-   **AI-Powered Summaries:** Generates summaries using the power of GPT-4o.
-   **Comprehensive Summary Output:**
    -   Video Title
    -   Main Topics
    -   Key Takeaways
    -   Timestamps for Notable Moments
    -   Important Quotes
    -   Sentiment Analysis (when possible)
    -   Notable Insights
-   **User-Friendly Interface:**  Markdown formatting for easy readability.
-   **Responsive Design:**  Works seamlessly on desktop and mobile devices.

## 🛠️ Technologies Used

-   **Frontend:** HTML, CSS, JavaScript
-   **Backend:** Python, Flask
-   **AI Model:** OpenAI GPT-4o
-   **Other:**  GitHub PAT for API authentication.

## ⚙️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BikramMondal5/YouTube-Video-Summarizer.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd YouTube-Video-Summarizer
    ```
3.  **Set up a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    # On Windows: venv\Scripts\activate
    ```
4.  **Install the required dependencies:**
    ```bash
    pip install flask youtube_transcript_api openai markdown
    ```
5.  **Set environment variables:**

    -   **Linux/macOS:**
        ```bash
        export FLASK_SECRET_KEY="your_secret_key"
        export youtube-summarizer="your_github_pat_token"
        ```
    -   **Windows:**
        ```bash
        set FLASK_SECRET_KEY=your_secret_key
        set youtube-summarizer=your_github_pat_token
        ```

## 📸 Screenshots

![YouTube Video Summarizer Screenshot](screenshot.jpg)

## 🚀 How to Use

1.  Open the application in your web browser.
2.  Paste a YouTube URL in the input field.
3.  Click the "✨ Summarize" button.
4.  Wait for the application to process the video.
5.  View the summary alongside the embedded video (if applicable).

## 🤝 Contribution

Feel free to fork this repository, raise issues, or submit pull requests to add features or improve the design.

## 📜 License

This project is licensed under the `MIT License`.
