import sys,unittest,io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import pandas as pd
from dimensia.datasets import load_table,audit,numeric_stats,linear_fit
from dimensia.loads import LoadCombination
from dimensia.sections import rectangle,circle,hollow_rectangle
class Extensions(unittest.TestCase):
 def test_csv(self):
  df=load_table(b'x,y\n1,2\n2,4\n3,6\n4,8\n','test.csv')
  self.assertEqual(len(df),4)
  self.assertEqual(int(audit(df).manquants.sum()),0)
  self.assertAlmostEqual(float(numeric_stats(df).loc['x','mean']),2.5)
 def test_regression(self):
  d=pd.DataFrame({'x':[1,2,3,4],'y':[2,4,6,8]})
  fit,_=linear_fit(d,'x','y')
  self.assertAlmostEqual(fit['pente'],2)
  self.assertAlmostEqual(fit['r2'],1)
 def test_invalid(self):
  with self.assertRaises(ValueError):load_table(b'abc','test.exe')
  with self.assertRaises(ValueError):load_table(b'','test.csv')
 def test_loads(self):
  self.assertEqual(LoadCombination(10,5,1.35,1.5).evaluate()['q_combine (kN/m)'],21)
 def test_sections(self):
  self.assertAlmostEqual(rectangle(.2,.3)['aire_m2'],.06)
  self.assertAlmostEqual(circle(2)['aire_m2'],3.141592653589793)
  self.assertAlmostEqual(hollow_rectangle(.4,.6,.2,.3)['aire_m2'],.18)
if __name__=='__main__':unittest.main()
