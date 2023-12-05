import ast
from inspect import getsource, signature
from pathlib import Path
from copy import deepcopy
from unittest import mock
import pytest
from pprint import pformat
import random
            
try:
    import funcoes
except:
    funcoes = None
