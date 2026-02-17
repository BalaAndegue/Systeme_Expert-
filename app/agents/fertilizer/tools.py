"""
Outils spécialisés pour l'agent de fertilisation.
Calculs NPK, diagnostic carences, recommandations engrais, planning d'application.
"""

from typing import Dict, Any, List
from app.services.llm_service import LLMService


# Base de données des besoins NPK par culture (kg/ha)
CROP_NPK_REQUIREMENTS = {
    "cacao": {
        "N": {"young": 50, "mature": 80, "old": 60},
        "P": {"young": 30, "mature": 40, "old": 35},
        "K": {"young": 80, "mature": 120, "old": 100},
        "cycle": "jeune(<5ans), mature(5-15ans), vieux(>15ans)",
        "organic_preference": "Haute - compost, fientes volailles"
    },
    "café": {
        "N": {"young": 60, "mature": 100, "old": 70},
        "P": {"young": 25, "mature": 35, "old": 30},
        "K": {"young": 90, "mature": 140, "old": 110},
        "cycle": "jeune(<3ans), mature(3-10ans), vieux(>10ans)",
        "organic_preference": "Haute - compost, marc café"
    },
    "maïs": {
        "N": {"pre_semis": 40, "montaison": 80, "floraison": 40},
        "P": {"pre_semis": 60, "montaison": 20, "floraison": 0},
        "K": {"pre_semis": 40, "montaison": 40, "floraison": 20},
        "cycle": "pré-semis, montaison(30j), floraison(60j)",
        "organic_preference": "Moyenne - fumier décomposé"
    },
    "manioc": {
        "N": {"plantation": 30, "croissance": 20},
        "P": {"plantation": 40, "croissance": 10},
        "K": {"plantation": 60, "croissance": 40},
        "cycle": "plantation, croissance(3mois)",
        "organic_preference": "Faible - tolère sols pauvres"
    },
    "arachide": {
        "N": {"semis": 15},  # Légumineuse - fixation N2
        "P": {"semis": 50},
        "K": {"semis": 60},
        "cycle": "semis uniquement",
        "organic_preference": "Moyenne - inoculum rhizobium"
    },
    "tomate": {
        "N": {"plantation": 60, "floraison": 80, "fructification": 40},
        "P": {"plantation": 70, "floraison": 30, "fructification": 20},
        "K": {"plantation": 80, "floraison": 100, "fructification": 60},
        "cycle": "plantation, floraison(40j), fructification(60j)",
        "organic_preference": "Haute - compost riche"
    },
}

# Symptômes de carences nutritionnelles
NUTRIENT_DEFICIENCY_SYMPTOMS = {
    "N": {
        "symptômes": ["Jaunissement généralisé feuilles âgées", "Croissance ralentie", "Petites feuilles"],
        "cultures_sensibles": ["maïs", "cacao", "légumes"],
        "correction": "Urée (46-0-0) ou sulfate ammonium (21-0-0)"
    },
    "P": {
        "symptômes": ["Coloration pourpre/violette feuilles", "Mauvais développement racines", "Retard croissance"],
        "cultures_sensibles": ["tomate", "arachide", "maïs"],
        "correction": "Superphosphate triple (0-46-0) ou DAP (18-46-0)"
    },
    "K": {
        "symptômes": ["Nécrose bordures feuilles âgées", "Fruits de faible qualité", "Sensibilité maladies"],
        "cultures_sensibles": ["cacao", "café", "tomate"],
        "correction": "Chlorure potassium (0-0-60) ou sulfate potassium (0-0-50)"
    },
    "Ca": {
        "symptômes": ["Nécrose apex feuilles jeunes", "Fruits difformes", "Pourriture apicale"],
        "cultures_sensibles": ["tomate", "piment"],
        "correction": "Chaux agricole ou nitrate calcium"
    },
    "Mg": {
        "symptômes": ["Chlorose interveinaire feuilles âgées", "Rougissement feuilles"],
        "cultures_sensibles": ["cacao", "café"],
        "correction": "Dolomie (CaMg(CO3)2) ou sulfate magnésium"
    },
}

