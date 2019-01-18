import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
from matplotlib.colors import LogNorm
from scipy import signal
import random as rd
from Object import *
from In_Terface_Temporal import *


scale = 5

in_terface = In_Terface_Temporal()
in_terface.initialize_interface()