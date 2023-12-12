import paraview.simple
from paraview.simple import Sphere

paraview.simple._DisableFirstRenderCameraReset()

# create a new "Sphere"
sphere1 = Sphere(registrationName="Sphere1")
# Properties modified on sphere1
sphere1.ThetaResolution = 32
sphere1.PhiResolution = 32
assert sphere1.PointData.NumberOfArrays == 1
