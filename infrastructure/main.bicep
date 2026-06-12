param appName string
param image string
param location string = resourceGroup().location

module app './modules/container-app.bicep' = {
  name: '${appName}-container-app'
  params: {
    appName: appName
    image: image
    location: location
  }
}