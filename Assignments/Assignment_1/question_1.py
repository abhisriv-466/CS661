
## Import VTK
from vtk import *

## Load data
#######################################
reader = vtkXMLImageDataReader()
reader.SetFileName('Isabel_2D.vti')
reader.Update()
data = reader.GetOutput()

## Query how many cells the dataset has
#######################################
numCells = data.GetNumberOfCells()
# print('number of cells :',numCells)


# C=int(input("Enter the isovalue: "))

numPoints=0
## Get a single cell from the list of cells
###########################################
dataArr = data.GetPointData().GetArray('Pressure')
points = vtkPoints()
cells = vtkCellArray()
pdata = vtkPolyData()

for C in range(-310,-300):
    for i in range(int(numCells)):
        cell = data.GetCell(i)
        pid1 = cell.GetPointId(0)
        pid2 = cell.GetPointId(1)
        pid3 = cell.GetPointId(3)
        pid4 = cell.GetPointId(2)


        val1 = dataArr.GetTuple1(pid1)
        val2 = dataArr.GetTuple1(pid2)
        val3 = dataArr.GetTuple1(pid3)
        val4 = dataArr.GetTuple1(pid4)

        p1=data.GetPoint(pid1)
        p2=data.GetPoint(pid2)
        p3=data.GetPoint(pid3)
        p4=data.GetPoint(pid4)

        # print(p1)
        # print(p2)
        # print(p3)
        # print(p4)
        
        #Comparing values at cell vertices with C
        current_points = list()
        if ((val1-C)*(val2-C))<=0:
            new_x = p1[0] + (((val1 - C) / (val1 - val2)) * (p2[0]-p1[0]))
            pc1 = p1[:0] + (new_x,)+p1[1:]
            numPoints+=1
            # count+=1
            print(pc1)
            # points.InsertNextPoint(pc1)
            current_points.append(pc1)
        if ((val2-C)*(val3-C))<=0:
            # pc2=p2+(((val2-C)/(val3-C))*(p3-p2))
            new_y = p2[1] + (((val2 - C) / (val2 - val3)) * (p3[1]-p2[1]))
            pc2 = p2[:1] + (new_y,)+p2[2:]
            # print(type(p2))
            # points.InsertNextPoint(pc2)
            # count+=1
            print(pc2)
            # points.InsertNextPoint(pc2)
            current_points.append(pc2)
            numPoints+=1
        if ((val3-C)*(val4-C))<=0:
            new_xx = p3[0] + (((val3 - C) / (val3 - val4)) * (p4[0]-p3[0]))
            pc3 = p3[:0] + (new_xx,)+p3[1:]
            # pc3=p3+(((val3-C)/(val4-C))*(p4-p3))
            # points.InsertNextPoint(pc3)
            current_points.append(pc3)
            print(pc3)
            numPoints+=1
            # count+=1
        if ((val4-C)*(val1-C))<=0:
            # pc4=p4+(((val4-C)/(val1-C))*(p1-p4))
            # points.InsertNextPoint(pc4)
            new_yy = p4[1] + (((val4 - C) / (val4 - val1)) * (p1[1]-p4[1]))
            pc4 = p4[:1] + (new_yy,)+p4[2:]
            numPoints+=1
            print(pc4)
            # count+=1
            # points.InsertNextPoint(pc4)
            current_points.append(pc4)
        
        # print(numPoints)
        
        for point in current_points:
            points.InsertNextPoint(point)
        
        polyLine = vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(len(current_points))
        for j in range(len(current_points)):
            polyLine.GetPointIds().SetId(j, j+numPoints-len(current_points))

        # Insert polyline into vtkCellArray
        cells.InsertNextCell(polyLine)
        # print(len(current_points))

        
# for C in range(-1430,-1425):
#     for i in range(int(numCells)):
#         cell = data.GetCell(i)
#         pid1 = cell.GetPointId(0)
#         pid2 = cell.GetPointId(1)
#         pid3 = cell.GetPointId(3)
#         pid4 = cell.GetPointId(2)


#         val1 = dataArr.GetTuple1(pid1)
#         val2 = dataArr.GetTuple1(pid2)
#         val3 = dataArr.GetTuple1(pid3)
#         val4 = dataArr.GetTuple1(pid4)

#         p1=data.GetPoint(pid1)
#         p2=data.GetPoint(pid2)
#         p3=data.GetPoint(pid3)
#         p4=data.GetPoint(pid4)

#         # print(p1)
#         # print(p2)
#         # print(p3)
#         # print(p4)
        
#         #Comparing values at cell vertices with C
#         current_points = list()
#         if ((val1-C)*(val2-C))<=0:
#             new_x = p1[0] + (((val1 - C) / (val1 - val2)) * (p2[0]-p1[0]))
#             pc1 = p1[:0] + (new_x,)+p1[1:]
#             numPoints+=1
#             # count+=1
#             print(pc1)
#             # points.InsertNextPoint(pc1)
#             current_points.append(pc1)
#         if ((val2-C)*(val3-C))<=0:
#             # pc2=p2+(((val2-C)/(val3-C))*(p3-p2))
#             new_y = p2[1] + (((val2 - C) / (val2 - val3)) * (p3[1]-p2[1]))
#             pc2 = p2[:1] + (new_y,)+p2[2:]
#             # print(type(p2))
#             # points.InsertNextPoint(pc2)
#             # count+=1
#             print(pc2)
#             # points.InsertNextPoint(pc2)
#             current_points.append(pc2)
#             numPoints+=1
#         if ((val3-C)*(val4-C))<=0:
#             new_xx = p3[0] + (((val3 - C) / (val3 - val4)) * (p4[0]-p3[0]))
#             pc3 = p3[:0] + (new_xx,)+p3[1:]
#             # pc3=p3+(((val3-C)/(val4-C))*(p4-p3))
#             # points.InsertNextPoint(pc3)
#             current_points.append(pc3)
#             print(pc3)
#             numPoints+=1
#             # count+=1
#         if ((val4-C)*(val1-C))<=0:
#             # pc4=p4+(((val4-C)/(val1-C))*(p1-p4))
#             # points.InsertNextPoint(pc4)
#             new_yy = p4[1] + (((val4 - C) / (val4 - val1)) * (p1[1]-p4[1]))
#             pc4 = p4[:1] + (new_yy,)+p4[2:]
#             numPoints+=1
#             print(pc4)
#             # count+=1
#             # points.InsertNextPoint(pc4)
#             current_points.append(pc4)
        
#         # print(numPoints)
        
#         for point in current_points:
#             points.InsertNextPoint(point)
        
#         polyLine = vtkPolyLine()
#         polyLine.GetPointIds().SetNumberOfIds(len(current_points))
#         for j in range(len(current_points)):
#             polyLine.GetPointIds().SetId(j, j+numPoints-len(current_points))

#         # Insert polyline into vtkCellArray
#         cells.InsertNextCell(polyLine)
#         # print(len(current_points))

        



        
    
    
number_of_points = cells.GetNumberOfCells()

print(f"Number of points in vtkPoints: {number_of_points}")
pdata.SetPoints(points)
pdata.SetLines(cells)
# print(polyLine)
### Store the polydata into a vtkpolydata file with extension .vtp
###################################################################

# print(pdata)

writer = vtkXMLPolyDataWriter()
writer.SetFileName('Export_question1.vtp')
writer.SetInputData(pdata)
writer.Write()