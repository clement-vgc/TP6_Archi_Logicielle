# TP6_Archi_Logicielle

Application de gestion de quiz avec:
- une API backend en Flask (dossier api)
- un client frontend en Vue + Vite (dossier frontend)

## Rôle de chaque composant frontend

- EditerQuiz.vue: écran principal d'administration. Il affiche la liste des quiz, permet de consulter/modifier/supprimer un quiz et d'ajouter des questions au quiz sélectionné.
- CreerQuiz.vue: écran de création d'un nouveau quiz. Il envoie le nom du quiz à l'API puis redirige vers l'écran de modification.
- ModifierQuiz.vue: édition complète d'un quiz précis (nom du quiz, ajout de questions, modification/suppression des questions existantes).
- ConsulterQuiz.vue: affichage d'un quiz en lecture (nom, id, questions).
- QuestionAdminItem.vue: composant réutilisable pour afficher et éditer une question côté administration.
- JouerQuiz.vue: mode joueur. Il permet de choisir un quiz, répondre aux questions, valider les réponses et calculer le score.
- RepondreQuizItem.vue: composant d'affichage d'une question côté joueur.
  
## 1) Prerequis

- Linux, macOS ou Windows
- Python 3.10+ (ou version proche)
- Node.js 18+ et npm

## 2) Installation

Depuis la racine du projet:

```bash
cd TP6_Archi_Logicielle
```

### 2.1 Installation backend

Linux/macOS :

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd ..
```

Windows :

```powershell
cd api
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
cd ..
```

### 2.2 Installation frontend

```bash
cd frontend
npm install
cd ..
```

## 3) Lancer l'application

Ouvrir 2 terminaux: un pour le serveur API, un pour le client web.

### Terminal 1 - lancer le serveur backend

Linux/macOS:

```bash
cd api
source .venv/bin/activate
cd todo
flask run
```

Windows:

```powershell
cd api
.\.venv\Scripts\Activate.ps1
cd todo
flask run
```
Ensuite il suffit de cliquer sur le lien :
- http://127.0.0.1:5000

### Terminal 2 - lancer le client frontend

```bash
cd frontend
npm run dev
```
Cliquer sur le lien :
- http://localhost:5173
