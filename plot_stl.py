
##############################################################
# Code to plot/display an object stored in a binary STL file #
#                                                            #
#            Written by: Neelotpal Dutta                     #
#            [https://neelotpal-d.github.io/]                # 
##############################################################






from matplotlib import pyplot
from mpl_toolkits import mplot3d
import struct

figure=pyplot.figure()
ax=figure.add_subplot(111,projection='3d')

#########################################

file_name='3d.stl'

#########################################

x_max=-1e6
x_min=1e6
y_max=-1e6
y_min=1e6
z_max=-1e6
z_min=1e6

poly=list([])

with open(file_name,'rb') as f:
    f.read(80) #read header
    n=int.from_bytes(f.read(4),'little')
    print('Number of triangles: {}'.format(n)) #print number of triangles
    
    for i in range(n):
        [xn,yn,zn]=struct.unpack('fff',f.read(12)) #normal
        [x1,y1,z1]=struct.unpack('fff',f.read(12)) #vertex 1
        [x2,y2,z2]=struct.unpack('fff',f.read(12)) #vertex 2
        [x3,y3,z3]=struct.unpack('fff',f.read(12)) #vertex 3
        f.read(2)
        poly.append([(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)]) #store the triangle coordinates
        
        #get the extreme coordinates to adjust the axes
        x_max=max(x_max,x1,x2,x3) 
        x_min=min(x_min,x1,x2,x3)
        y_max=max(y_max,y1,y2,y3)
        y_min=min(y_min,y1,y2,y3)
        z_max=max(z_max,z1,z2,z3)
        z_min=min(z_min,z1,z2,z3)
        


poly3d=mplot3d.art3d.Poly3DCollection(poly)
poly3d.set_edgecolor('green')
ax.add_collection3d(poly3d)

ax.set_xlim3d(x_min,x_max)
ax.set_ylim3d(y_min,y_max)
ax.set_zlim3d(z_min,z_max)
pyplot.gca().set_aspect('equal', adjustable='box')
pyplot.axis('off')
pyplot.show()
