# Task API

A small CRUD API for managing a to-do list. In-memory storage only — no database, data resets on restart (that's intentional, not a bug).

Built for FlyRank AI Internship — Week 2, Assignment BE-01.

## Run it

Requires Python 3.10+.

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then open http://localhost:8000/docs for interactive Swagger UI, or hit the API directly at http://localhost:8000.

## Endpoints

| Method | Path          | Description               | Success | Errors                  |
|--------|---------------|----------------------------|---------|--------------------------|
| GET    | `/`           | API info                   | 200     | —                        |
| GET    | `/health`     | Health check                | 200     | —                        |
| GET    | `/tasks`      | List all tasks              | 200     | —                        |
| GET    | `/tasks/{id}` | Get a single task           | 200     | 404 if not found         |
| POST   | `/tasks`      | Create a task                | 201     | 400 if `title` missing/empty |
| PUT    | `/tasks/{id}` | Update a task (title/done)  | 200     | 400 invalid body, 404 not found |
| DELETE | `/tasks/{id}` | Delete a task                | 204     | 404 if not found         |
| GET    | `/stats`      | Task counts (bonus)          | 200     | —                        |
| POST   | `/reset`      | Reset to example tasks (bonus) | 200  | —                        |

## Example request

```bash
curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

```
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Full checkpoint run (all passing)

```
GET  /                 -> 200  {"name":"Task API","version":"1.0","endpoints":["/tasks"]}
GET  /health            -> 200  {"status":"ok"}
GET  /tasks              -> 200  [3 example tasks]
GET  /tasks/1             -> 200  {"id":1,"title":"Buy milk","done":false}
GET  /tasks/99             -> 404  {"detail":"Task 99 not found"}
POST /tasks {"title":"Buy milk"}     -> 201  {"id":4,"title":"Buy milk","done":false}
POST /tasks {"title":""}              -> 400  {"detail":"title is required and cannot be empty"}
PUT  /tasks/1 {"done":true}            -> 200  {"id":1,"title":"Buy milk","done":true}
DELETE /tasks/2                         -> 204  (no body)
DELETE /tasks/99                         -> 404  {"detail":"Task 99 not found"}
```

## Swagger UI

Screenshot: `[insert your own screenshot here — /docs, with the full CRUD cycle exercised via "Try it out"]`

## The mortality experiment

Restarting the server resets `tasks` back to the 3 seed tasks — anything created, updated, or deleted during a session is gone. That's because the "database" is just a Python list living in the process's memory: when the process ends, the memory is freed. This is exactly why real APIs use a persistent database instead of an in-memory list — Week 3.

## AI vs me

`[if you complete Stage 7, add your own prompt, the AI-generated version in ai-version/, and your differences here]`
