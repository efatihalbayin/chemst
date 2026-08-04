import requests
from dataclasses import dataclass
from typing import Optional

@dataclass
class ChemicalCompound:
    name: str
    cid: int
    molecular_weight: float
    iupac_name: str
    density: Optional[float] = None

class PubChemService:
    """PubChem REST API üzerinden kimyasal veri çekme servisi."""
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    @classmethod
    def get_compound_by_name(cls, name: str) -> Optional[ChemicalCompound]:
        try:
            cid_url = f"{cls.BASE_URL}/compound/name/{requests.utils.quote(name)}/cids/JSON"
            response = requests.get(cid_url, timeout=5)
            if response.status_code != 200:
                return None
            
            data = response.json()
            if "IdentifierList" not in data or "CID" not in data["IdentifierList"]:
                return None
                
            cid = data["IdentifierList"]["CID"][0]

            prop_url = f"{cls.BASE_URL}/compound/cid/{cid}/property/MolecularWeight,IUPACName/JSON"
            prop_res = requests.get(prop_url, timeout=5)
            if prop_res.status_code != 200:
                return None

            properties = prop_res.json()["PropertyTable"]["Properties"][0]

            return ChemicalCompound(
                name=name,
                cid=cid,
                molecular_weight=float(properties.get("MolecularWeight", 0.0)),
                iupac_name=properties.get("IUPACName", name)
            )
        except Exception as e:
            print(f"PubChem Fetch Error: {e}")
            return None

class SolutionCalculator:
    """Laboratuvar Molarite, Seyreltme ve Derşik Asit/Baz Hesaplama Motoru."""

    @staticmethod
    def calculate_molar_solution(compound_name: str, molecular_weight: float, target_molarity_M: float, 
                                 target_volume_mL: float, purity_percent: float = 100.0, 
                                 hydration_water_moles: int = 0) -> dict:
        effective_mw = molecular_weight + (hydration_water_moles * 18.015)
        target_volume_L = target_volume_mL / 1000.0
        moles_needed = target_molarity_M * target_volume_L
        pure_mass_g = moles_needed * effective_mw
        actual_mass_g = pure_mass_g / (purity_percent / 100.0)

        return {
            "compound_name": compound_name,
            "effective_mw": round(effective_mw, 3),
            "required_mass_g": round(actual_mass_g, 4),
            "target_molarity_M": target_molarity_M,
            "target_volume_mL": target_volume_mL,
            "recipe": (
                f"1. Hassas terazide tam {round(actual_mass_g, 4)} g {compound_name} tartın.\n"
                f"2. Çözeltiyi hazırlayacağınız kaba alıp yaklaşık {round(target_volume_mL * 0.7, 1)} mL saf suda tamamen çözün.\n"
                f"3. Balon jojeye aktarıp hacmi saf su ile tam {target_volume_mL} mL çizgisine tamamlayın ve çalkalayın."
            )
        }

    @staticmethod
    def calculate_dilution(stock_molarity_M: float, target_molarity_M: float, target_volume_mL: float) -> dict:
        if target_molarity_M >= stock_molarity_M:
            raise ValueError("Hedef molarite, stok molariteden büyük veya eşit olamaz!")

        stock_volume_needed_mL = (target_molarity_M * target_volume_mL) / stock_molarity_M
        water_volume_needed_mL = target_volume_mL - stock_volume_needed_mL

        return {
            "stock_volume_mL": round(stock_volume_needed_mL, 2),
            "water_volume_mL": round(water_volume_needed_mL, 2),
            "recipe": (
                f"1. Stok çözeltiden hassas dereceli pipetle {round(stock_volume_needed_mL, 2)} mL çekin.\n"
                f"2. Üzerine {round(water_volume_needed_mL, 2)} mL saf su ekleyerek toplam hacmi tam {target_volume_mL} mL'ye tamamlayın."
            )
        }

    @staticmethod
    def calculate_liquid_acid_base(molecular_weight: float, density_g_ml: float, purity_percent: float,
                                   target_molarity_M: float, target_volume_mL: float) -> dict:
        if density_g_ml <= 0 or purity_percent <= 0:
            raise ValueError("Yoğunluk ve saflık katsayısı 0'dan büyük olmalıdır.")

        stock_molarity_M = (density_g_ml * purity_percent * 10.0) / molecular_weight

        if target_molarity_M >= stock_molarity_M:
            raise ValueError("Hedef molarite stok çözelti molaritesinden büyük veya eşit olamaz!")

        required_acid_volume_mL = (target_molarity_M * target_volume_mL) / stock_molarity_M
        water_volume_mL = target_volume_mL - required_acid_volume_mL

        return {
            "stock_molarity_M": round(stock_molarity_M, 3),
            "required_acid_vol_mL": round(required_acid_volume_mL, 2),
            "water_vol_mL": round(water_volume_mL, 2),
            "recipe": (
                f"⚠️ EMNİYET UYARISI: Asit üzerine su dökülmez! Daima su üzerine yavaşça asit ekleyin!\n\n"
                f"1. Balon jojeye önce yaklaşık {round(water_volume_mL * 0.7, 1)} mL saf su koyun.\n"
                f"2. Çeker ocak altında, hassas pipetle tam {round(required_acid_volume_mL, 2)} mL derşik çözeltiden çekip suya ekleyin.\n"
                f"3. Çözelti oda sıcaklığına geldikten sonra saf su ile hacmi tam {target_volume_mL} mL çizgisine tamamlayın."
            )
        }