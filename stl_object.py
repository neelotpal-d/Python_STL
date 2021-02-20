

from matplotlib import pyplot
from mpl_toolkits import mplot3d
import struct
import numpy


    

class stl_object:
    '''
    stl_object() -> new empty stl_object
    stl_object(triangles,normals,header,triangle_numbers) -> new stl_object
        triangles: List of triangles (List) of 3 tupules, each tupule (x,y,z) is a vertex of the triangle
                    [[(xa,ya,za),(xb,yb,zb),(xc,yc,zc)],..]         
        normals: List of tupules (x,y,z) representing normals of the corresponding triangle in list
                    [(x,y,z),...]
        header: string
        triangle_numbers: int
        *Assign x_max,x_min, y_max... after creation of stl_object using parameters
    '''
    def __init__(self,triangles=None,normals=None,header=None,triangle_numbers=None):
        
        self.triangles=triangles
        self.normals=normals
        self.header=header
        self.triangle_numbers=triangle_numbers
        self.x_max=None
        self.x_min=None
        self.y_max=None
        self.y_min=None
        self.z_max=None
        self.z_min=None
        

    def read_from_file(self,file_name):
        '''
        stl_object.read_from_file('file_path/file_name') -> None -- fill an empty stl_object
        '''
        self.x_max=-1e6
        self.x_min=1e6
        self.y_max=-1e6
        self.y_min=1e6
        self.z_max=-1e6
        self.z_min=1e6

        self.triangles=list([])
        self.normals=list([])
        

        with open(file_name,'rb') as f:
            self.header=f.read(80).decode() #read header
            self.triangle_numbers=int.from_bytes(f.read(4),'little')
            
            
            for i in range(self.triangle_numbers):
                [xn,yn,zn]=struct.unpack('fff',f.read(12)) #normal
                [x1,y1,z1]=struct.unpack('fff',f.read(12)) #vertex 1
                [x2,y2,z2]=struct.unpack('fff',f.read(12)) #vertex 2
                [x3,y3,z3]=struct.unpack('fff',f.read(12)) #vertex 3
                f.read(2)
                self.normals.append([xn,yn,zn])
                self.triangles.append([(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)]) #store the triangle coordinates
            
                #get the extreme coordinates to adjust the axes
                self.x_max=max(self.x_max,x1,x2,x3) 
                self.x_min=min(self.x_min,x1,x2,x3)
                self.y_max=max(self.y_max,y1,y2,y3)
                self.y_min=min(self.y_min,y1,y2,y3)
                self.z_max=max(self.z_max,z1,z2,z3)
                self.z_min=min(self.z_min,z1,z2,z3)
                
            print('{} triangles read from {} with header {}'.format(self.triangle_numbers,file_name,self.header)) #print number of triangles
            

    def display(self,axis='off'):
        '''
        stl_object.display() -> None -- display an stl object
        '''
        
        figure=pyplot.figure()
        ax=figure.add_subplot(111,projection='3d')
        
        x_range=self.x_max-self.x_min
        y_range=self.y_max-self.y_min
        z_range=self.z_max-self.z_min

        max_range=max(x_range,y_range,z_range)
        half_range=max_range/2.0

        x_mean=0.5*(self.x_max+self.x_min)
        y_mean=0.5*(self.y_max+self.y_min)
        z_mean=0.5*(self.z_max+self.z_min)



        poly3d=mplot3d.art3d.Poly3DCollection(self.triangles)
        poly3d.set_edgecolor('green')
        ax.add_collection3d(poly3d)


        ax.auto_scale_xyz([x_mean-half_range,x_mean+half_range],[y_mean-half_range,y_mean+half_range],[z_mean-half_range,z_mean+half_range])
        ax.set_aspect('equal', adjustable='box')
        
        pyplot.axis(axis)
        if axis=='on':
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        pyplot.show()






    def rotated_max_min(self,direction):
        '''
        stl_object.rotated_max_min(direction) -> float,float,float,float,float,float,numpy.array
        -- returns x_max_new,x_min_new,y_max_new,y_min_new,z_max_new,z_min_new,rot_mat with 'direction' towards z axis
        '''
        x_max_new=-1e6
        x_min_new=1e6
        y_max_new=-1e6
        y_min_new=1e6
        z_max_new=-1e6
        z_min_new=1e6

        rot_mat=[]
        new_x=numpy.array([0,direction[2],-direction[1]])
        new_x=new_x/numpy.linalg.norm(new_x)
        new_y=numpy.cross(direction,new_x)
        rot_mat=numpy.array([new_x,new_y,direction])

        for i in range(self.triangle_numbers):
            X_1=numpy.array([self.triangles[i][0][0],self.triangles[i][0][1],self.triangles[i][0][2]])
            X_2=numpy.array([self.triangles[i][1][0],self.triangles[i][1][1],self.triangles[i][1][2]])
            X_3=numpy.array([self.triangles[i][2][0],self.triangles[i][2][1],self.triangles[i][2][2]])


            

            X_1=numpy.dot(rot_mat,X_1)
            X_2=numpy.dot(rot_mat,X_2)
            X_3=numpy.dot(rot_mat,X_3)

            
            
            [x1,y1,z1]=X_1
            [x2,y2,z2]=X_2
            [x3,y3,z3]=X_3

            x_max_new=max(x_max_new,x1,x2,x3)
            x_min_new=min(x_min_new,x1,x2,x3)
            y_max_new=max(y_max_new,y1,y2,y3)
            y_min_new=min(y_min_new,y1,y2,y3)
            z_max_new=max(z_max_new,z1,z2,z3)
            z_min_new=min(z_min_new,z1,z2,z3)

        return x_max_new,x_min_new,y_max_new,y_min_new,z_max_new,z_min_new,rot_mat
            






   

    
