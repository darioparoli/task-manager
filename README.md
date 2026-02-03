# Task Manager 📋

Web application completa basata su Python (FastAPI) per la gestione di task. Include API REST, interfaccia web e configurazione Docker.

## Caratteristiche

- **API REST con FastAPI**: Endpoints per creare, leggere, aggiornare ed eliminare task
- **Interfaccia Web HTML/JS**: Interfaccia utente moderna e responsive
- **Test Automatizzati**: Unit test con pytest
- **Docker**: Dockerfile multi-stage e docker-compose per deployment rapido
- **In-Memory Storage**: Gestione task in memoria (adatto per demo e sviluppo)

## Struttura del Progetto

```
task-manager/
├── main.py                 # Applicazione FastAPI
├── requirements.txt        # Dipendenze Python
├── Dockerfile             # Dockerfile multi-stage
├── docker-compose.yml     # Configurazione Docker Compose
├── static/
│   ├── index.html        # Interfaccia web
│   ├── css/
│   │    └── style.css
│   └── js/
│        └── script.js   
├── tests/
│   ├── __init__.py
│   └── test_main.py      # Unit test
└── README.md
```

## API Endpoints

- `GET /` - Interfaccia web
- `GET /api/tasks` - Ottieni tutti i task
- `POST /api/tasks` - Crea un nuovo task
- `GET /api/tasks/{id}` - Ottieni un task specifico
- `PUT /api/tasks/{id}` - Aggiorna un task
- `DELETE /api/tasks/{id}` - Elimina un task
- `DELETE /api/tasks/completed` - Elimina i task completati

## Come Avviare l'Applicazione con Docker su Linux

### Prerequisiti

- Docker installato ([Guida installazione Docker](https://docs.docker.com/engine/install/))
- Docker Compose installato (solitamente incluso con Docker Desktop)

### Avvio con Docker Compose (Consigliato)

1. **Clona il repository** (se non già fatto):
   ```bash
   git clone https://github.com/darioparoli/task-manager.git
   cd task-manager
   ```

2. **Avvia l'applicazione**:
   ```bash
   docker-compose up -d
   ```

   Oppure per vedere i log in tempo reale:
   ```bash
   docker-compose up
   ```

3. **Accedi all'applicazione**:
   - Apri il browser e vai su: `http://localhost:8080`
   - API disponibile su: `http://localhost:8080/api/tasks`

4. **Verifica lo stato**:
   ```bash
   docker-compose ps
   ```

5. **Visualizza i log**:
   ```bash
   docker-compose logs -f
   ```

6. **Ferma l'applicazione**:
   ```bash
   docker-compose down
   ```

### Avvio con Docker (Senza Compose)

1. **Costruisci l'immagine Docker**:
   ```bash
   docker build -t task-manager:latest .
   ```

2. **Esegui il container**:
   ```bash
   docker run -d -p 8080:8080 --name task-manager-app task-manager:latest
   ```

3. **Verifica che il container sia in esecuzione**:
   ```bash
   docker ps
   ```

4. **Visualizza i log**:
   ```bash
   docker logs -f task-manager-app
   ```

5. **Ferma e rimuovi il container**:
   ```bash
   docker stop task-manager-app
   docker rm task-manager-app
   ```

## Sviluppo Locale (Senza Docker)

### Prerequisiti

- Python 3.11 o superiore
- pip

### Setup

1. **Crea un ambiente virtuale**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Linux/Mac
   # oppure
   venv\Scripts\activate     # Su Windows
   ```

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Avvia l'applicazione**:
   ```bash
   python main.py
   ```

4. **Accedi all'applicazione**:
   - Interfaccia web: `http://localhost:8080`
   - Documentazione API interattiva: `http://localhost:8080/docs`

## Esecuzione dei Test

### Con Docker

```bash
docker-compose run task-manager pytest tests/ -v
```

### Senza Docker

```bash
# Assicurati che l'ambiente virtuale sia attivo
pytest tests/ -v
```

## Utilizzo dell'API

### Esempi con curl

**Creare un task**:
```bash
curl -X POST http://localhost:8080/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Mio Task", "description": "Descrizione del task"}'
```

**Ottenere tutti i task**:
```bash
curl http://localhost:8080/api/tasks
```

**Ottenere un task specifico**:
```bash
curl http://localhost:8080/api/tasks/1
```

**Aggiornare un task**:
```bash
curl -X PUT http://localhost:8080/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "Task Aggiornato", "completed": true, "created_at": "2024-01-01T00:00:00"}'
```

**Eliminare un task**:
```bash
curl -X DELETE http://localhost:8080/api/tasks/1
```

## Tecnologie Utilizzate

- **FastAPI**: Framework web moderno e veloce per Python
- **Uvicorn**: Server ASGI per FastAPI
- **Pydantic**: Validazione dei dati
- **Pytest**: Framework di testing
- **Docker**: Containerizzazione
- **HTML/CSS/JavaScript**: Interfaccia web

## Note

- L'applicazione utilizza storage in memoria, quindi i dati vengono persi quando il container viene fermato
- Per un ambiente di produzione, considera l'utilizzo di un database persistente (PostgreSQL, MySQL, ecc.)
- La porta predefinita è 8080 ma può essere modificata nel file `docker-compose.yml`

## Licenza

Questo progetto è fornito come esempio per scopi educativi e di sperimentazione DevOps.
