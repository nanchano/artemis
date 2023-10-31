run:
	uvicorn artemis.main:app --reload

ping:
	curl http://127.0.0.1:8000/ping

create-event:
	curl -X POST \
    -H "Content-Type: application/json" \
    -d '{"name": "Random Event", "description": "a random test event", "category": "random", "location": "Buenos Aires", "publisher": "Nico", "start_ts": "2023-01-01T18:00:00Z","end_ts": "2023-01-01T21:00:00Z"}' \
	http://127.0.0.1:8000/events/

get-event:
	curl http://127.0.0.1:8000/events/1

update-event:
	curl -X PUT \
    -H "Content-Type: application/json" \
    -d '{"description": "Changed Description"}' \
	http://127.0.0.1:8000/events/1

delete-event:
	curl -X DELETE http://127.0.0.1:8000/events/1

all-requests:
	make create-event && make get-event && make update-event && make delete-event

dependencies:
	poetry install --no-interaction --no-root

lint:
	flake8 . --count --select=E9,F63,F7,F82 --max-line-length=88 --max-complexity=18 --show-source --statistics

fmt:
	black --check .
	isort --profile black --diff .

test:
	coverage run -m pytest --ff
