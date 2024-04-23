#!/bin/bash

# Define the image and service names - monday
image_name="docker-asa-image"
service_name="docker-asa-deployment"

# Start Minikube
minikube start

# Set Docker environment
eval "$(minikube docker-env)"  # Ensure the correct environment

# Build the Docker image
docker build -t "$image_name" .  # Builds the image from the Dockerfile in the current directory

# Deploy using kubectl and a YAML configuration file
kubectl apply -f k8/deployment/deployment.yaml

# Expose the deployment with LoadBalancer on the specified port
kubectl expose deployment "$service_name" --name="$service_name" --type=LoadBalancer --target-port=80

# Check if the service exists and has endpoints
while true; do
  # Get the list of endpoints for the service
  endpoints=$(kubectl get endpoints "$service_name" -o=jsonpath='{.subsets[*].addresses[*].ip}')

  # If there are endpoints (i.e., not empty), the service is considered "on"
  if [[ -n "$endpoints" ]]; then
    echo "Service $service_name is active with endpoints: $endpoints."
    break
  else
    echo "Service $service_name is not active yet. Waiting..."
    sleep 5  # Adjust the sleep time as needed
  fi
done

# Get the service URL to access from the host machine
service_url=$(minikube service "$service_name" --url)

# Open the URL in the default browser
xdg-open "$service_url" &

