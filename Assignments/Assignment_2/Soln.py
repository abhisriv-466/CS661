import numpy as np
from ipywidgets import interact, Button
from IPython.display import display
from plotly import graph_objects as go
from plotly.graph_objects import Histogram
from vtk import *
from plotly.subplots import make_subplots
from vtk.util.numpy_support import vtk_to_numpy


# Read data from .vti file
reader = vtkXMLImageDataReader()
reader.SetFileName("C:/Users/Abhishek Srivastava/OneDrive - IIT Kanpur/Documents/4th sem/CS661/Assignment_2/mixture.vti")  # Replace with your file path
reader.Update()

# Get data points and scalar values

# Get the image data
image_data = reader.GetOutput()

# Get the number of points
num_points = image_data.GetNumberOfPoints()

# Initialize empty arrays for coordinates
x = np.empty(num_points)
y = np.empty(num_points)
z = np.empty(num_points)

# Extract point coordinates using GetPoint()
for i in range(num_points):
    point = image_data.GetPoint(i)
    x[i], y[i], z[i] = point


# data_points = reader.GetOutput().GetPoints().GetData()
scalar_data = reader.GetOutput().GetPointData().GetScalars()

# Convert data points to NumPy arrays
data = np.array(scalar_data)


# Define initial isovalue and data range
isovalue = 0.0
data_min, data_max = data.min(), data.max()


def create_plot(isoval):
  """
  This function creates the figure with isosurface and histogram plots.

  Args:
      isoval: Current isovalue for isosurface.
  """
  global isovalue

  # Isosurface plot
  iso_surface = go.Isosurface(
      x=x,
      y=y,
      z=z,
      value=data,
      isomin=isoval,
      isomax=isoval,
      showscale=False,
      colorscale="plasma"
  )

  # Histogram plot (entire data)
  hist_all = Histogram(
      x=data.flatten(),
      histfunc="count",
      histnorm="probability",
      xaxis="x2",
      yaxis="y2"
  )

  # Update histogram for subset based on isovalue
  if isoval > 0:
    filtered_data = data[data >= (isoval - 0.25)]
    filtered_data = filtered_data[filtered_data <= (isoval + 0.25)]
    hist_filtered = Histogram(
        x=filtered_data.flatten(),
        histfunc="count",
        histnorm="probability",
        xaxis="x3",
        yaxis="y3"
    )
  else:
    hist_filtered = None

  # Create subplots using make_subplots
  fig = go.Figure(make_subplots(rows=1, cols=3, specs=[[{'type': 'scatter3d'}, {'type': 'histogram'}, {'type': 'histogram'}]]))

  # Add traces to specific subplots
  fig.add_trace(iso_surface, row=1, col=1)  # Main plot on subplot (1, 1)
  fig.add_trace(hist_all, row=1, col=2)      # Histogram on subplot (1, 2)
  if hist_filtered is not None:
      fig.add_trace(hist_filtered, row=1, col=3)  # Filtered histogram (optional)

  # Update layout and subplot titles
  fig.update_layout(
      showlegend=False,
      xaxis_title="X",
      yaxis_title="Y"
  )
  fig.update_xaxes(title_text="Data Value", row=1, col=2)  # Set title for x-axis 2
  fig.update_yaxes(title_text="Probability", row=1, col=2)  # Set title for y-axis 2
  if hist_filtered is not None:
      fig.update_xaxes(title_text=f"Data Value (around {isoval})", row=1, col=3)
      fig.update_yaxes(title_text="Probability (Filtered)", row=1, col=3)


# Create initial plot
initial_plot = create_plot(isovalue)

# Slider widget for isovalue
slider = interact(create_plot, isoval=(data_min, data_max, 0.1))

# Reset button
reset_button = Button(description="Reset")


def reset_callback(b):
  global isovalue
  isovalue = 0.0
  slider.value = isovalue
  create_plot(isovalue)


reset_button.on_click(reset_callback)

# Display plots and widgets
display(initial_plot)
display(slider)
display(reset_button)

