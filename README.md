# ChemST 🧪
> **Smart Chemical Solution & Stoichiometry Engine for Python**

[![PyPI version](https://img.shields.io/pypi/v/chemst.svg)](https://pypi.org/project/chemst/)
[![Python Versions](https://img.shields.io/pypi/pyversions/chemst.svg)](https://pypi.org/project/chemst/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ChemST** is a lightweight, high-precision Python library designed for computational chemists, laboratory researchers, and students. It automates complex stoichiometry calculations, hydration adjustments, dilution protocols, and concentrated acid/base preparations while seamlessly integrating with the **PubChem REST API** to retrieve live molecular properties.

---

## 🌟 Key Features

* **⚡ Live PubChem REST API Integration:** Automatically fetch Molecular Weight (MW) and IUPAC names for any chemical compound using its common or scientific name.
* **🧪 Molar Solution Calculator:** Calculate required masses for target molarities, fully adjusting for chemical purity (`% w/w`) and hydrate water molecules ($H_2O$).
* **💧 Simple & Stock Dilution (C1V1 = C2V2):** Compute required stock and solvent volumes for accurate lab dilutions.
* **⚠️ Concentrated Acid/Base Engine:** Determine stock molarity from physical constants (density $d$, purity %, MW) and generate safety-compliant lab preparation protocols.
* **📋 Step-by-Step Lab Protocols:** Generates human-readable, actionable laboratory procedure guides for every calculation.

---
💻 Usage & Code Examples
1. Fetching Chemical Properties via PubChem API
Python
from chemst import PubChemService

# Retrieve compound info by name
compound = PubChemService.get_compound_by_name("Caffeine")

if compound:
    print(f"Name: {compound.name}")
    print(f"CID: {compound.cid}")
    print(f"IUPAC Name: {compound.iupac_name}")
    print(f"Molecular Weight: {compound.molecular_weight} g/mol")

2. Calculating Solid / Hydrated Molar SolutionsAdjusts automatically for hydrate water (e.g., CuSO₄ · 5H₂O) and chemical purity.$$\text{Effective MW} = \text{MW}_{\text{solute}} + (n \cdot \text{MW}_{\text{H}_2\text{O}})$$Pythonfrom chemst import SolutionCalculator

# Prepare 500 mL of 0.1 M Copper(II) sulfate pentahydrate (Purity 99%)
result = SolutionCalculator.calculate_molar_solution(
    compound_name="Copper sulfate",
    molecular_weight=159.60,
    target_molarity_M=0.1,
    target_volume_mL=500.0,
    purity_percent=99.0,
    hydration_water_moles=5
)

print(f"Required Mass: {result['required_mass_g']} g")
print(f"Effective MW: {result['effective_mw']} g/mol")
print("\n--- Lab Protocol ---")
print(result['recipe'])
3. Solution Dilution (M₁V₁ = M₂V₂)Pythonfrom chemst import SolutionCalculator

# Dilute 1.0 M stock solution to prepare 250 mL of 0.05 M solution
dilution = SolutionCalculator.calculate_dilution(
    stock_molarity_M=1.0,
    target_molarity_M=0.05,
    target_volume_mL=250.0
)

print(f"Stock Volume Needed: {dilution['stock_volume_mL']} mL")
print(f"Water Volume Needed: {dilution['water_volume_mL']} mL")
print("\n--- Procedure ---")
print(dilution['recipe'])
4. Concentrated Acid / Base PreparationCalculates stock molarity ($M_{\text{stock}}$) using liquid physical constants:$$M_{\text{stock}} = \frac{d \cdot \% \cdot 10}{\text{MW}}$$Pythonfrom chemst import SolutionCalculator

# Prepare 500 mL of 1.0 M HCl from concentrated stock (%37 HCl, d=1.19 g/mL, MW=36.46 g/mol)
acid_recipe = SolutionCalculator.calculate_liquid_acid_base(
    molecular_weight=36.46,
    density_g_ml=1.19,
    purity_percent=37.0,
    target_molarity_M=1.0,
    target_volume_mL=500.0
)

print(f"Stock Molarity: {acid_recipe['stock_molarity_M']} M")
print(f"Required Acid Volume: {acid_recipe['required_acid_vol_mL']} mL")
print("\n--- Safety Protocol & Steps ---")
print(acid_recipe['recipe'])

📜 License
Distributed under the MIT License. See LICENSE for more information.

👨‍💻 Author
Developed by Ertan Fatih Albayın

LinkedIn: Ertan Fatih Albayın

GitHub: @efatihalbayin

## 🚀 Installation

Install the stable release directly from PyPI via `pip`:

```bash
pip install chemst 
