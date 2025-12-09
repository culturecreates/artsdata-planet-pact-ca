#!/bin/bash

# Fetch data using Python script
echo "Fetching data from PACT API..."
python3 data_fetcher.py

# Check if Python script executed successfully
if [ $? -ne 0 ]; then
  echo "Error: Failed to fetch data from API"
  exit 1
fi

# Check if output file was created
if [ ! -f "output.json" ]; then
  echo "Error: output.json not found in outputs directory"
  exit 1
fi

echo "Data fetched successfully!"

# Update the Config file
config_file="ontorefine-config.json"

# Start the services in the background
sudo docker compose up -d

# Wait for the server to start
echo "Waiting for server to start..."
while ! curl --output /dev/null --silent --head --fail http://localhost:7333; do
  sleep 5
done
echo "Server started!"

# Send a command to the running container
echo "Running OntoRefine CLI using config.json..."
sudo docker exec onto_refine /opt/ontorefine/dist/bin/ontorefine-cli transform ../data/output.json \
  -u http://localhost:7333  \
  --no-clean \
  --configurations ../data/ontorefine-config.json  \
  -f json >> entities.ttl

# Open the default browser
open http://localhost:7333

echo "Open Project to edit the RDF Mapping."