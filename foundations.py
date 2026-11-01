"""Centered footing sizing under a vertical service load; simplified bearing-pressure check only."""
import math
def centered_footing(load_kn,allowable_kpa,ratio=1.0,footing_depth_m=0.45,unit_weight_kn_m3=24.0,include_self_weight=True):
 if not 0<load_kn<=1e7 or not 1<=allowable_kpa<=5000 or not .3<=ratio<=4:raise ValueError("Charge, portance ou ratio hors limites.")
 if not .1<=footing_depth_m<=3 or not 10<=unit_weight_kn_m3<=40:raise ValueError("Épaisseur ou poids volumique hors limites.")
 net=allowable_kpa-(unit_weight_kn_m3*footing_depth_m if include_self_weight else 0)
 if net<=0:raise ValueError("Portance insuffisante après prise en compte du poids propre.")
 area=load_kn/net
 width=math.sqrt(area/ratio);length=width*ratio
 actual=(load_kn+unit_weight_kn_m3*footing_depth_m*area if include_self_weight else load_kn)/area
 return {"area_m2":area,"width_m":width,"length_m":length,"bearing_kpa":actual,"allowable_kpa":allowable_kpa}
