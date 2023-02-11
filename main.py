import sys
import time
import pyfiglet
def slowprint(s):
	for c in s + '\n':
		sys.stdout.write(c)
		sys.stdout.flush()
		time.sleep(1./1000)
def ascii(input):
    result= pyfiglet.figlet_format(input)
    return result
### formatting functions
results = ascii("Omega")
print(results)
slowprint("Version 1.0 Alpha")
##########################################################
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import ta
import pandas_ta as pta
from finta import TA


df = yf.download("AAPL", start="2020-01-01", end="2020-12-31")

df.plot()
plt.show()
