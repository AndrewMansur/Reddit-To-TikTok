
# TikTok Automation

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

A Python-based automation tool that creates TikTok videos by scraping Reddit posts, generating audio with AWS Polly, creating post images with Pillow, and combining them with gameplay footage and subtitles using FFmpeg. Built as a portfolio project to demonstrate skills in API integration, media processing, and automation.

## Features
- Scrapes unique posts from subreddits like `r/confession` and `r/tifu` using PRAW.
- Converts post title and text to audio with AWS Polly.
- Generates stylized post images with profile pictures and text using Pillow.
- Combines gameplay video, audio, and subtitles into a final TikTok-ready video using FFmpeg.
- Robust error handling for API calls, file operations, and media processing.
- Modular design with clean code following PEP 8 conventions.

## Demo
Watch a sample output video: [Sample TikTok Video](https://example.com/sample-video.mp4)
*Note: Replace the link with a hosted video (e.g., Google Drive, YouTube) or include a screenshot in the repo.*

## Prerequisites
- **Python**: 3.8 or higher
- **FFmpeg**: Installed and added to system PATH
- **NVIDIA Driver**: Version 551.76+ for hardware encoding (`h264_nvenc`); current project uses `libx264` for compatibility with older drivers (e.g., 546.29)
- **Accounts**:
  - AWS account with Polly access
  - AssemblyAI account for transcription
  - Reddit developer account for API access
- **Assets**: Gameplay video (`Minecraft.mp4`), images (`ProfilePicture.jpeg`, `PostTemplate.png`, `Mask.png`, `Verified.png`), and font (`Kanit-Medium.ttf`)

## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/TikTok-Automation.git
   cd TikTok-Automation
 2. **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt`
3. **Install FFmpeg:**
 - **Windows**: Download from ffmpeg.org or use Chocolatey
	
	```bash
	choco install ffmpeg
	```

- **macOS/Linux:** Use Homebrew (`brew install ffmpeg`) or your package manager
- Verify: `ffmpeg -version`

4. **Configure Environment Variables**:
-	Copy the example environment file:
  ``` bash
    cp .env.example .env 
   ```
   - edit `.env` file with your credentials
   
```plaintext 
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=TikTokAutomation/1.0 by your_username
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
   ```

- Ensure AWS credentials have `AmazonPollyFullAccess` permissions and use `AWS_SECRET_ACCESS_KEY` (not `AWS_SECRET`). Missing or invalid credentials will cause a `ValueError`.


5. **Prepare Assets**:
- Place the following files in their respective directories:
	- `assets/Video/Minecraft.mp4`: A gameplay video (e.g., Minecraft clip).
	- assets/Images/ProfilePicture.jpeg: A profile image (e.g., 100x100 pixels).
	- assets/Images/PostTemplate.png: A blank template (e.g., 1080x1920 pixels).
	-  assets/Images/Mask.png: A circular mask image (e.g., 170x170 pixels).
	-  assets/Images/Verified.png: A verified badge icon (e.g., 50x50 pixels).
	- assets/Fonts/Kanit-Medium.ttf: Kanit Medium font from [Google Fonts](https://fonts.google.com/specimen/Kanit).

- Missing files will cause a FileNotFoundError. Download sample assets or create placeholders as needed

## Usage
Run the main script to generate a TikTok video:
```bash
python video_generator.py
```
- **Output**: `assets/Video/FinalVideo.mp4`
- The script scrapes a Reddit post, generates audio and an image, and combines them with gameplay footage and subtitles.

## Notes
- **Video Encoding**: Uses `libx264` for CPU-based encoding due to NVIDIA driver 546.29. For faster GPU encoding, update to driver 551.76+ and change `libx264` to `h264_nvenc` in `video_generator.py`.
- **Error Handling**: The project includes robust checks for file existence, API errors, and FFmpeg failures.
- **Font**: Subtitles use Arial for compatibility. Replace with Kanit-Medium.ttf in video_generator.py if desired.
- **Extensibility**: Modular design allows easy addition of new subreddits, voices, or video inputs.
