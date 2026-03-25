# TP6_Archi_Logicielle

Application de gestion de quiz avec:
- une API backend en Flask (dossier api)
- un client frontend en Vue + Vite (dossier frontend)

## 1) Prerequis

- Linux, macOS ou Windows
- Python 3.10+ (ou version proche)
- Node.js 18+ et npm

Verifier les versions:

```bash
python3 --version
node --version
npm --version
```

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
pip install -r requirements.txt
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
flask --app todo run
```

Windows:

```powershell
cd api
.\.venv\Scripts\Activate.ps1
flask --app todo run
```

- http://127.0.0.1:5000/quiz/api/v1.0/questionnaires

### Terminal 2 - lancer le client frontend

```bash
cd frontend
npm run dev
```


- http://localhost:5173
