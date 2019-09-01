# -*- coding: utf-8 -*-
import os
import sys
from dotenv import load_dotenv

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '..\kabuthon'))

load_dotenv(verbose=True)