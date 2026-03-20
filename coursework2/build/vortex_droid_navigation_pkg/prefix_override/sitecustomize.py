import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/student20/Downloads/coursework2/install/vortex_droid_navigation_pkg'
