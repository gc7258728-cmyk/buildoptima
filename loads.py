"""User-defined combination of permanent and variable loads.

Factors are not claimed to represent BAEL or EC2 normative coefficients.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class LoadCombination:
    permanent_kn_m: float
    variable_kn_m: float
    gamma_g: float
    gamma_q: float

    def evaluate(self):
        values=(self.permanent_kn_m,self.variable_kn_m,self.gamma_g,self.gamma_q)
        if any(v<0 or v>10000 for v in values):
            raise ValueError('Charges et coefficients entre 0 et 10 000.')
        return {
            'G (kN/m)': self.permanent_kn_m,
            'Q (kN/m)': self.variable_kn_m,
            'gamma_G': self.gamma_g,
            'gamma_Q': self.gamma_q,
            'q_combine (kN/m)': self.gamma_g*self.permanent_kn_m+self.gamma_q*self.variable_kn_m,
        }
