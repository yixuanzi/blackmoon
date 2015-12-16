import os
import sys
import sys
import os
import pm
# append modle path
sys.path.append(sys.path[0]+'\\libs')
sys.path.append(sys.path[0]+'\\plugins')
from pm import *
from bmplugin import *
from main_command import *

main=main_command()
init_plugins(main)
main.start()