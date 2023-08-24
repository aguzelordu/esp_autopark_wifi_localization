#Empty slots and nodes taken from image processing will be processed separately.
#The (x,y) data received from the RSSI will determine which slot it is in to calculate the distance.

import math
import pandas as pd

with open("xy_datas.txt", "r") as file:
    content = file.read()
    
rows = content.split("\n")
x0 = float(rows[0])
y0 = float(rows[1])


empty_slot = []
full_slot = []
empty_node = []
full_node = []

s_dist = []
n_dist = []

temp = []

nodes = {"s1": (88, 47), "s2": (66, 47), "s3": (15, 37), "s4": (15, 61),
           "s5": (15, 87), "s6": (15, 112), "s7": (66, 115), "s8": (88, 115),
           "s9": (135, 112), "s10": (135, 87), "s11": (135, 61), "s12": (135, 37),
           "n1": (75, 0), "n2": (66, 20), "n3": (39, 16), "n4": (39, 37),
           "n5": (39, 61), "n6": (39, 87), "n7": (39, 112), "n8": (39, 139),
           "n9": (66, 139), "n10": (88, 139), "n11": (110, 139), "n12": (110, 112),
           "n13": (110, 87), "n14": (110, 61), "n15": (110, 37), "n16": (110, 16),
           "n17": (88, 20), "n18": (88, 82), "n19": (66, 82)}

img_slot = list(("s6", "s7", "s9", "s10")) 

#Slot datas from image processing.
#Location datas received via RSSI.


"""   ------------------------still developing part-----------------------
def target_park():
    for s in img_slot:
        if s in slots:
            empty_slot.append(s)
            
    print("Empty Slots:", empty_slot)
    
    for es in empty_slot:
        m = math.sqrt((slotlar[es][0] - x0)**2 + (slotlar[es][1] - y0)**2)
        s_dist.append(m)
        
    print(s_dist)
    target = s_dist.index(min(s_dist))
    print(empty_slot[target])
   """    
    
def locate():
    """Find our location"""
    for n in nodes.items():
        temp.append(n)
        m = math.sqrt((n[1][0] - x0)**2 + (n[1][1] - y0)**2)
        n_dist.append(m)
    
    #print(n_mesafeler)
    my_loc = n_dist.index(min(n_dist))
    print(temp[my_loc][0])


locate()