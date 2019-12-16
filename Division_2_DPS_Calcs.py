
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plot
import pylab
import matplotlib.ticker as mtick

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

# Stats
base_dmg=19957
RPM=990
Headshot_per=100
HSR=Headshot_per/100
CHC=38
crit_prob=CHC/100
CHD=41
HSD=55
reload=2.4
AWD=22.5
WTD=49
DTE=92
EAD=0
HD=29
OOC=0

# Talents
p_concussion="y"
spark="y"
composure="y"
berserk=100 # percentage of max armor depleted

merciless_passive=(1+5/100*base_dmg)

berserk=berserk/20
berserk=truncate(berserk)*(8)
AWD=AWD+berserk

if p_concussion=="y":
    HSD=HSD+20
if spark=="y":
    AWD=AWD+15
if composure=="y":
    AWD=AWD+10

talents=merciless_passive

dmg_shot=base_dmg*(1+(AWD+WTD)/100)*(1+((HSD*HSR)+CHD*crit_prob)/100)*(1+(DTE)/100)*(1+(OOC)/100)*(1+(EAD)/100)*(1+(HD)/100)*talents

DPS=dmg_shot*RPM/60

print("DPS = ",end="")
print ("{0:,.1f}".format(DPS))
print("Assumptions: \n\t(1) Enemy is elite \n\t(2) All talents are proc'd \n\t(3) Enemy armor is 0")

