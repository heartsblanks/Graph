import os
from pptx import Presentation

# Folder containing the PowerPoint files
ppt_folder = "path_to_your_folder"  # Update this with the path to your folder

# Iterate through all files in the folder
for file_name in os.listdir(ppt_folder):
    if file_name.endswith(".pptx"):  # Only process PowerPoint files
        ppt_file = os.path.join(ppt_folder, file_name)
        print(f"\nProcessing file: {file_name}")

        # Load the PowerPoint presentation
        prs = Presentation(ppt_file)

        # Iterate through slides to extract titles and text from shapes
        for slide_num, slide in enumerate(prs.slides):
            print(f"\nSlide {slide_num + 1}:")
            
            # Extract the slide's title (header)
            if slide.shapes.title:
                title = slide.shapes.title.text
                print(f"Title: {title}")
            else:
                print("Title: None")

            # Extract text from other shapes
            for shape_num, shape in enumerate(slide.shapes):
                # Skip the title shape (we already extracted that)
                if shape == slide.shapes.title:
                    continue

                if not shape.has_text_frame:
                    continue  # Skip shapes without text

                # Extract text from each shape's text frame
                text = "\n".join([paragraph.text for paragraph in shape.text_frame.paragraphs])
                print(f"Shape {shape_num + 1}: {text}")