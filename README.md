<p align="center">
  <img src="logo.png" alt="ChemST Logo" width="180">
</p>

<h1 align="center">ChemST 🧪</h1>

<p align="center">
  <b>Smart Chemical Solution & Stoichiometry Engine for Python</b>
</p>

<p align="center">
  <a href="https://efatihalbayin.github.io/chemst-web/">🌐 <b>Live Web Application</b></a> •
  <a href="https://pypi.org/project/chemst/">📦 <b>PyPI Package</b></a>
</p>

<p align="center">
  <a href="https://pypi.org/project/chemst/"><img src="https://img.shields.io/pypi/v/chemst.svg" alt="PyPI version"></a>
  <a href="https://pypi.org/project/chemst/"><img src="https://img.shields.io/pypi/pyversions/chemst.svg" alt="Python Versions"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

---

**ChemST** is a lightweight, high-precision Python library designed for computational chemists, laboratory researchers, and students. It automates complex stoichiometry calculations, hydration adjustments, dilution protocols, and concentrated acid/base preparations while seamlessly integrating with the **PubChem REST API** to retrieve live molecular properties.

---

## 🌟 Key Features

- **⚡ Live PubChem REST API Integration:** Automatically fetch Molecular Weight (MW) and IUPAC names for any chemical compound using its common or scientific name.
- **🧪 Molar Solution Calculator:** Calculate required masses for target molarities, fully adjusting for chemical purity (`% w/w`) and hydrate water molecules ($H_2O$).
- **💧 Simple & Stock Dilution ($C_1V_1 = C_2V_2$):** Compute required stock and solvent volumes for accurate lab dilutions.
- **⚠️ Concentrated Acid/Base Engine:** Determine stock molarity from physical constants (density $d$, purity %, MW) and generate safety-compliant lab preparation protocols.
- **📋 Step-by-Step Lab Protocols:** Generates human-readable, actionable laboratory procedure guides for every calculation.

---

## 🚀 Installation

Install the stable release directly from PyPI via `pip`:

```bash
pip install chemst

---

## 📖 System Architecture

ChemST is divided into two core modules:

1. `PubChemService`: Interfaces dynamically with external NCBI databases.
2. `SolutionCalculator`: Executes high-precision stoichiometry algorithms and safety checks.

```text
        +--------------------+
        |    User Request    |
        +---------+----------+
                  |
         +--------+--------+
         |                 |
         v                 v
+---------------+   +--------------------+
| PubChemService|   | SolutionCalculator |
+-------+-------+   +---------+----------+
        |                     |
        v                     v
 [NCBI REST API]    [Stoichiometric Core]
        |                     |
        +--------+------------+
                 |
                 v
    [Result Dictionary & Recipe]

```

---

## 💻 Usage & Code Examples

### 1. Fetching Chemical Properties via PubChem API

```python
from chemst import PubChemService

# Retrieve compound info by name
compound = PubChemService.get_compound_by_name("Caffeine")

if compound:
    print(f"Name: {compound.name}")
    print(f"CID: {compound.cid}")
    print(f"IUPAC Name: {compound.iupac_name}")
    print(f"Molecular Weight: {compound.molecular_weight} g/mol")

```

---

### 2. Calculating Solid / Hydrated Molar Solutions

Adjusts automatically for hydrate water (e.g., $CuSO_4 \cdot 5H_2O$) and chemical purity.

$$\text{Effective MW} = \text{MW}_{\text{solute}} + (n \cdot \text{MW}_{\text{H}_2\text{O}})$$

```python
from chemst import SolutionCalculator

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

```

---

### 3. Solution Dilution ($M_1V_1 = M_2V_2$)

```python
from chemst import SolutionCalculator

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

```

---

### 4. Concentrated Acid / Base Preparation

Calculates stock molarity ($M_{\text{stock}}$) using liquid physical constants:

$$M_{\text{stock}} = \frac{d \cdot\%\cdot10}{\text{MW}}$$

```python
from chemst import SolutionCalculator

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

```

---

## 🛠️ API Reference

| Class | Method | Description |
| --- | --- | --- |
| `PubChemService` | `get_compound_by_name(name)` | Fetches compound metadata & MW from NCBI PubChem. |
| `SolutionCalculator` | `calculate_molar_solution(...)` | Mass calculation adjusted for hydrate water & purity. |
| `SolutionCalculator` | `calculate_dilution(...)` | Standard volumetric dilution protocol. |
| `SolutionCalculator` | `calculate_liquid_acid_base(...)` | High-density concentrated reagent calculation with safety notes. |

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👨‍💻 Author

Developed by **Ertan Fatih Albayın**

* **LinkedIn:** [Ertan Fatih Albayın](https://www.linkedin.com/in/ertan-fatih-albay%C4%B1n-90a606279/)
* **GitHub:** [@efatihalbayin](https://github.com/efatihalbayin)

```

```