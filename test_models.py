import sys,unittest,io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dimensia.mechanics import Beam,analyze
from dimensia.foundations import centered_footing
from dimensia.reliability import sample_udl_limit
from dimensia.optimization import search
from dimensia.reports import pdf
class Models(unittest.TestCase):
 def test_simple(self):
  b=Beam(5,.25,.45,30,20,0,2.5);r=analyze(b)
  self.assertAlmostEqual(r['m_max'],62.5,places=3)
  self.assertAlmostEqual(r['v_max'],50,places=3)
  self.assertAlmostEqual(r['reactions']['RA'],50)
  self.assertAlmostEqual(r['deflection_mm'],5*20*5**4/(384*(30e6*.25*.45**3/12))*1000,places=2)
 def test_point(self):
  r=analyze(Beam(6,.3,.5,30,0,30,3));self.assertAlmostEqual(r['m_max'],45,places=2)
  self.assertAlmostEqual(r['reactions']['RA'],15)
 def test_cantilever(self):
  r=analyze(Beam(3,.3,.5,30,10,0,0,'Console'))
  self.assertAlmostEqual(r['m_max'],45)
  self.assertAlmostEqual(r['deflection_mm'],10*3**4/(8*(30e6*.3*.5**3/12))*1000,places=3)
 def test_cantilever_point(self):
  b=Beam(3,.3,.5,30,0,20,3,'Console');r=analyze(b)
  self.assertAlmostEqual(r['m_max'],60)
  self.assertAlmostEqual(r['deflection_mm'],20*3**3/(3*30e6*(.3*.5**3/12))*1000,places=2)
 def test_footing(self):
  r=centered_footing(900,200,1,.45);self.assertAlmostEqual(r['bearing_kpa'],200)
  self.assertAlmostEqual(r['width_m'],r['length_m'])
 def test_reliability(self):
  b=Beam(5,.25,.45,30,20,0,0)
  r=sample_udl_limit(b,62.5,.2,10000,42)
  self.assertEqual(r['probability'],sample_udl_limit(b,62.5,.2,10000,42)['probability'])
  self.assertTrue(0<r['probability']<1)
 def test_optimize(self):
  r=search(Beam(5,.25,.45,30,20,0,0),[.2,.25],[.4,.45],100,100)
  self.assertEqual(len(r),4)
 def test_pdf(self):
  self.assertTrue(pdf('Poutre',{'L':5},{'M':62.5},'Limites').startswith(b'%PDF'))
 def test_validation(self):
  with self.assertRaises(ValueError):analyze(Beam(-1,.2,.3))
  with self.assertRaises(ValueError):centered_footing(100,5,1,1)
if __name__=='__main__':unittest.main()
