
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

file_name='3dsample.stl'

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

x_range=x_max-x_min
y_range=y_max-y_min
z_range=z_max-z_min

max_range=max(x_range,y_range,z_range)
half_range=max_range/2.0

x_mean=0.5*(x_max+x_min)
y_mean=0.5*(y_max+y_min)
z_mean=0.5*(z_max+z_min)


ax.auto_scale_xyz([x_mean-half_range,x_mean+half_range],[y_mean-half_range,y_mean+half_range],[z_mean-half_range,z_mean+half_range])
ax.set_aspect('equal', adjustable='box')

pyplot.axis('off')
pyplot.show()
