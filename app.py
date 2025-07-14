from flask import Flask, request, render_template, send_from_directory
import subprocess
import os
import uuid

app = Flask(__name__)
VIDEO_DIR = os.path.join("static", "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = None
    error = None

    if request.method == 'POST':
        tiktok_url = request.form.get('url', '').strip()
        if not tiktok_url:
            error = "Please enter a valid TikTok URL."
        else:
            filename = str(uuid.uuid4()) + ".mp4"
            output_path = os.path.join(VIDEO_DIR, filename)

            try:
                cmd = [
                    "yt-dlp",
                    "-o", output_path,
                    tiktok_url
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode == 0 and os.path.exists(output_path):
                    video_url = f"/static/videos/{filename}"
                else:
                    print("yt-dlp error:", result.stderr)
                    error = "❌ Failed to download video. Please try again."
            except Exception as e:
                error = f"❌ Error: {e}"

    return render_template("index.html", video_url=video_url, error=error)

if __name__ == '__main__':
    app.run(debug=True)

