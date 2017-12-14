#!/usr/bin/env python3

import math
import stl
from stl import mesh
import numpy
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
from shapely import geometry


# THIS SECTION CAN BE MODIFIED MANUALLY BY THE USER ########################

# importing ths stl file
your_mesh = mesh.Mesh.from_file('box.stl')
thickness = 1

# END OF THE SECTION ##############################################


# calculating the triangle number in the stl file
triangle_tuple = your_mesh.points.shape
triangle_list = list(triangle_tuple)
triangle_number = triangle_list[0]

# converting "numpy nd.array" type into "list" type
big_list = []
for k in range(triangle_number):
    
    b = list(your_mesh[k,:])
    big_list = big_list + [b]
    


# find the max dimensions, so we can know the bounding box, getting the height,
# width, length (because these are the step size)...
minx = maxx = miny = maxy = minz = maxz = None
for p in your_mesh.points:
    # p contains (x, y, z)
    if minx is None:
        minx = p[stl.Dimension.X]
        maxx = p[stl.Dimension.X]
        miny = p[stl.Dimension.Y]
        maxy = p[stl.Dimension.Y]
        minz = p[stl.Dimension.Z]
        maxz = p[stl.Dimension.Z]
    else:
        maxx = max(p[stl.Dimension.X], maxx)
        minx = min(p[stl.Dimension.X], minx)
        maxy = max(p[stl.Dimension.Y], maxy)
        miny = min(p[stl.Dimension.Y], miny)
        maxz = max(p[stl.Dimension.Z], maxz)
        minz = min(p[stl.Dimension.Z], minz)


z_maxx = maxz
z_minn = minz

# they had to be converted into integer to be used in loops
z_max = int(z_maxx)
z_min = int(z_minn)



main_list = []