# Engrais organiques locaux
ORGANIC_FERTILIZERS_CAMEROON = {
    "compost_mature": {"N": 1.5, "P": 0.8, "K": 1.2, "disponibilité": "Très haute", "coût_fcfa_tonne": 15000},
    "fientes_volailles": {"N": 3.0, "P": 2.5, "K": 1.5, "disponibilité": "Haute", "coût_fcfa_tonne": 25000},
    "fumier_bovin": {"N": 0.6, "P": 0.3, "K": 0.5, "disponibilité": "Haute", "coût_fcfa_tonne": 10000},
    "tourteau_palmiste": {"N": 4.0, "P": 1.5, "K": 1.0, "disponibilité": "Moyenne", "coût_fcfa_tonne": 35000},
    "cendres_bois": {"N": 0, "P": 1.0, "K": 5.0, "disponibilité": "Haute", "coût_fcfa_tonne": 5000},
    "marc_café": {"N": 2.0, "P": 0.3, "K": 0.5, "disponibilité": "Moyenne (zones café)", "coût_fcfa_tonne": 8000},
}


async def calculate_npk_requirements(llm_service: LLMService, crop: str, area_ha: float = 1.0, growth_stage: str = "mature") -> Dict[str, Any]:
    """
    Calcule les besoins NPK pour une culture donnée.
    """
    crop_lower = crop.lower()
    
    if crop_lower not in CROP_NPK_REQUIREMENTS:
        # Utiliser LLM pour estimation
        prompt = f"""Estime besoins NPK (kg/ha) pour {crop} en général.
Format JSON: {{"N": X, "P": Y, "K": Z, "notes": "..."}}"""
        response = await llm_service.generate_response(prompt)
        return {"error": f"Culture {crop} non en base. Estimation générique requise.", "llm_estimate": response}
    
    crop_data = CROP_NPK_REQUIREMENTS[crop_lower]
    
    # Extraction besoins selon stade
    n_req = crop_data["N"].get(growth_stage, list(crop_data["N"].values())[0])
    p_req = crop_data["P"].get(growth_stage, list(crop_data["P"].values())[0])
    k_req = crop_data["K"].get(growth_stage, list(crop_data["K"].values())[0])
    
    total_n = n_req * area_ha
    total_p = p_req * area_ha
    total_k = k_req * area_ha
    
    return {
        "culture": crop,
        "superficie_ha": area_ha,
        "stade_croissance": growth_stage,
        "besoins_npk_kg_ha": {"N": n_req, "P": p_req, "K": k_req},
        "besoins_totaux_kg": {"N": total_n, "P": total_p, "K": total_k},
        "cycle_info": crop_data["cycle"],
        "préférence_organique": crop_data["organic_preference"]
    }


async def get_organic_fertilizers(llm_service: LLMService, npk_needs: Dict[str, float], region: str = "Cameroun") -> Dict[str, Any]:
    """
    Recommande engrais organiques pour atteindre besoins NPK.
    """
    n_target = npk_needs.get("N", 0)
    p_target = npk_needs.get("P", 0)
    k_target = npk_needs.get("K", 0)
    
    recommendations = []
    
    for fert_name, fert_data in ORGANIC_FERTILIZERS_CAMEROON.items():
        # Calcul quantité pour N
        qty_for_n = (n_target / fert_data["N"]) * 1000 if fert_data["N"] > 0 else 0
        
        n_supplied = (qty_for_n / 1000) * fert_data["N"]
        p_supplied = (qty_for_n / 1000) * fert_data["P"]
        k_supplied = (qty_for_n / 1000) * fert_data["K"]
        
        cost = (qty_for_n / 1000) * fert_data["coût_fcfa_tonne"]
        
        recommendations.append({
            "engrais": fert_name,
            "quantité_kg": round(qty_for_n, 1),
            "apport_npk": {"N": round(n_supplied, 1), "P": round(p_supplied, 1), "K": round(k_supplied, 1)},
            "disponibilité": fert_data["disponibilité"],
            "coût_fcfa": round(cost, 0)
        })
    
    # Trier par disponibilité et coût
    recommendations.sort(key=lambda x: (x["disponibilité"] != "Très haute", x["coût_fcfa"]))
    
    return {
        "besoins_cibles_kg_ha": {"N": n_target, "P": p_target, "K": k_target},
        "recommandations_organiques": recommendations[:3],  # Top 3
        "conseil": "Combiner plusieurs sources pour équilibre NPK optimal"
    }


