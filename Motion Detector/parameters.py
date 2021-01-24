import os
from pathlib import Path

cwd = Path(os.getcwd())
relPathVideo = "Resources/sorpasso.mp4"
vsPath = cwd.parent / relPathVideo
#vsPath = ""
relPathBackground = "Resources/background.jpg"
backgroundPath = cwd.parent / relPathBackground
#backgroundPath = 40
resize = True
resizeCoef = 3
outPath = "output.avi"
minAreaContour = 800
minBackgroundDiff = 125
# minBackgroundDiff = 100
