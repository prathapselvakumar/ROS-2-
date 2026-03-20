import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/student20/assessments/coursework1/install/beta_pilot_controller_pkg'
