from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path
import helpers  # Changed from 'from . import helpers'

def create_post_image(
    profile_picture_path: Path,
    template_path: Path,
    mask_path: Path,
    username: str,
    scrape
) -> None:
    # Create a post image with profile picture, username, and post title
    print("Generating post image...")
    try:
        # Load images
        mask = Image.open(mask_path).convert("L")
        profile_picture = Image.open(profile_picture_path)
        post_template = Image.open(template_path).convert("RGBA")
        verified_image = Image.open("Assets/Images/Verified.png").convert("RGBA")

        # Process profile picture
        circle_diameter = 170
        circle_position = (71, 62)
        profile_picture = ImageOps.fit(
            profile_picture,
            (circle_diameter, circle_diameter),
            centering=(0.5, 0.5)
        )
        resized_mask = mask.resize(profile_picture.size)
        profile_picture.putalpha(resized_mask)
        post_template.paste(profile_picture, circle_position, profile_picture)

        # Draw username
        text_color = "black"
        font_path = "Assets/Fonts/Kanit-Medium.ttf"
        username_font = ImageFont.truetype(font_path, 40)
        text_font = ImageFont.truetype(font_path, 45)
        text_width, _ = helpers.get_text_dimensions(username, username_font)
        username_position = (300, 100)
        draw = ImageDraw.Draw(post_template)
        draw.text(username_position, username, fill=text_color, font=username_font)

        # Draw post title
        split_text = helpers.split_string(scrape.title)
        for i, line in enumerate(split_text):
            text_position = (68, 250 + 45 * i)
            draw.text(text_position, line, fill=text_color, font=text_font)

        # Add verified badge
        verified_image_size = (50, 50)
        verified_image = verified_image.resize(verified_image_size, Image.Resampling.LANCZOS)
        verified_image_position = (username_position[0] + text_width + 10, 105)
        post_template.paste(verified_image, verified_image_position, verified_image)

        # Save final image
        finalized_image = post_template.resize((540, 290))
        output_path = Path("Assets/Images/Post.png")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        finalized_image.save(output_path)
    except Exception as e:
        print(f"Error generating post image: {str(e)}")
        raise