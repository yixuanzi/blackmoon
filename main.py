import os
import sys
import sys
import os
sys.path.append(sys.path[0]+'\\libs')
sys.path.append(sys.path[0]+'\\plugins')
from bmplugin import *

main_i=lib_interactive.interactive()
main_i.start()