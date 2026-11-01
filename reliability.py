"""Illustrative probability of exceeding an explicit mechanical threshold, NOT code reliability."""
import numpy as np
from .mechanics import Beam,analyze
def sample_udl_limit(beam,threshold_knm,cv=0.15,n=10000,seed=42):
 beam.validate()
 if beam.point_kn:raise ValueError("Simulation disponible uniquement pour une charge répartie (P=0).")
 if not 0<=cv<=1 or not 100<=n<=100000 or threshold_knm<=0:raise ValueError("Paramètres de simulation invalides.")
 rng=np.random.default_rng(int(seed))
 # Positive lognormal, mean = specified characteristic input for this teaching model
 sig=np.sqrt(np.log1p(cv*cv));mu=np.log(max(beam.udl_kn_m,1e-9))-sig*sig/2
 q=rng.lognormal(mu,sig,n)
 m=q*beam.span_m**2/(8 if beam.support=="Simplement appuyée" else 2)
 p=float(np.mean(m>threshold_knm))
 return {"moments":m,"probability":p,"mc_se":float(np.sqrt(p*(1-p)/n)),"p95":float(np.quantile(m,.95))}
