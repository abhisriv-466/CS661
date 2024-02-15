from vtk import *

# Load 3D data
reader = vtkXMLImageDataReader()  # Assuming a .vti file
reader.SetFileName('Isabel_3D.vti')
reader.Update()

# Transfer functions (replace with actual values from your tables)
colorTransferFunction = vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(-4931.54,0.0,1.0,1.0)
colorTransferFunction.AddRGBPoint(-2508.95,0.0,0.0,1.0)
colorTransferFunction.AddRGBPoint(-1873.9,0.0,0.0,0.5)
colorTransferFunction.AddRGBPoint(-1027.16,1.0,0.0,0.0)
colorTransferFunction.AddRGBPoint(-298.031,1.0,0.4,0.0)
colorTransferFunction.AddRGBPoint(2594.97,1.0,1.0,0.0)  # Example point
# ... add more points as needed

opacityTransferFunction = vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(-4931.54, 1.0)
opacityTransferFunction.AddPoint(101.815, 0.002)
opacityTransferFunction.AddPoint(2594.97,0.0)
  # Example point
# ... add more points as needed

# Volume mapper
volumeMapper = vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetRequestedRenderModeToGPU()  # Optional for GPU acceleration

# Phong shading (optional)
phongShading = input("Do you want to use Phong shading? (yes/no): ")
if phongShading.lower() == "yes":
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.SetAmbient(0.5)
    volumeProperty.SetDiffuse(0.5)
    volumeProperty.SetSpecular(0.5)
    volumeProperty.SetSpecularPower(10.0)
else:
    volumeProperty = vtkVolumeProperty()
    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOff()  # Ensure Phong shading is off

# Volume actor
volumeActor = vtkVolume()
volumeActor.SetMapper(volumeMapper)
volumeActor.SetProperty(volumeProperty)

# Outline
outlineFilter = vtkOutlineFilter()
outlineFilter.SetInputConnection(reader.GetOutputPort())

outlineMapper = vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineFilter.GetOutputPort())

outlineActor = vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(0.0, 0.0, 0.0)  # Set outline color

# Renderer and render window
renderer = vtkRenderer()
renderer.AddActor(volumeActor)
renderer.AddActor(outlineActor)
renderer.SetBackground(1.0, 1.0, 1.0)  # Set background color

renderWindow = vtkRenderWindow()
renderWindow.AddRenderer(renderer)
renderWindow.SetSize(1000, 1000)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderWindow)

# Render
renderWindow.Render()
interactor.Start()
