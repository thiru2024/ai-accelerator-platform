import os
import yaml
from pathlib import Path

def main():
    config_path = Path("app/platform.yml")

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    services = config["services"]

    os.makedirs("app/generated", exist_ok=True)

    if "container_app" in services:
        bicep = """
param appName string
param image string
param location string = resourceGroup().location

resource containerEnv 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: 'env-${appName}'
  location: location
  properties: {}
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: appName
  location: location
  properties: {
    managedEnvironmentId: containerEnv.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
      }
    }
    template: {
      containers: [
        {
          name: appName
          image: image
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
      }
    }
  }
}

output appUrl string = containerApp.properties.configuration.ingress.fqdn
"""
    else:
        bicep = """
param appName string
param image string
param location string = resourceGroup().location
"""

    with open("app/generated/main.bicep", "w") as f:
        f.write(bicep.strip())

    print("Generated app/generated/main.bicep")

if __name__ == "__main__":
    main()