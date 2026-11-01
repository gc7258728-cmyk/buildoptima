"""Elementary Euler-Bernoulli beam models. Loads are characteristic/service loads, not ULS combinations."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Beam:
 span_m:float
 width_m:float
 depth_m:float
 e_gpa:float=30.0
 udl_kn_m:float=15.0
 point_kn:float=0.0
 point_x_m:float=0.0
 support:str="Simplement appuyée"

 def validate(self):
  if not 0.2<=self.span_m<=40:raise ValueError("Portée entre 0,2 et 40 m.")
  if not 0.05<=self.width_m<=3 or not 0.08<=self.depth_m<=4:raise ValueError("Dimensions de section hors limites.")
  if not 1<=self.e_gpa<=250:raise ValueError("Module E hors limites.")
  if not 0<=self.udl_kn_m<=500 or not 0<=self.point_kn<=10000:raise ValueError("Charges hors limites.")
  if not 0<=self.point_x_m<=self.span_m:raise ValueError("Position de charge hors portée.")
  if self.support not in ("Simplement appuyée","Console"):raise ValueError("Type d'appui inconnu.")

def analyze(b,n=401):
 b.validate()
 L=b.span_m;q=b.udl_kn_m;P=b.point_kn;a=b.point_x_m
 x=np.linspace(0,L,n);I=b.width_m*b.depth_m**3/12
 EI=b.e_gpa*1e6*I # kN/m² * m4 -> kN m²
 if b.support=="Simplement appuyée":
  rb=q*L/2+P*a/L;ra=q*L+P-rb
  V=ra-q*x-P*(x>=a)
  M=ra*x-q*x*x/2-P*np.maximum(x-a,0)
  # EIy = ra*x^3/6 - q*x^4/24 - P*<x-a>^3/6 + C1*x, C1 from y(L)=0
  c1=-(ra*L**3/6-q*L**4/24-P*(L-a)**3/6)/L
  y=(ra*x**3/6-q*x**4/24-P*np.maximum(x-a,0)**3/6+c1*x)/EI
  reactions={"RA":float(ra),"RB":float(rb)}
 else:
  # Console clamped x=0, free at x=L
  ra=q*L+P
  V=ra-q*x-P*(x>=a)
  M=-(q*(L-x)**2/2+P*np.maximum(a-x,0))
  # displacement from integrating M/EI twice, zero at x=0
  y=-(q*x*x*(6*L*L-4*L*x+x*x)/24 + P*(x*x*(3*a-x)/6)*(x<=a)
      +P*(a*a*(3*x-a)/6)*(x>a))/EI
  reactions={"RA":float(ra),"M_encastrement":float(q*L*L/2+P*a)}
 return {"x":x,"V":V,"M":M,"y_mm":y*1000,"inertia_m4":I,"volume_m3":b.width_m*b.depth_m*L,
         "m_max":float(np.max(np.abs(M))),"v_max":float(max(abs(V.min()),abs(V.max()))),
         "deflection_mm":float(np.max(np.abs(y))*1000),"reactions":reactions}
def rectangular_section_modulus(b,h):
 if b<=0 or h<=0:raise ValueError("Dimensions positives requises.")
 return b*h*h/6
