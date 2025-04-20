document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('youtube-form');
    const urlInput = document.getElementById('youtube-url');
    const summarizeBtn = document.getElementById('summarize-btn');
    const spinner = summarizeBtn.querySelector('.spinner-border');
    const buttonText = summarizeBtn.querySelector('.button-text');
    const errorMessage = document.getElementById('error-message');
    const results = document.getElementById('results');
    const videoIframe = document.getElementById('video-iframe');
    const summaryContent = document.getElementById('summary-content');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset UI
        errorMessage.style.display = 'none';
        results.style.display = 'none';
        
        // Get YouTube URL
        const youtubeUrl = urlInput.value.trim();
        
        if (!youtubeUrl) {
            showError('Please enter a YouTube URL');
            return;
        }
        
        // Show loading state
        setLoading(true);
        
        // Send request to server
        const formData = new FormData();
        formData.append('youtube_url', youtubeUrl);
        
        fetch('/summarize', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            setLoading(false);
            
            if (!data.success) {
                showError(data.error);
                return;
            }
            
            // Display results
            videoIframe.src = `https://www.youtube.com/embed/${data.video_id}`;
            summaryContent.innerHTML = data.summary_html;
            results.style.display = 'block';
            
            // Scroll to results
            results.scrollIntoView({ behavior: 'smooth', block: 'start' });
        })
        .catch(error => {
            setLoading(false);
            showError('An error occurred. Please try again.');
            console.error('Error:', error);
        });
    });
    
    function setLoading(isLoading) {
        if (isLoading) {
            buttonText.textContent = 'Processing...';
            spinner.classList.remove('d-none');
            summarizeBtn.disabled = true;
        } else {
            buttonText.textContent = '✨ Summarize';
            spinner.classList.add('d-none');
            summarizeBtn.disabled = false;
        }
    }
    
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }
});