#!/bin/bash
curl http://localhost:5000/api/content/generate -X POST -H 'Content-Type: application/json' -d '{"topic": "letter A", "age_group": "preschool"}'
