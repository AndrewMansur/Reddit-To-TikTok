TikTok Automation

A Python-based automation tool that creates TikTok videos by scraping Reddit posts, generating audio with AWS Polly, creating post images with Pillow, and combining them with gameplay footage and subtitles using FFmpeg. Built as a portfolio project to demonstrate skills in API integration, media processing, and automation.
Features

Scrapes unique posts from subreddits like r/confession and r/tifu using PRAW.
Converts post title and text to audio with AWS Polly.
Generates stylized post images with profile pictures and text using Pillow.
Combines gameplay video, audio, and subtitles into a final TikTok-ready video using FFmpeg.
Robust error handling for API calls, file operations, and media processing.
Modular design with clean code following PEP 8 conventions.

Demo
Watch a sample output video: Sample TikTok VideoNote: Replace the link with a hosted video (e.g., Google Drive, YouTube) or include a screenshot in the repo.
Prerequisites

Python: 3.8 or higher
FFmpeg: Installed and added to system PATH
NVIDIA Driver: Version 551.76+ for hardware encoding (h264_nvenc); current project uses libx264 for compatibility with older drivers (e.g., 546.29)
Accounts:
AWS account with Polly access
AssemblyAI account for transcription
Reddit developer account for API access


Assets: Gameplay video (Minecraft.mp4), images (ProfilePicture.jpeg, PostTemplate.png, Mask.png, Verified.png), and font (Kanit-Medium.ttf)

Setup

Clone the Repository:
git clone https://github.com/yourusername/TikTok-Automation.git
cd TikTok-Automation


Install Python Dependencies:
pip install -r requirements.txt


Install FFmpeg:

Windows: Download from ffmpeg.org or use Chocolatey:choco install ffmpeg


macOS/Linux: Use Homebrew (brew install ffmpeg) or your package manager.
Verify: ffmpeg -version


Configure Environment Variables:

Copy the example environment file:cp .env.example .env


Edit .env with your credentials:REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=TikTokAutomation/1.0 by your_username
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key




Prepare Assets:

Place Minecraft.mp4 in Assets/Video/.
Place ProfilePicture.jpeg, PostTemplate.png, Mask.png, and Verified.png in Assets/Images/.
Place Kanit-Medium.ttf in Assets/Fonts/.
Ensure the directory structure matches:TikTok-Automation/
├── Assets/
│   ├── Video/
│   │   └── Minecraft.mp4
│   ├── Images/
│   │   ├── ProfilePicture.jpeg
│   │   ├── PostTemplate.png
│   │   ├── Mask.png
│   │   ├── Verified.png
│   ├── Fonts/
│   │   └── Kanit-Medium.ttf
│   ├── Audio/
│   ├── Subtitles/





Usage
Run the main script to generate a TikTok video:
python src/video_generator.py


Output: Assets/Video/FinalVideo.mp4
The script scrapes a Reddit post, generates audio and an image, and combines them with gameplay footage and subtitles.

Notes

Video Encoding: Uses libx264 for CPU-based encoding due to NVIDIA driver 546.29. For faster GPU encoding, update to driver 551.76+ and change libx264 to h264_nvenc in src/video_generator.py.
Error Handling: The project includes robust checks for file existence, API errors, and FFmpeg failures.
Font: Subtitles use Arial for compatibility. Replace with Kanit-Medium.ttf in src/video_generator.py if desired.
Extensibility: Modular design allows easy addition of new subreddits, voices, or video inputs.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m 'Add your feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
MIT License
Contact
For questions or feedback, reach out via GitHub Issues or your.email@example.com.