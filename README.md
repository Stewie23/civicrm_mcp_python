# CiviCRM MCP Server (Python)

Ein minimal lauffähiger **Model Context Protocol (MCP)** Server für **CiviCRM APIv4** in Python.
Er stellt generische CRUD- und Query-Tools bereit und kann per **stdio** gestartet werden.

## Features
- Tools: `civicrm.create`, `civicrm.get`, `civicrm.update`, `civicrm.delete`, `civicrm.search`  
- Extras: `civicrm.batch`, `civicrm.schema.entities`, `civicrm.schema.fields`
- Async mit `httpx` und `mcp` (FastMCP)
- Konfig via `.env` (URL, Token, Auth-Schema etc.)
- Einfacher Schema-Cache (in-memory)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# Passe CIVI_URL / CIVI_TOKEN / AUTH_SCHEME an
# Beispiel: CIVI_URL=https://example.org/civicrm/api4
#           AUTH_SCHEME=bearer (oder x-civi-auth)
#           CIVI_TOKEN=DEIN_TOKEN

python app.py
```

Der Server spricht MCP über **stdio**. Binde ihn in deinen Client/LLM ein als MCP-Server-Prozess mit stdio-Transport.

## Tools & Payloads

### civicrm.create
```json
{
  "entity": "Contact",
  "record": { "contact_type": "Individual", "first_name": "Alice" }
}
```

### civicrm.get
```json
{ "entity": "Contact", "id": 123, "select": ["id","display_name"], "include": ["email"] }
```

### civicrm.update
```json
{ "entity": "Contact", "id": 123, "record": { "first_name": "Alicia" } }
```

### civicrm.delete
```json
{ "entity": "Contact", "id": 123 }
```

### civicrm.search
```json
{
  "entity": "Contact",
  "where": [{"field":"contact_type","op":"=","value":"Individual"}],
  "select": ["id","display_name"],
  "include": ["email"],
  "orderBy": {"id": "DESC"},
  "limit": 25,
  "offset": 0
}
```

### civicrm.batch
```json
{
  "operations": [
    {"entity":"Contact","action":"get","params":{"where":[{"field":"id","op":"=","value":1}]}},
    {"entity":"Contact","action":"create","params":{"first_name":"Bob","contact_type":"Individual"}}
  ]
}
```

### civicrm.schema.entities
```json
{}
```

### civicrm.schema.fields
```json
{ "entity": "Contact", "forceRefresh": false }
```

## Hinweise
- Auth-Header werden über `AUTH_SCHEME` gewählt: `bearer` → `Authorization: Bearer <TOKEN>`,  
  `x-civi-auth` → `X-Civi-Auth: <TOKEN>`.
- APIv4 erwartet POST JSON `{ entity, action, params }` auf `CIVI_URL` (z. B. `https://example.org/civicrm/api4`). 
- Rückgabestruktur wird unverändert zurückgegeben (inkl. `is_error`, `values` etc.).
- Fehler werden als MCP-Tool-Fehler mit Details geworfen.

## Lizenz
MIT
