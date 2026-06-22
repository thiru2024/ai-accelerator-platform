import os
import yaml

def main():
    with open("platform.yml", "r") as f:
        config = yaml.safe_load(f)

    app_name = config["app_name"]
    services = config["services"]

    os.makedirs("generated", exist_ok=True)

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

    if "container_app" not in services:
        bicep = """
param appName string
param image string
param location string = resourceGroup().location
"""

    with open("generated/main.bicep", "w") as f:
        f.write(bicep.strip())

    print("Generated generated/main.bicep")

if __name__ == "__main__":
    main()