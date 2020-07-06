# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 15:48:22 2020

@author: tilan
"""


import numpy as np
import pandas as pd

import main



# Fixing random state for reproducibility
np.random.seed(19680801)



dfStudentDetails = main.getStudentDetails()



#---------------------------------
# school selection
def BuildOptions(options):  
    return [{'label': i, 'value': i} for i in options]


GroupSelector_options = BuildOptions(dfStudentDetails['GroupId'].unique())

