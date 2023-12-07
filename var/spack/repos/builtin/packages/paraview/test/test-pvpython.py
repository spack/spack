import paraview.simple
from paraview.simple import (
    ColorBy,
    GetActiveViewOrCreate,
    GetColorTransferFunction,
    GetLayout,
    GetOpacityTransferFunction,
    GetTransferFunction2D,
    SaveScreenshot,
    Show,
    Sphere,
)

paraview.simple._DisableFirstRenderCameraReset()

# create a new "Sphere"
sphere1 = Sphere(registrationName="Sphere1")
# Properties modified on sphere1
sphere1.ThetaResolution = 32
sphere1.PhiResolution = 32
assert sphere1.PointData.NumberOfArrays == 1

try:
    renderView1 = GetActiveViewOrCreate("RenderView")
    sphere1Display = Show(sphere1, renderView1, "GeometryRepresentation")
    sphere1Display.Representation = "Surface"
    renderView1.ResetCamera(False)
    renderView1.Update()
    ColorBy(sphere1Display, ("POINTS", "Normals", "Magnitude"))
    normalsLUT = GetColorTransferFunction("Normals")
    normalsPWF = GetOpacityTransferFunction("Normals")
    normalsTF2D = GetTransferFunction2D("Normals")
    layout1 = GetLayout()
    layout1.SetSize(1988, 1176)
    renderView1.CameraPosition = [0.0, 0.0, 3.3432027854673882]
    renderView1.CameraParallelScale = 0.8652845525187569
    SaveScreenshot("test-pvpython.png", renderView1, ImageResolution=[1988, 1176])
except Exception as e:
    print("[Error] ParaView might not be built with rendering support : ", e)
