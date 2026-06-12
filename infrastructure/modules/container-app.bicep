param appName string
param location string = resourceGroup().location
param image string

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