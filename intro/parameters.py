import os
from pathlib import Path

cwd = Path(os.getcwd())
relPathImage = "Resources/Machiavelli.jpg"
relPathVideo = "Resources/sorpasso.mp4"
pathImage = cwd.parent / relPathImage
pathVideo = cwd.parent / relPathVideo

