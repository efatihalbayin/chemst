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

## 🚀 Installation

Install the stable release directly from PyPI via `pip`:

```bash
pip install chemst 
