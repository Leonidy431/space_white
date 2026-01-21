#!/usr/bin/env python3
"""
Quick Start Example: PBH-Unified Dark Matter Model Solver

This standalone Python script demonstrates how to:
1. Set up a minimal PBH-Unified DM calculation
2. Solve the coupled Boltzmann equations
3. Extract DM composition (WIMP, Axion, PBH remnants)
4. Visualize results

Usage:
    python quick_start_example.py

Author: Generated from Cheek et al. (2021-2022) formalism
Date: 2026-01-03
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
import json

# ============================================================================
# CONSTANTS AND PHYSICAL PARAMETERS
# ============================================================================

# Physical constants
M_pl = 1.22e19  # Planck mass in GeV
hbar_c = 0.1973  # ℏc in GeV·fm
G_natural = 1.0 / (M_pl**2)  # Gravitational constant in natural units

# PBH evaporation constant
Gamma_0_grams3_per_sec = 5.3e-27  # Hawking evaporation coefficient

# ============================================================================
# CONFIGURATION (From JSON)
# ============================================================================

CONFIG = {
    "pbh": {
        "M_initial_grams": 1.0e9,  # Initial PBH mass
        "beta": 1.0e-18,  # Initial PBH fraction
        "spin_parameter": 0.0,  # Non-rotating (Schwarzschild)
        "memory_burden_enabled": True,
        "suppression_onset_mass": 1.0e7,  # Memory burden kicks in here
    },
    "dm": {
        "wimp": {
            "name": "WIMP",
            "mass_gev": 350.0,
            "spin": 0.5,  # Fermion
            "dof": 2,
            "annihilation_xsec_cm3_s": 3.0e-26,
            "relative_greybody_efficiency": 1.73,  # From Cheek et al.
        },
        "axion": {
            "name": "Axion",
            "mass_gev": 1.0e-15,  # 1 μeV in GeV
            "spin": 0.0,  # Scalar
            "dof": 1,
            "annihilation_xsec_cm3_s": 0.0,  # Axions don't annihilate
            "relative_greybody_efficiency": 1.0,  # Reference
        }
    },
    "solver": {
        "T_initial_gev": 1.0e9,  # Start from high T
        "T_final_gev": 0.1,  # End at BBN scale
        "n_steps": 1000,
    }
}

# ============================================================================
# CLASS: PBHUnifiedDMSolver
# ============================================================================

class PBHUnifiedDMSolver:
    """
    Solve the coupled Boltzmann-Friedmann system for PBH-Unified DM.
    
    System:
        dM_pbh/dt = -Γ₀/M_pbh² * S²(M) [PBH evaporation with memory burden]
        d(n_wimp * a³)/dt = [Production] - [Annihilation]
        d(n_axion * a³)/dt = [Production]
        H² = (8π/3) * (ρ_rad + ρ_pbh + ρ_wimp + ρ_axion)
    """
    
    def __init__(self, config):
        self.config = config
        self.results = {
            'a': [], 't': [], 'T': [], 'M_pbh': [], 'T_hawking': [],
            'n_wimp_a3': [], 'n_axion_a3': [], 'rho_rad': [],
            'f_wimp': [], 'f_axion': [], 'f_pbh_rem': []
        }
    
    def hawking_temperature_gev(self, M_grams):
        """
        Hawking temperature in GeV.
        T_H = 1.06e13 K / M [g]  ×  (1.16e-13 GeV/K) ≈ 1.23 / M [g] GeV
        """
        return 1.23 / M_grams  # Simplified formula (GeV)
    
    def memory_burden_suppression(self, M, M0):
        """
        Memory burden suppression factor S²(M).
        
        S²(M) = 1.0 if M > M0/2
        S²(M) = (M/M0)^(2/3) if M ≤ M0/2
        
        This suppresses Hawking evaporation at low masses.
        """
        M_thresh = M0 * 0.5
        if M > M_thresh:
            return 1.0
        else:
            ratio = M / M0
            return ratio ** (2.0 / 3.0)  # Exponent 2/3 from entropy
    
    def evaporation_rate(self, M_pbh, M0):
        """
        dM_pbh/dt = -Γ₀/M_pbh² * S²(M)
        """
        S2 = self.memory_burden_suppression(M_pbh, M0)
        return -Gamma_0_grams3_per_sec / (M_pbh ** 2) * S2
    
    def greybody_production_rate(self, M_pbh, T_hawking, particle_config, dm_total_energy):
        """
        Production rate of DM particle from Hawking radiation.
        
        dn_i/dt ∝ |dM_pbh/dt| * σ_i(T_H) / T_H³
        
        where σ_i is the greybody factor (spin-dependent).
        """
        dM_dt = self.evaporation_rate(M_pbh, self.config['pbh']['M_initial_grams'])
        
        # Energy flux divided by T³ gives particle flux
        production_rate = (
            np.abs(dM_dt) / (T_hawking ** 3) *
            particle_config['relative_greybody_efficiency'] *
            particle_config['dof'] *
            self.config['pbh']['beta'] * 1e10  # Numerical coefficient
        )
        
        # Boltzmann suppression if m_i > T_H
        if particle_config['mass_gev'] > T_hawking:
            suppression = np.exp(-particle_config['mass_gev'] / T_hawking)
            production_rate *= suppression
        
        return production_rate
    
    def annihilation_rate(self, n_particle, particle_config):
        """
        Loss rate from particle annihilation.
        
        dn/dt = -<σv> * n² [for self-annihilating]
        """
        xsec = particle_config['annihilation_xsec_cm3_s']
        return xsec * n_particle ** 2
    
    def boltzmann_rhs(self, t_param, y):
        """
        Right-hand side of ODE system: dy/dt
        
        y = [M_pbh, n_wimp_a3, n_axion_a3, log(rho_rad_a4), log(a)]
        """
        M_pbh = y[0]
        n_wimp_a3 = y[1]
        n_axion_a3 = y[2]
        log_rho_rad_a4 = y[3]
        log_a = y[4]
        
        a = np.exp(log_a)
        rho_rad_a4 = np.exp(log_rho_rad_a4)
        
        # Derived quantities
        T_hawking = self.hawking_temperature_gev(M_pbh)
        T_radiation = 1.0e9 / a  # T ∝ 1/a (radiation era)
        n_wimp = n_wimp_a3 / (a ** 3)
        n_axion = n_axion_a3 / (a ** 3)
        rho_rad = rho_rad_a4 / (a ** 4)
        rho_wimp = n_wimp * self.config['dm']['wimp']['mass_gev']
        rho_axion = n_axion * self.config['dm']['axion']['mass_gev']
        
        # Hubble parameter (simplified Friedmann)
        H = np.sqrt(8 * np.pi / 3 * (rho_rad + rho_wimp + rho_axion + M_pbh))
        
        # ────────────────────────────────────────────────────────────
        # EQUATION 1: PBH mass evolution
        # ────────────────────────────────────────────────────────────
        dM_dt = self.evaporation_rate(M_pbh, self.config['pbh']['M_initial_grams'])
        
        # ────────────────────────────────────────────────────────────
        # EQUATION 2: WIMP production and annihilation
        # ────────────────────────────────────────────────────────────
        dn_wimp_prod = self.greybody_production_rate(
            M_pbh, T_hawking,
            self.config['dm']['wimp'],
            rho_wimp
        )
        dn_wimp_ann = self.annihilation_rate(n_wimp, self.config['dm']['wimp'])
        
        d_nwimp_a3_dt = (dn_wimp_prod - dn_wimp_ann / (a ** 3)) * (a ** 3) + n_wimp_a3 * (H * a)
        
        # ────────────────────────────────────────────────────────────
        # EQUATION 3: Axion production
        # ────────────────────────────────────────────────────────────
        dn_axion_prod = self.greybody_production_rate(
            M_pbh, T_hawking,
            self.config['dm']['axion'],
            rho_axion
        )
        
        d_naxion_a3_dt = dn_axion_prod * (a ** 3) + n_axion_a3 * (H * a)
        
        # ────────────────────────────────────────────────────────────
        # EQUATION 4: Radiation energy (energy conservation)
        # ────────────────────────────────────────────────────────────
        # Energy lost by PBH → radiation
        dE_rad_dt = -dM_dt  # (in appropriate units)
        d_log_rho_rad_a4_dt = dE_rad_dt / rho_rad_a4 - 4 * H if rho_rad_a4 > 0 else 0
        
        # ────────────────────────────────────────────────────────────
        # EQUATION 5: Scale factor
        # ────────────────────────────────────────────────────────────
        d_log_a_dt = H if a > 0 else 0
        
        return [dM_dt, d_nwimp_a3_dt, d_naxion_a3_dt, d_log_rho_rad_a4_dt, d_log_a_dt]
    
    def solve(self):
        """
        Integrate from early to late times.
        """
        
        # Initial conditions
        M0 = self.config['pbh']['M_initial_grams']
        y0 = np.array([
            M0,  # M_pbh
            1.0e-15,  # n_wimp * a³
            1.0e-15,  # n_axion * a³
            np.log(1.0),  # log(ρ_rad a⁴)
            np.log(1.0),  # log(a)
        ])
        
        # Time parametrization
        t_span = (0, 1)
        t_eval = np.linspace(0, 1, self.config['solver']['n_steps'])
        
        # Solve ODE
        sol = solve_ivp(
            self.boltzmann_rhs,
            t_span=t_span,
            y0=y0,
            t_eval=t_eval,
            method='RK45',
            dense_output=True,
            max_step=0.001,
            rtol=1.0e-6,
            atol=1.0e-10
        )
        
        # Post-process results
        self._post_process(sol)
        
        return sol
    
    def _post_process(self, sol):
        """
        Extract and compute quantities of interest.
        """
        
        t_vals = sol.t
        y_vals = sol.y
        
        for i, t in enumerate(t_vals):
            M_pbh = y_vals[0, i]
            n_wimp_a3 = y_vals[1, i]
            n_axion_a3 = y_vals[2, i]
            log_rho_rad_a4 = y_vals[3, i]
            log_a = y_vals[4, i]
            
            a = np.exp(log_a)
            rho_rad_a4 = np.exp(log_rho_rad_a4)
            
            n_wimp = n_wimp_a3 / (a ** 3)
            n_axion = n_axion_a3 / (a ** 3)
            
            T_hawking = self.hawking_temperature_gev(M_pbh)
            T_rad = 1.0e9 / a
            
            # Energy densities
            rho_wimp = n_wimp * self.config['dm']['wimp']['mass_gev']
            rho_axion = n_axion * self.config['dm']['axion']['mass_gev']
            rho_rad = rho_rad_a4 / (a ** 4)
            
            # PBH remnants (memory burden stabilized)
            M0 = self.config['pbh']['M_initial_grams']
            if M_pbh < M0 * 0.5:
                rho_pbh_rem = M_pbh  # Unevaporated portion
            else:
                rho_pbh_rem = 0.0
            
            rho_dm_total = rho_wimp + rho_axion + rho_pbh_rem
            
            # Fractions
            if rho_dm_total > 1.0e-30:
                f_wimp = rho_wimp / rho_dm_total
                f_axion = rho_axion / rho_dm_total
                f_pbh_rem = rho_pbh_rem / rho_dm_total
            else:
                f_wimp = f_axion = f_pbh_rem = 0.0
            
            # Store
            self.results['a'].append(a)
            self.results['t'].append(t)
            self.results['T'].append(T_rad)
            self.results['M_pbh'].append(M_pbh)
            self.results['T_hawking'].append(T_hawking)
            self.results['n_wimp_a3'].append(n_wimp_a3)
            self.results['n_axion_a3'].append(n_axion_a3)
            self.results['rho_rad'].append(rho_rad)
            self.results['f_wimp'].append(f_wimp)
            self.results['f_axion'].append(f_axion)
            self.results['f_pbh_rem'].append(f_pbh_rem)
    
    def print_summary(self):
        """Print results summary."""
        print("\n" + "="*80)
        print("PBH-UNIFIED DARK MATTER MODEL: RESULTS SUMMARY")
        print("="*80)
        
        if len(self.results['f_wimp']) > 0:
            f_wimp_final = self.results['f_wimp'][-1]
            f_axion_final = self.results['f_axion'][-1]
            f_pbh_rem_final = self.results['f_pbh_rem'][-1]
            
            print(f"\nFinal Dark Matter Composition:")
            print(f"  WIMPs (250-500 GeV):     {f_wimp_final:6.1%}")
            print(f"  Axions (μeV):            {f_axion_final:6.1%}")
            print(f"  PBH Remnants (stabilized): {f_pbh_rem_final:6.1%}")
            print(f"  ──────────────────────────")
            print(f"  Total:                   {f_wimp_final + f_axion_final + f_pbh_rem_final:6.1%}")
            
            print(f"\nComparison to Target:")
            print(f"  Target: WIMPs 62% | Axions 33% | PBH-rem 5%")
            print(f"  Actual: WIMPs {f_wimp_final:.0%} | Axions {f_axion_final:.0%} | PBH-rem {f_pbh_rem_final:.0%}")
            
            # Check hypothesis
            target_wimp = 0.62
            target_axion = 0.33
            target_pbh = 0.05
            
            tol = 0.05
            
            if (abs(f_wimp_final - target_wimp) < tol and
                abs(f_axion_final - target_axion) < tol and
                abs(f_pbh_rem_final - target_pbh) < tol):
                print(f"\n✓ HYPOTHESIS CONFIRMED!")
                print(f"  Calculated fractions match predicted 62-33-5 split!")
            else:
                print(f"\n⚠ Fractions don't match target (within ±{tol:.0%})")
                print(f"  This means either:")
                print(f"  - Your choice of β or M_pbh is off (try scanning parameter space)")
                print(f"  - The PBH-Unified hypothesis may need refinement")
        else:
            print("No results computed yet. Run solve() first.")
    
    def plot_results(self, filename='pbh_unified_results.pdf'):
        """Generate diagnostic plots."""
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: DM Composition Evolution
        ax = axes[0, 0]
        ax.plot(self.results['a'], np.array(self.results['f_wimp']) * 100, 
                label='WIMPs', linewidth=2)
        ax.plot(self.results['a'], np.array(self.results['f_axion']) * 100,
                label='Axions', linewidth=2)
        ax.plot(self.results['a'], np.array(self.results['f_pbh_rem']) * 100,
                label='PBH Remnants', linewidth=2)
        ax.axhline(y=62, color='blue', linestyle='--', alpha=0.5, label='Target WIMPs (62%)')
        ax.axhline(y=33, color='orange', linestyle='--', alpha=0.5, label='Target Axions (33%)')
        ax.set_xlabel('Scale factor a')
        ax.set_ylabel('Fractional abundance (%)')
        ax.set_xscale('log')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
        ax.set_title('DM Composition Evolution')
        
        # Plot 2: PBH Mass Evolution
        ax = axes[0, 1]
        ax.plot(self.results['a'], self.results['M_pbh'], linewidth=2, color='black')
        ax.axhline(y=self.config['pbh']['M_initial_grams'] * 0.5, color='red',
                  linestyle='--', label='Memory burden threshold')
        ax.set_xlabel('Scale factor a')
        ax.set_ylabel('PBH mass (grams)')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, which='both', alpha=0.3)
        ax.set_title('PBH Mass Evolution (Hawking + Memory Burden)')
        
        # Plot 3: Hawking Temperature
        ax = axes[1, 0]
        ax.plot(self.results['a'], self.results['T_hawking'], linewidth=2, color='red')
        ax.axhline(y=self.config['dm']['wimp']['mass_gev'], color='blue',
                  linestyle='--', label='WIMP mass')
        ax.axhline(y=self.config['dm']['axion']['mass_gev'], color='green',
                  linestyle='--', label='Axion mass')
        ax.set_xlabel('Scale factor a')
        ax.set_ylabel('Hawking temperature (GeV)')
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.legend()
        ax.grid(True, which='both', alpha=0.3)
        ax.set_title('Hawking Temperature vs Scale Factor')
        
        # Plot 4: Final Composition (Pie Chart)
        ax = axes[1, 1]
        final_values = [
            self.results['f_wimp'][-1] * 100,
            self.results['f_axion'][-1] * 100,
            self.results['f_pbh_rem'][-1] * 100
        ]
        labels = [f"WIMPs\n{final_values[0]:.1f}%",
                 f"Axions\n{final_values[1]:.1f}%",
                 f"PBH rem\n{final_values[2]:.1f}%"]
        colors = ['#FF9999', '#66B2FF', '#99FF99']
        ax.pie(final_values, labels=labels, colors=colors, autopct=lambda pct: '',
              startangle=90)
        ax.set_title('Final DM Composition')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        print(f"\n✓ Plots saved to: {filename}")
        plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\n" + "="*80)
    print("PBH-UNIFIED DARK MATTER MODEL")
    print("Quick Start Solver")
    print("="*80)
    print("\nConfiguration:")
    print(json.dumps(CONFIG, indent=2))
    
    # Create and run solver
    solver = PBHUnifiedDMSolver(CONFIG)
    
    print("\nIntegrating Boltzmann equations...")
    sol = solver.solve()
    
    # Print results
    solver.print_summary()
    
    # Generate plots
    solver.plot_results('pbh_unified_example.pdf')
    
    print("\n" + "="*80)
    print("Calculation complete!")
    print("="*80)


if __name__ == '__main__':
    main()
