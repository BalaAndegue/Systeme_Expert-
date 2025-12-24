from app.models.region import Region

# Données statiques des 10 régions du Cameroun
CAMEROON_REGIONS = [
    Region(
        name="Centre",
        capital="Yaoundé",
        climate_description="Climat équatorial de type guinéen, 4 saisons.",
        soil_types=["Ferralitiques", "Argileux"],
        major_crops=["Cacao", "Café", "Manioc", "Maïs", "Arachide", "Plantain"],
        description="Zone de forêt dense et de savane périforestière. C'est le bassin agricole principal pour le cacao."
    ),
    Region(
        name="Littoral",
        capital="Douala",
        climate_description="Climat équatorial de type camerounien, très humide.",
        soil_types=["Sableux", "Volcaniques (fertile)"],
        major_crops=["Banane", "Palmier à huile", "Hévéa", "Poivre", "Cacao"],
        description="Zone côtière fertile, propice aux grandes plantations agro-industrielles."
    ),
    Region(
        name="Ouest",
        capital="Bafoussam",
        climate_description="Climat tempéré d'altitude, frais et pluvieux.",
        soil_types=["Volcaniques noirs (très fertiles)"],
        major_crops=["Café Arabica", "Thé", "Maïs", "Haricot", "Pomme de terre", "Tomate"],
        description="Le grenier du Cameroun grâce à ses sols volcaniques et son climat favorable."
    ),
    Region(
        name="Nord-Ouest",
        capital="Bamenda",
        climate_description="Climat de montagne, frais.",
        soil_types=["Volcaniques"],
        major_crops=["Café Arabica", "Thé", "Pomme de terre", "Riz", "Maïs"],
        description="Région montagneuse avec une forte activité agricole et pastorale."
    ),
    Region(
        name="Sud-Ouest",
        capital="Buea",
        climate_description="Climat équatorial humide de mousson (proche Mont Cameroun).",
        soil_types=["Volcaniques"],
        major_crops=["Cacao", "Café", "Palmier à huile", "Banane", "Thé"],
        description="Zone très fertile située au pied du Mont Cameroun."
    ),
    Region(
        name="Sud",
        capital="Ebolowa",
        climate_description="Climat équatorial pur.",
        soil_types=["Ferralitiques"],
        major_crops=["Cacao", "Manioc", "Plantain", "Palmier à huile"],
        description="Zone de forêt dense, agriculture vivrière et de rente (cacao)."
    ),
    Region(
        name="Est",
        capital="Bertoua",
        climate_description="Climat équatorial.",
        soil_types=["Ferralitiques"],
        major_crops=["Cacao", "Café", "Manioc", "Plantain", "Maïs"],
        description="Vaste zone forestière, potentiel agricole immense mais enclavé."
    ),
    Region(
        name="Adamaoua",
        capital="Ngaoundéré",
        climate_description="Climat tropical de savane d'altitude.",
        soil_types=["Ferralitiques rouges"],
        major_crops=["Maïs", "Igname", "Manioc", "Sorgho", "Millet"],
        description="Le 'château d'eau' du Cameroun, zone de transition forêt-savane, grande zone d'élevage."
    ),
    Region(
        name="Nord",
        capital="Garoua",
        climate_description="Climat tropical sec (Soudanien).",
        soil_types=["Ferrugineux"],
        major_crops=["Coton", "Arachide", "Sorgho", "Maïs", "Oignon"],
        description="Zone de savane, culture principale du coton et des céréales sèches."
    ),
    Region(
        name="Extrême-Nord",
        capital="Maroua",
        climate_description="Climat sahélien, chaud et sec.",
        soil_types=["Sableux", "Argileux (Vertisols)"],
        major_crops=["Coton", "Sorgho", "Millet", "Oignon", "Riz"],
        description="Zone la plus septentrionale, agriculture adaptée à la sécheresse (mil, sorgho)."
    )
]

def get_all_regions():
    return CAMEROON_REGIONS

def get_region_by_name(name: str):
    for region in CAMEROON_REGIONS:
        if region.name.lower() == name.lower():
            return region
    return None
