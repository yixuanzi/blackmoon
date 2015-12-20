import os
import sys
import sys
import os

# append modle path
sys.path.append(sys.path[0]+'\\libs')
sys.path.append(sys.path[0]+'\\plugins')

from pm import *
from bmplugin import *
from main_command import *

for path in PLUGINS_PATH:
    sys.path.append(path)

main=main_command()
init_plugins(main)
main.start()