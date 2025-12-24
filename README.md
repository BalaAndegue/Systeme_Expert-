# Système Multi-Agents Agriculture Cameroun 🇨🇲

Une plateforme intelligente basée sur des agents autonomes pour assister les agriculteurs camerounais. Le système utilise l'IA Gemini pour fournir des conseils personnalisés sur la météo, les cultures, la santé des plantes et l'économie agricole, adaptés aux spécificités des 10 régions du Cameroun.

## 🚀 Fonctionnalités

- **Orchestration Intelligente** : Analyse sémantique des questions pour activer uniquement les agents pertinents.
- **Agents Spécialisés** :
  - 🌦️ **Météo** : Climatologie locale et conseils saisonniers.
  - 🌱 **Cultures** : Itinéraires techniques (Cacao, Café, Maïs, etc.).
  - 🩺 **Santé** : Diagnostic maladies et traitements biologiques.
  - 💰 **Économie** : Prix du marché en FCFA et tendances.
- **Données Locales** : Intègre les calendriers culturaux et spécificités de chaque région du Cameroun.
- **Double Interface** : CLI (Ligne de commande) et API/Web.

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone <votre-repo>
   cd agriculture-cameroun-simple
   ```

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**
   - Copiez `.env.example` vers `.env`
   - Ajoutez votre clé API Google Gemini
   ```bash
   cp .env.example .env
   # Editez .env avec votre éditeur préféré
   ```

## 📖 Utilisation

### Mode Ligne de Commande (CLI)

Posez une question directement depuis le terminal :

```bash
python main.py cli --query "Comment lutter contre la pourriture brune du cacao ?" --region "Centre"
```

Ou plus simplement :
```bash
python main.py cli -q "Quel est le prix actuel du maïs ?" -r "Ouest"
```

### Mode Serveur Web / API

Lancez le serveur API :

```bash
python main.py web
```
Le serveur démarrera sur `http://localhost:5000`.

**Exemple d'appel API :**

```bash
curl -X POST http://localhost:5000/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Quand planter le maïs ?", "region": "Nord"}'
```

## 🏗️ Architecture

```
agriculture-cameroun-simple/
├── app/
│   ├── agents/       # Agents spécialisés (Weather, Crop, etc.)
│   ├── core/         # Orchestrateur et Bus de messages
│   ├── data/         # Données statiques (Régions, Prix, Calendriers)
│   ├── services/     # Services externes (Gemini)
│   └── api/          # Routes API Flask
├── main.py           # Point d'entrée unifié
└── config.py         # Configuration
```

## 🧪 Tests

Pour lancer les tests unitaires :

```bash
pytest tests/
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Merci d'ouvrir une issue pour discuter des changements majeurs.

## 📄 Licence

MIT