async def diagnose_nutrient_deficiency(llm_service: LLMService, symptoms: str, crop: str) -> Dict[str, Any]:
    """
    Diagnostique carence nutritionnelle depuis symptômes.
    """
    probable_deficiencies = []
    
    symptoms_lower = symptoms.lower()
    
    for nutrient, data in NUTRIENT_DEFICIENCY_SYMPTOMS.items():
        match_score = 0
        for symptom in data["symptômes"]:
            if any(word in symptoms_lower for word in symptom.lower().split()):
                match_score += 1
        
        if match_score > 0:
            probable_deficiencies.append({
                "nutriment": nutrient,
                "score_match": match_score,
                "symptômes_attendus": data["symptômes"],
                "correction": data["correction"]
            })
    
    # Trier par score
    probable_deficiencies.sort(key=lambda x: x["score_match"], reverse=True)
    
    if not probable_deficiencies:
        # Utiliser LLM
        prompt = f"""Diagnostic carence nutritionnelle:
Culture: {crop}
Symptômes: {symptoms}

Identifie carence probable (N, P, K, Ca, Mg, Fe, etc.) et traitement. Format concis."""
        llm_diagnosis = await llm_service.generate_response(prompt)
        return {"diagnostic": "Non concluant (base données)", "analyse_llm": llm_diagnosis}
    
    return {
        "culture": crop,
        "symptômes_décrits": symptoms,
        "carences_probables": probable_deficiencies[:2],  # Top 2
        "action_immédiate": probable_deficiencies[0]["correction"] if probable_deficiencies else "Analyse sol recommandée"
    }


async def get_application_schedule(llm_service: LLMService, crop: str, total_npk_kg: Dict[str, float]) -> Dict[str, Any]:
    """
    Génère calendrier d'application fractionné des engrais.
    """
    crop_lower = crop.lower()
    
    if crop_lower not in CROP_NPK_REQUIREMENTS:
        return {"error": f"Pas de calendrier pour {crop}"}
    
    crop_data = CROP_NPK_REQUIREMENTS[crop_lower]
    stages = list(crop_data["N"].keys())
    
    schedule = []
    
    for i, stage in enumerate(stages):
        n_portion = crop_data["N"][stage]
        p_portion = crop_data["P"][stage]
        k_portion = crop_data["K"][stage]
        
        if crop_lower == "maïs":
            timing = ["Pré-semis (1 semaine avant)", "Montaison (30 jours)", "Floraison (60 jours)"][i]
        elif crop_lower in ["cacao", "café"]:
            timing = ["Début saison pluies", "Mi-saison pluies", "Fin saison pluies"][min(i, 2)]
        else:
            timing = f"Stade {i+1}: {stage}"
        
        schedule.append({
            "étape": i + 1,
            "stade": stage,
            "timing": timing,
            "doses_kg_ha": {"N": n_portion, "P": p_portion, "K": k_portion},
            "méthode": "Épandage en couronne (25cm du tronc)" if crop_lower in ["cacao", "café"] else "Épandage uniforme + incorporation"
        })
    
    return {
        "culture": crop,
        "fractionnement": len(schedule),
        "calendrier_application": schedule,
        "conseil_général": "Appliquer après légère pluie ou irriguer après. Éviter contact direct avec tige."
    }


