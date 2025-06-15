import os

# Safe for both local and deployment environments (like Render)
PROJECT_ROOT = os.getcwd()

# Central folder for generated files like images, audio, etc.
ASSET_DIR = os.path.join(PROJECT_ROOT, "generated-assets")

# Make sure it exists (optional: remove this if you're calling it elsewhere)
os.makedirs(ASSET_DIR, exist_ok=True)
