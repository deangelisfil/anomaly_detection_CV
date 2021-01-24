import os
from pathlib import Path

cwd = Path(os.getcwd())
relPathVideo = "Resources/sorpasso.mp4"
vsPath = cwd.parent / relPathVideo
relPathBackground = "Resources/background.jpg"
# backgroundPath = ""
backgroundPath = cwd.parent / relPathBackground

resizeCoef = 3
outPath = "output.avi"
minAreaContour = 800
minBackgroundDiff = 125
