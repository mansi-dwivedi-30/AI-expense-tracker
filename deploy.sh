#!/bin/bash
rm -rf migrations

# 2. Initialize migrations again
flask db init

# 3. Create fresh migration (auto-detect models)
flask db migrate -m "initial"

# 4. Apply to DB
flask db upgrade

echo "Starting Flask server..."
flask run --host=0.0.0.0 --port=5000
