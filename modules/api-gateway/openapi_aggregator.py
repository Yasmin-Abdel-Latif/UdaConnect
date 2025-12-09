"""
OpenAPI Spec Aggregator

Fetches and aggregates OpenAPI/Swagger specifications from downstream services
and provides a combined view accessible from the API Gateway.
"""

import requests
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Downstream service configurations
DOWNSTREAM_SERVICES = {
    "persons": {
        "url": "http://persons:5000",
        "description": "Person management service"
    },
    "locations": {
        "url": "http://locations:5001",
        "description": "Location tracking service"
    },
    "connections": {
        "url": "http://connections:5003",
        "description": "Connection and proximity service"
    }
}

OPENAPI_VERSION = "3.0.0"
GATEWAY_HOST = "api-gateway:5002"
GATEWAY_DESCRIPTION = "UdaConnect API Gateway - Aggregated OpenAPI specification"


def fetch_service_spec(service_name: str, service_url: str, timeout: int = 5) -> Optional[Dict[str, Any]]:
    """
    Fetch the Swagger/OpenAPI spec from a downstream service.
    
    Args:
        service_name: Name of the service
        service_url: Base URL of the service
        timeout: Request timeout in seconds
        
    Returns:
        The OpenAPI spec dict, or None if fetch fails
    """
    try:
        spec_url = f"{service_url}/apispec_1.json"  # Flasgger default endpoint
        response = requests.get(spec_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.warning(f"Failed to fetch spec from {service_name} ({service_url}): {e}")
        return None


def extract_paths_from_spec(spec: Dict[str, Any], service_name: str) -> Dict[str, Any]:
    """
    Extract and transform paths from a service spec, prefixing with service name.
    
    Args:
        spec: The OpenAPI spec dictionary
        service_name: Name of the service (used for prefixing)
        
    Returns:
        Transformed paths dictionary
    """
    paths = spec.get("paths", {})
    transformed = {}
    
    for path, methods in paths.items():
        # Prefix path with service name for clarity
        prefixed_path = f"/{service_name}{path}" if not path.startswith(f"/{service_name}") else path
        transformed[prefixed_path] = methods
    
    return transformed


def extract_schemas_from_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract schema definitions from a service spec.
    
    Args:
        spec: The OpenAPI spec dictionary
        
    Returns:
        Schemas dictionary
    """
    if "definitions" in spec:
        return spec.get("definitions", {})
    elif "components" in spec and "schemas" in spec["components"]:
        return spec["components"]["schemas"]
    return {}


def build_aggregated_spec() -> Dict[str, Any]:
    """
    Build an aggregated OpenAPI specification from all downstream services.
    
    Returns:
        Combined OpenAPI specification
    """
    aggregated_spec = {
        "openapi": OPENAPI_VERSION,
        "info": {
            "title": "UdaConnect API Gateway",
            "description": GATEWAY_DESCRIPTION,
            "version": "1.0.0",
            "contact": {
                "name": "UdaConnect Team"
            }
        },
        "servers": [
            {
                "url": f"http://{GATEWAY_HOST}",
                "description": "API Gateway"
            }
        ],
        "paths": {},
        "components": {
            "schemas": {}
        }
    }
    
    # Fetch and aggregate specs from each service
    for service_name, service_config in DOWNSTREAM_SERVICES.items():
        logger.info(f"Fetching spec from {service_name}...")
        spec = fetch_service_spec(service_name, service_config["url"])
        
        if spec:
            # Extract and merge paths
            paths = extract_paths_from_spec(spec, service_name)
            aggregated_spec["paths"].update(paths)
            
            # Extract and merge schemas
            schemas = extract_schemas_from_spec(spec)
            aggregated_spec["components"]["schemas"].update(schemas)
            
            logger.info(f"Successfully aggregated spec from {service_name}")
        else:
            logger.warning(f"Could not aggregate spec from {service_name}")
    
    # Add gateway-level endpoints
    aggregated_spec["paths"].update({
        "/swagger-ui": {
            "get": {
                "summary": "Swagger UI",
                "description": "Interactive API documentation",
                "tags": ["gateway"],
                "responses": {
                    "200": {
                        "description": "Swagger UI HTML"
                    }
                }
            }
        },
        "/openapi.json": {
            "get": {
                "summary": "OpenAPI Specification",
                "description": "Complete aggregated OpenAPI specification",
                "tags": ["gateway"],
                "responses": {
                    "200": {
                        "description": "OpenAPI JSON specification",
                        "content": {
                            "application/json": {}
                        }
                    }
                }
            }
        }
    })
    
    return aggregated_spec


def get_aggregated_spec() -> Dict[str, Any]:
    """
    Get the cached or freshly built aggregated spec.
    
    Returns:
        Aggregated OpenAPI specification
    """
    return build_aggregated_spec()
