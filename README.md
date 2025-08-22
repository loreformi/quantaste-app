# Quantaste - Smart Score Engine

Questo progetto è un'applicazione full-stack che calcola uno "Smart Score" per i titoli azionari, combinando analisi fondamentale e tecnica. Fornisce un backend FastAPI per l'elaborazione dei dati e un frontend Next.js per la visualizzazione.

## Struttura

- `/backend`: Applicazione Python FastAPI.
- `/frontend`: Applicazione web Next.js.

---

## Configurazione

Prima di avviare le applicazioni, è necessario configurare le variabili d'ambiente.

1.  **Crea i file `.env`**:
    Nella root di `/backend` e `/frontend`, crea un file `.env` copiando il rispettivo file `.env.example`.

2.  **Configura il Backend (`/backend/.env`)**:

    ```ini
    # URL del database. Per SQLite (default), il percorso è relativo alla directory /backend.
    # Per Postgres, usare un formato come: "postgresql://user:password@host:port/dbname"
    DATABASE_URL="sqlite:///./quantaste.db"

    # Lista di ticker da analizzare, separati da virgola.
    DEFAULT_TICKERS="AAPL,MSFT,GOOGL,AMZN,TSLA,NVDA"
    ```

3.  **Configura il Frontend (`/frontend/.env`)**:

    ```ini
    # URL del backend FastAPI a cui il frontend si connetterà.
    NEXT_PUBLIC_API_URL="http://127.0.0.1:8000"
    ```

---

## Avvio in modalità Sviluppo

Segui questi passaggi per avviare il backend e il frontend.

### 1. Backend

Assicurati di avere Python 3.8+ installato.

```bash
# 1. Vai nella directory del backend
cd backend

# 2. (Consigliato) Crea e attiva un ambiente virtuale
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
# source venv/bin/activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Avvia il server FastAPI
# Il server sarà in esecuzione su http://127.0.0.1:8000
# La prima volta che lo avvii, creerà il database SQLite e scaricherà i dati iniziali.
# Questo processo potrebbe richiedere qualche minuto.
uvicorn app.main:app --reload
```

### 2. Frontend

Assicurati di avere Node.js 18+ installato.

```bash
# 1. Apri un NUOVO terminale e vai nella directory del frontend
cd frontend

# 2. Installa le dipendenze
npm install

# 3. Avvia il server di sviluppo Next.js
# Il sito sarà accessibile su http://localhost:3000
npm run dev
```

Dopo aver completato questi passaggi, apri [http://localhost:3000](http://localhost:3000) nel tuo browser per vedere la dashboard.
