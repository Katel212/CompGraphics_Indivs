import sys
import os

from task2.ui import UI

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == '__main__':
    ui = UI()
    ui.setup_room()
    ui.run()