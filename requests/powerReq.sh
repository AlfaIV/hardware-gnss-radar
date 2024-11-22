curl -X POST "http://85.198.109.43:1000/hardware/power" \
-H "Content-Type: application/json" \
-d '{
    "token": "123",
    "description": {
        "startTime": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")'",
        "endTime": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")'",
        "group": "GPS",
        "target": "G12",
        "signal": "L1"
    },
    "data": {
        "power": [10,11],
        "startTime": "'$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")'",
        "timeStep": 1
    }
}'