async def get_soil_amendment_advice(llm_service: LLMService, soil_type: str, target_crop: str) -> Dict[str, Any]:
    """
    Conseils amendements selon type de sol.
    """
    soil_amendments = {
        "acide": {
            "problème": "pH < 5.5, toxicité Al, carence P/Ca/Mg",
            "amendement": "Chaux agricole (CaCO3)",
            "dose_kg_ha": "2000-4000",
            "timing": "3 mois avant plantation",
            "cultures_sensibles": ["tomate", "haricot", "arachide"]
        },
        "sableux": {
            "problème": "Faible rétention eau/nutriments, lessivage",
            "amendement": "Compost + argile bentonite",
            "dose_kg_ha": "10000-20000",
            "timing": "Épandage annuel",
            "cultures_sensibles": ["maraîchères", "riz"]
        },
        "argileux": {
            "problème": "Compaction, mauvais drainage, travail difficile",
            "amendement": "Sable grossier + matière organique",
            "dose_kg_ha": "Sable: 5000, MO: 10000",
            "timing": "Avant labour",
            "cultures_sensibles": ["arachide", "manioc"]
        },
        "ferralitique": {
            "problème": "Pauvre en P, acidité élevée",
            "amendement": "Phosphate naturel + chaux + compost",
            "dose_kg_ha": "Phosphate: 500, Chaux: 2000",
            "timing": "Début cycle cultural",
            "cultures_sensibles": ["cacao", "palmier"]
        }
    }
    
    soil_lower = soil_type.lower()
    amendment_data = None
    
    for soil_key, data in soil_amendments.items():
        if soil_key in soil_lower:
            amendment_data = data
            break
    
    if not amendment_data:
        prompt = f"""Conseils amendement pour sol: {soil_type}, culture: {target_crop}.
Format: problème, amendement recommandé, dose, timing."""
        llm_advice = await llm_service.generate_response(prompt)
        return {"type_sol": soil_type, "conseil_llm": llm_advice}
    
    return {
        "type_sol": soil_type,
        "culture_cible": target_crop,
        "problématique": amendment_data["problème"],
        "amendement_recommandé": amendment_data["amendement"],
        "dose_recommandée_kg_ha": amendment_data["dose_kg_ha"],
        "timing_application": amendment_data["timing"],
        "note": f"Critique pour: {', '.join(amendment_data['cultures_sensibles'])}"
    }


async def calculate_compost_recipe(llm_service: LLMService, target_volume_m3: float = 1.0) -> Dict[str, Any]:
    """
    Génère recette compost équilibré pour Cameroun.
    """
    # Recette standard compost Cameroun (ratios volumétriques)
    base_recipe = {
        "matières_vertes": {
            "items": ["Herbes fraîches", "Feuilles légumineuses", "Épluchures"],
            "volume_pct": 40,
            "ratio_C_N": "15:1"
        },
        "matières_brunes": {
            "items": ["Paille sèche", "Feuilles mortes", "Sciure bois"],
            "volume_pct": 40,
            "ratio_C_N": "60:1"
        },
        "activateurs": {
            "items": ["Fientes volailles", "Fumier bovin", "Cendres (1%)"],
            "volume_pct": 15,
            "ratio_C_N": "10:1"
        },
        "terre_locale": {
            "items": ["Terre de surface"],
            "volume_pct": 5,
            "ratio_C_N": "N/A"
        }
    }
    
    recipe_volumes = {}
    for category, data in base_recipe.items():
        volume = target_volume_m3 * (data["volume_pct"] / 100)
        recipe_volumes[category] = {
            "volume_m3": round(volume, 2),
            "ingrédients": data["items"],
            "proportion_pct": data["volume_pct"]
        }
    
    return {
        "volume_cible_m3": target_volume_m3,
        "recette_équilibrée": recipe_volumes,
        "instructions": [
            "1. Alterner couches vertes (10cm) et brunes (10cm)",
            "2. Saupoudrer activateurs entre couches",
            "3. Humidifier (60-70% humidité)",
            "4. Retourner tous les 7 jours",
            "5. Maturité en 6-8 semaines (texture terreuse, odeur forêt)"
        ],
        "température_optimale": "55-65°C (phase active)",
        "rendement_final": f"{target_volume_m3 * 0.6:.1f}m³ compost mature (perte 40%)"
    }
