import numpy as np
import matplotlib.pyplot as plt

class FusionSim:
    def __init__(self, **kwargs):
        # Initialize simulation parameters with dataset values
        self.params = {
            "magnetic_field_fluctuations": 0.05,
            "leakage": 0.02,
            "instabilities": 0.1,
            "plasma_instabilities": 0.08,
            "magnetic_field_strength": 5.0,  # Tesla
            "magnetic_field_configuration": "tokamak",
            "injection_energy": 100.0,  # keV
            "beam_symmetry": 0.95,
            "target_density": 1.0e20,  # particles/m^3
            "target_composition": "D-T",
            "fuel_density": 5.0e20,  # particles/m^3
            "temperature": 150e6,  # Kelvin
            "confinement_time": 1.0,  # seconds
            "fuel_purity": 0.98,
            "energy_input": 200.0,  # Megawatts (MW)
            "power_output": 0.0,  # MW (to be computed)
            "pressure": 3.0,  # atm
            "neutron_yield": 0.0,  # to be computed
            "ignition": 0  # 1 if ignition is achieved, otherwise 0
        }
        
        # Update parameters with user input
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value

    def compute_power_output(self):
        """Compute power output based on temperature, density, and confinement time."""
        efficiency_factor = self.params["fuel_purity"] * (1 - self.params["leakage"]) * self.params["beam_symmetry"]
        fusion_rate = self.params["target_density"] * self.params["fuel_density"] * np.exp(-1e-8 / self.params["temperature"])
        self.params["power_output"] = efficiency_factor * fusion_rate * self.params["energy_input"]
        return self.params["power_output"]
    
    def compute_neutron_yield(self):
        """Estimate neutron yield using a more realistic formula."""
        self.params["neutron_yield"] = self.params["power_output"] * 1e10  # Adjusted for realism
        return self.params["neutron_yield"]
    
    def check_ignition(self):
        """Determine if ignition is achieved (returns 1 for ignition, 0 otherwise)."""
        self.params["ignition"] = int(self.params["power_output"] >= self.params["energy_input"])
        return self.params["ignition"]

    def run_simulation(self):
        """Run the fusion simulation and compute key outputs."""
        self.compute_power_output()
        self.compute_neutron_yield()
        self.check_ignition()
        
        print("Simulation Results:")
        for key, value in self.params.items():
            print(f"{key}: {value}")
        return self.params
    
    def plot_results(self):
        """Visualize key fusion parameters with proper scaling."""
        keys = ["temperature", "fuel_density", "confinement_time", "energy_input", "power_output", "neutron_yield"]
        values = [self.params[k] for k in keys]

        # Normalize values for better visualization
        values = np.log10(np.array(values) + 1)  # log scaling to prevent extreme values

        plt.figure(figsize=(10, 5))
        plt.bar(keys, values, color='blue')
        plt.ylabel("Log10 Scale of Magnitude")
        plt.title("Fusion Simulation Results")
        plt.xticks(rotation=45)
        plt.show()

# Results with column diagram (column chart)
fusion_sim = FusionSim(temperature=200e6, energy_input=250.0)
fusion_sim.run_simulation()
fusion_sim.plot_results()
