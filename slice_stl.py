

######################################################
# Code to create planar slices from a binarySTL file #
#                                                    #
#         Written by: Neelotpal Dutta                #
#        [https://neelotpal-d.github.io/]            # 
######################################################





'''
Note that this code was not written to be used to
print the objects. This is just to visualise the
process of slicing used in 3D printing. The
current version does not include infill. However,
the code can be modified to produce printable
tool paths
'''




from matplotlib import pyplot
from mpl_toolkits import mplot3d
import struct
import numpy

figure=pyplot.figure()
ax=figure.add_subplot(111,projection='3d')





##############################################
file_name='3dsample.stl' #name/path of the STL file

S=1.0 #Layer gap, units
##############################################



x_max=-1e6
x_min=1e6
y_max=-1e6
y_min=1e6
z_max=-1e6
z_min=1e6


slices=list([])
slice_lines=[]


#Read the STL file once to find the extreme coordinates to
#translate the base of the object to XY plane
with open(file_name,'rb') as f:
    f.read(80) #file header
    n=int.from_bytes(f.read(4),'little')
    
    for i in range(n):
        [xn,yn,zn]=struct.unpack('fff',f.read(12)) #normal
        [x1,y1,z1]=struct.unpack('fff',f.read(12)) #Vertex 1
        [x2,y2,z2]=struct.unpack('fff',f.read(12)) #Vertex 2
        [x3,y3,z3]=struct.unpack('fff',f.read(12)) #Vertex 3
        f.read(2)
        
        x_max=max(x_max,x1,x2,x3)
        x_min=min(x_min,x1,x2,x3)
        y_max=max(y_max,y1,y2,y3)
        y_min=min(y_min,y1,y2,y3)
        z_max=max(z_max,z1,z2,z3)
        z_min=min(z_min,z1,z2,z3)



