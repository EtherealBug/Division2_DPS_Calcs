
# coding: utf-8

# In[81]:


import numpy as np
import matplotlib.pyplot as plot
import pylab
import matplotlib.ticker as mtick

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

### Variable Init ###
spark_bns=0
add_talents=0
talents=0

########################
### USER ENTRY STUFF ###
########################

# Stats
wep_base_dmg=11637
RPM=990
CHC=27.5
CHD=41
HSD=55
mag=50
reload=2.2
AWD=22.5
WTD=49
DTE=92
EAD=0
HD=29
OOC=0

# Talents
p_spotter="n"
p_concussion="y"
p_spark="n"
spark="y"
composure="n"
berserk="y"
merciless_holstered="y"
p_ignited="n"
ignited_freq=5 #How often ignited gets proc'd (in seconds)
strained="n" #Does your weapon have Strained on it?
fast_hands="y" #Does your weapon have Fast Hands on it?
finisher="n" #Is finisher going to be proc'd?
p_finisher="n" #Is perfect finisher going to be proc'd?
perforator="n" #Is the perforator talent going to be proc'd? (Dodge City Holster)

# ENEMY INFO
#Enter "y" if the listed option is what you want to use for your DPS calculation. Enter "n" if not.
elite="y"
armor="n"
enemy_is_in_cover="n"

# EVALUATION VARIABLES
#Enter specific values below to see more specific data
your_armor=100 #Percent of max armor you expect to have on average (100 being full armor). Do not include bonus armor.
f_dur=20 #length of time to evaluate DPS over, in seconds
reload_bonus=0 #reload speed reduction bonus percentage (decimal form)
Headshot_per=0


###############################
### END OF USER ENTRY STUFF ###
###############################

HSR=Headshot_per/100 #DO NOT EDIT
crit_prob=CHC/100 #DO NOT EDIT

# Determine Base Weapon Damage
dmg_bns=wep_base_dmg*((AWD+WTD)/100)
base_dmg=wep_base_dmg+dmg_bns

# Determine Damage Multipliers for Specific Talents
if elite=="n":
    DTE=0
if armor=="n":
    EAD=0
else:
    HD=0
if enemy_is_in_cover=="n":
    OOC=0
if p_spotter=="y":
    p_spotter_bns=20
    talents=talents+p_spotter_bns
if merciless_holstered=="y":
    merciless_passive=(5/100*base_dmg)
else:
    merciless_passive=0
if p_concussion=="y":
    HSD=HSD+20
if p_spark=="y":
    p_spark_bns=15
    add_talents=add_talents+spark_bns
if spark=="y":
    spark_bns=15
    add_talents=add_talents+spark_bns
if composure=="y":
    add_talents=add_talents+10
if p_ignited=="y":
    pyro=40/ignited_freq
    talents=talents+pyro
else:
    pyro=0
if berserk=="y":
    berserk_bns=100-your_armor
    berserk_bns=berserk_bns/20
    berserk_bns=truncate(berserk_bns)*(8)
    add_talents=add_talents+berserk_bns
else:
    berserk=0
if strained=="y":
    st_dmg=(100-your_armor)/10
    st_dmg=truncate(st_dmg)*(5)
    CHD=CHD+st_dmg
else:
    st_dmg=0
if fast_hands=="y":
    rel_bonus=(truncate(crit_prob*mag))
    if rel_bonus>30:
        rel_bonus=30*0.05
    else:
        rel_bonus=rel_bonus*0.05
if perforator=="y":
    add_talents=add_talents+20
if p_finisher=="y":
    CHC=CHC+40
    CHD=CHD+50
if finisher=="y":
    CHC=CHC+30
    CHD=CHD+30
if CHC>60:
    CHC=60
add_talents_bns=(1+(add_talents/100))*wep_base_dmg
fin_base_dmg=base_dmg+add_talents_bns
rel_bonus=rel_bonus+reload_bonus
rel_speed_final=reload-rel_bonus #reload speed with reload speed reduction bonuses

dmg_shot=(fin_base_dmg*(1+((HSD*HSR)+CHD*crit_prob)/100)*(1+(DTE)/100)*(1+(OOC)/100)*(1+(EAD)/100)*(1+(HD)/100))+(1*talents/100)+merciless_passive

DPS=dmg_shot*RPM/60

t_rel=(mag/(RPM/60)) #time to empty magazine
dps_cycle=t_rel+rel_speed_final #time to empty magazine and then complete a reload, in seconds
cycle_ct=f_dur/dps_cycle #number of dps cycles in time=f_dur
t_reloads=cycle_ct*rel_speed_final #total time spent reloading over f_dur
dps_time=f_dur-t_reloads #time spent dealing DPS over f_dur accounting for time lost due to reloads
tot_dmg=DPS*dps_time #total damage dealt over f_dur
avg_dps=tot_dmg/f_dur #average DPS over d_dur accounting for reloads


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

print(color.BOLD + "Average DPS = ",end="")
print (color.RED + "{0:,.1f}".format(DPS))
print(color.END + "\t**Note: This does not take into account loss of damage output due to time spent reloading**" + color.END)
print(color.BOLD + "\nAverage Dmg per Shot = ",end="")
print (color.BLUE + "{0:,.1f}".format(dmg_shot) + color.END)
print(color.BOLD + "\nTotal damage dealt over specified duration = ",end="")
print (color.BLUE + "{0:,.1f}".format(tot_dmg) + color.END)
print(color.BOLD + "Average DPS over specified duration = ",end="")
print (color.RED + "{0:,.1f}".format(avg_dps) + color.END)
print("\t**Note: This takes into account loss of damage output due to time spent reloading**")

print(color.BOLD + "\nAssumptions:")
if elite=="y":
    print(color.YELLOW + "\t(1) Enemy is elite")
else:
    print(color.RED + "\t(1) Enemy is not elite")
print(color.CYAN + "\t(2) All talents are proc'd")
if armor=="y":
    print(color.PURPLE + "\t(3) Enemy is armored")
else:
    print(color.RED + "\t(3) Enemy is unarmored")
    
get_ipython().system('jupyter nbconvert --to script Division_2_DPS_Calcs.ipynb')

