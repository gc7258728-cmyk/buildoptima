"""Geometric section properties; pure geometry, not reinforced concrete design."""
import math

def rectangle(b,h):
    if b<=0 or h<=0: raise ValueError('Dimensions positives requises.')
    return {'aire_m2':b*h,'ix_m4':b*h**3/12,'iy_m4':h*b**3/12,
            'wx_m3':b*h*h/6,'wy_m3':h*b*b/6,'rayon_giration_x_m':h/math.sqrt(12)}

def circle(d):
    if d<=0: raise ValueError('Diamètre positif requis.')
    return {'aire_m2':math.pi*d*d/4,'ix_m4':math.pi*d**4/64,
            'wx_m3':math.pi*d**3/32,'rayon_giration_m':d/4}

def hollow_rectangle(b,h,bi,hi):
    if not 0<bi<b or not 0<hi<h:raise ValueError('Dimensions intérieures inférieures aux extérieures.')
    area=b*h-bi*hi
    ix=(b*h**3-bi*hi**3)/12
    iy=(h*b**3-hi*bi**3)/12
    return {'aire_m2':area,'ix_m4':ix,'iy_m4':iy,'wx_m3':2*ix/h,'wy_m3':2*iy/b}
