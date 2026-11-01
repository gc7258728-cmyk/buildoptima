"""Educational serviceability screening; NOT normative reinforced-concrete sizing."""
from .mechanics import Beam,analyze
def search(base,widths,depths,deflection_limit_mm,moment_limit_knm):
 if deflection_limit_mm<=0 or moment_limit_knm<=0:raise ValueError("Limites strictement positives.")
 rows=[]
 for width in widths:
  for depth in depths:
   try:
    b=Beam(base.span_m,float(width),float(depth),base.e_gpa,base.udl_kn_m,base.point_kn,base.point_x_m,base.support)
    a=analyze(b)
    # Moment resistance threshold is externally provided, not derived from dimensions.
    ok=a["deflection_mm"]<=deflection_limit_mm and a["m_max"]<=moment_limit_knm
    rows.append({"largeur_cm":round(width*100,1),"hauteur_cm":round(depth*100,1),
                 "volume_m3":round(a["volume_m3"],4),"fleche_mm":round(a["deflection_mm"],3),
                 "moment_knm":round(a["m_max"],3),"admissible_selon_criteres_saisis":ok})
   except ValueError:pass
 return sorted(rows,key=lambda x:x["volume_m3"])