#Read the file again to slice the object from z=0
with open(file_name,'rb') as f:
    f.read(80) 
    n=int.from_bytes(f.read(4),'little')
    print('Number of triangles: {}'.format(n)) #print number of triangles
    print('Number of layers: {}'.format(1+numpy.floor((z_max-z_min)/S))) #print number of layers
    
    for i in range(n):
        [xn,yn,zn]=struct.unpack('fff',f.read(12))
        [x1,y1,z1]=struct.unpack('fff',f.read(12))
        [x2,y2,z2]=struct.unpack('fff',f.read(12))
        [x3,y3,z3]=struct.unpack('fff',f.read(12))
        [z1,z2,z3]=[z1-z_min,z2-z_min,z3-z_min]
        f.read(2)
        vert_tup=[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)] #The triangle/3 vertices
        
    
        # If the traiangle is on the slicing plane
        if(z1==z2 and z2==z3):
            continue

        L1=(z1/S) #To determine the closest slicing plane below or on the point
        L2=(z2/S)
        L3=(z3/S)
        
        
        L=numpy.floor([L1,L2,L3])
        
        on_layer_flag=0
        odd=0
        
        #determine the edge parallel to slicing plane
        if (z1==z2):
            on_layer_flag+=1
            odd=3
            
        if (z2==z3):
            on_layer_flag+=1
            odd=1
        if (z1==z3):
            on_layer_flag+=1
            odd=2
        
        L_max=numpy.floor(max(L1,L2,L3))
        L_min=numpy.floor(max(L1,L2,L3))

        
        # If one edge is parallel to the slicing plane
        if(on_layer_flag==1): 
            zs=[1,2,3]
            zs.remove(odd)

            #If parallel edge on slicing plane
            if(vert_tup[zs[0]-1][2]%S==0):
                line_vertices=[vert_tup[zs[0]-1],vert_tup[zs[1]-1]] #the parallel edge
                slice_lines.append(line_vertices)
                
                line_vertices=[]

                #if more slicing planes intersect the triangle
                if((L[odd-1]>L[zs[0]-1]+1 or L[odd-1]<L[zs[0]-1]-1)):
                    [xa,ya,za]=[vert_tup[odd-1][0],vert_tup[odd-1][1],vert_tup[odd-1][2]]
                    [xb,yb,zb]=[vert_tup[zs[0]-1][0],vert_tup[zs[0]-1][1],vert_tup[zs[0]-1][2]]
                    [xc,yc,zc]=[vert_tup[zs[1]-1][0],vert_tup[zs[1]-1][1],vert_tup[zs[1]-1][2]]
                    
                    
                    z_p1=L[odd-1]*S
                    if(za<zb): z_p1=z_p1+S
                    
                    while abs(z_p1-zb)>0:
                        if za==z_p1:
                            z_p1=z_p1+(S*(zb-z_p1))/abs(zb-z_p1)
                            continue
                        
                        x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                        y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb
                        
                        x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                        y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc
                        
                        line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                        
                        slice_lines.append(line_vertices)
                        if zb>z_p1:
                            z_p1=z_p1+S
                        else:
                            z_p1=z_p1-S
                        
            #If parallel edge not on slicing plane         
            elif ((L[odd-1]>L[zs[0]-1] or L[odd-1]<L[zs[0]-1])):
                [xa,ya,za]=[vert_tup[odd-1][0],vert_tup[odd-1][1],vert_tup[odd-1][2]]
                [xb,yb,zb]=[vert_tup[zs[0]-1][0],vert_tup[zs[0]-1][1],vert_tup[zs[0]-1][2]]
                [xc,yc,zc]=[vert_tup[zs[1]-1][0],vert_tup[zs[1]-1][1],vert_tup[zs[1]-1][2]]
                z_p1=(L[odd-1])*S
                if(za<zb): z_p1=z_p1+S
                              
                while (z_p1-zb)/(za-zb)>=0:
                    if za==z_p1:
                        z_p1=z_p1+(S*(zb-z_p1))/abs(zb-z_p1)
                        continue
                    
                    x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                    y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb
                    
                    x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                    y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc
                    
                    line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                    
                    slice_lines.append(line_vertices)
                    if zb>z_p1:
                        z_p1=z_p1+S
                    else:
                        z_p1=z_p1-S

        #The remaining triangles            
        else:
            vert_tup.sort(key=lambda x:x[2])
            [xa,ya,za]=[vert_tup[0][0],vert_tup[0][1],vert_tup[0][2]]
            [xb,yb,zb]=[vert_tup[1][0],vert_tup[1][1],vert_tup[1][2]]
            [xc,yc,zc]=[vert_tup[2][0],vert_tup[2][1],vert_tup[2][2]]

          
            L1=numpy.floor(za/S)
            L2=numpy.floor(zb/S)
            L3=numpy.floor(zc/S)

            if (L1<L3):
                z_p1=L3*S

                #start from highest vertex and move down
                while(z_p1>=zb):
                    if(z_p1==zc):
                        z_p1=z_p1-S
                        continue
                    
                    x_p1=(xc-xb)*(z_p1-zb)/(zc-zb)+xb
                    y_p1=(yc-yb)*(z_p1-zb)/(zc-zb)+yb

                    x_p2=(xc-xa)*(z_p1-za)/(zc-za)+xa
                    y_p2=(yc-ya)*(z_p1-za)/(zc-za)+ya

                    line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                    slice_lines.append(line_vertices)
                    z_p1=z_p1-S


                while(z_p1>za):
                    
                    x_p1=(xa-xb)*(z_p1-zb)/(za-zb)+xb
                    y_p1=(ya-yb)*(z_p1-zb)/(za-zb)+yb

                    x_p2=(xa-xc)*(z_p1-zc)/(za-zc)+xc
                    y_p2=(ya-yc)*(z_p1-zc)/(za-zc)+yc

                    line_vertices=[(x_p1,y_p1,z_p1),(x_p2,y_p2,z_p1)]
                    slice_lines.append(line_vertices)
                    z_p1=z_p1-S
        
                
                
          

        
        
        



le=len(slice_lines)


#Plot the Lines/Boundary of the slices on by one [not sorted by height]
for v in range(le):
    ax.plot([slice_lines[v][0][0],slice_lines[v][1][0]],[slice_lines[v][0][1],slice_lines[v][1][1]],[slice_lines[v][0][2],slice_lines[v][1][2]])

    
x_range=x_max-x_min
y_range=y_max-y_min
z_range=z_max

max_range=max(x_range,y_range,z_range)
half_range=max_range/2.0

x_mean=0.5*(x_max+x_min)
y_mean=0.5*(y_max+y_min)
z_mean=0.5*(z_max)

ax.auto_scale_xyz([x_mean-half_range,x_mean+half_range],[y_mean-half_range,y_mean+half_range],[z_mean-half_range,z_mean+half_range])
ax.set_aspect('equal', adjustable='box')

pyplot.axis('off')
pyplot.show()