def slicer(z_val):
    # in a specified layer, goes through all the vertices triangle by triangle, see if any of the vertices intersect the cutting plane
    # If a vertice intersects the cutting plane, by knowing the z value, x and y coordinates are obtained and appended to the vertices list
    # Then those vertices will be connected through a line and the contour will be obtained
    # All 5 of the scenarios are gone through and proper one is selected
    case = 0
    x_y_val = []
    cutting_ver = []
    sc4_list = []
    add_triangle = []
    val = 0
    for i in big_list:
        z_com = [i[2], i[5], i[8]] # a list of z coordinates of the 3 points of the triangle
         
        
        #scenario1:
        # no intersection found
        if (z_com[0] > z_val and z_com[1] > z_val and z_com[2] > z_val) or \
            (z_com[0] < z_val and z_com[1] < z_val and z_com[2] < z_val): 
            pass
             
                   
        
        
        #scenario2:
        # only one of the vertices intersects with the cutting plane
        elif (z_com[0] == z_val and z_com[1] != z_val and z_com[2] != z_val) or \
               (z_com[0] != z_val and z_com[1] == z_val and z_com[2] != z_val) or \
               (z_com[0] != z_val and z_com[1] != z_val and z_com[2] == z_val): 
                pass
            
        
        
        #scenario3:
        # 2 vertices on the cutting plane. So intersection is a full line. But at the moment we only store the vertices of the line
        # 
        elif (z_com[0] == z_val and z_com[1] == z_val and z_com[2] != z_val ) or (z_com[0] == z_val and z_com[2] == z_val and z_com[1] != z_val) or (z_com[2] == z_val and z_com[1] == z_val and z_com[0] != z_val):
            if z_com[0] == z_val and z_com[1] == z_val and z_com[2] != z_val:
                var = 3

            elif z_com[0] == z_val and z_com[2] == z_val and z_com[1] != z_val:
                var = 2

            else:
                var = 1

            z_list = [0,1,2]
            new_z_list = z_list
            new_z_list.remove(var - 1)
            x_y_val.extend((i[new_z_list[0]*3], i[new_z_list[0]*3+1], i[new_z_list[1]*3], i[new_z_list[1]*3+1]))               


        
        #scenario4:
        # all 3 vertices are on the cutting plane
        elif (z_com[0] == z_val and z_com[1] == z_val and z_com[2] == z_val):
            pass        


        #scenario5:
        ### the detailed exlanation is made in the report with a flow chart and mathemitacal model
        
        elif (z_com[0] > z_val and z_com[1] < z_val and z_com[2] < z_val) or \
              (z_com[0] < z_val and z_com[1] > z_val and z_com[2] < z_val) or \
              (z_com[0] < z_val and z_com[1] < z_val and z_com[2] > z_val) or \
              (z_com[0] < z_val and z_com[1] > z_val and z_com[2] > z_val) or \
              (z_com[0] > z_val and z_com[1] < z_val and z_com[2] > z_val) or \
              (z_com[0] > z_val and z_com[1] > z_val and z_com[2] < z_val): 
            
            # a new list of the same z coordinates
            z_com_new = z_com
            # z value of the cutting plane is subrtracted from the each z coordinate, to find out which points will be above the plane
            # and which will be below the blane
            z_com_new = [ j - z_val for j in z_com_new ]   
               
            # a new list created, and then filled with the positive values(z coordinates over the cutting plance)      
            pos_neg = []
            pos_neg[:] =[x > 0 for x in z_com_new]
            
            
            spn = sum(pos_neg)
                           
            
            
            if spn == 1:
              
              single_point_index = pos_neg.index(True)
              case = 1            
              
              
            else:
              single_point_index = pos_neg.index(False)
              case = 2                                         
            
              
            dummy_list = [0,1,2]
            other_dummy_list =dummy_list
            other_dummy_list.remove(single_point_index)
            
            # x, y and z coordinates of the point that is singly above/below the plane
            x_1 = i[single_point_index*3]
            y_1 = i[single_point_index*3+1]
            z_1 = i[single_point_index*3+2]
            
            # x, y and z coordinates of the other points
            x_2 = i[other_dummy_list[0]*3]
            y_2 = i[other_dummy_list[0]*3+1]
            z_2 = i[other_dummy_list[0]*3+2]
             
            x_3 = i[other_dummy_list[1]*3]
            y_3 = i[other_dummy_list[1]*3+1]
            z_3 = i[other_dummy_list[1]*3+2]
            
            
            
            # x and y coordinates of the tail and head of the lines

            if case == 1:

                if x_1 == x_2:
                    x_n_1 = x_1                                       
                else:
                    x_n_1 = (x_1 - x_2)*(z_val - z_2)/(z_1 - z_2)
                    if x_n_1 < 0:
                        x_n_1 = x_n_1 + max(x_2,x_3)

                if y_1 == y_2:
                    y_n_1 = y_2
                else:
                    y_n_1 = (y_1 - y_2)*(z_val - z_2)/(z_1 - z_2)
                    if y_n_1 < 0:
                        y_n_1 = y_n_1 + max(y_2,y_3)
                
                if x_1 == x_3:
                    x_n_2 = x_1
                else:
                    x_n_2 = (x_1 - x_3)*(z_val - z_3)/(z_1 - z_3)
                    if x_n_2 < 0:
                        x_n_2 = x_n_2 + max(x_3,x_2)
               
                if y_1 == y_3:
                    y_n_2 = y_1
                else:
                    y_n_2 = (y_1 - y_3)*(z_val - z_3)/(z_1 - z_3)
                    if y_n_2 < 0:
                        y_n_2 = y_n_2 + max(y_3,y_2)
                
            elif case==2:
                if x_1 == x_2:
                    x_n_1 = x_1                                       
                else:                                   
                    x_n_1 = (x_2 - x_1)*(z_val - z_1)/(z_2 - z_1)
                    if x_n_1 < 0:
                        x_n_1 = x_n_1 + max(x_2,x_3)

                if y_1 == y_2:
                    y_n_1 = y_2
                else:
                    y_n_1 = (y_2 - y_1)*(z_val - z_1)/(z_2 - z_1)
                    if y_n_1 < 0:
                        y_n_1 = y_n_1 + max(y_2,y_3)
                
                if x_1 == x_3:
                    x_n_2 = x_1
                else:
                    x_n_2 = (x_3 - x_1)*(z_val - z_1)/(z_3 - z_1)
                    if x_n_2 < 0:
                        x_n_2 = x_n_2 + max(x_3,x_2)

                if y_1 == y_3:
                    y_n_2 = y_1
                else:
                    y_n_2 = (y_3 - y_1)*(z_val - z_1)/(z_3 - z_1)
                    if y_n_2 < 0:
                        y_n_2 = y_n_2 + max(y_3,y_2)           
                                
                
                
                
            
            n_1 = [x_n_1, y_n_1]
            n_2 = [x_n_2, y_n_2] 
            
            
            x_y_val.extend((x_n_1, y_n_1,x_n_2, y_n_2))
            


        
        
        

    return x_y_val

# as "for" can't loop with float values, the following correction is done, by normalizing z_max and z_min over thickness, so that the increment for the following for loop is 1
thickness_correction = 1 / thickness
z_min_correction = int( z_min * thickness_correction)
z_max_correction = int(z_max * thickness_correction)
z_val = 0

# for each z value of the intersecting place, which varies with respect to thickness, slicer function is called, and the result is added to the list "main_list"       
for range_var in range(z_min_correction, z_max_correction+1, 1):    
    
    main_list = main_list + [slicer(z_val)]    
    z_val = z_val + thickness

print(main_list,"main_list")


        
       
        
################################################


# we are also at the edge of finishing the converting of the file into bmp format by using a package, which contains also variables for resolution, but then we had some problems
# by plotting the file perfectly, thus that part will be demonstrated in the final report.




