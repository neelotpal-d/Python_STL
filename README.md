# Python_STL

This repository contains the python class `stl_object` and related modules to handle binary STL files.

------------------------------

## stl_object
Contains class `stl_object`
```
stl_object() -> empty stl_object

stl_object(triangles,normals,header,triangle_numbers) -> new stl_object
--- assigns: 
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
        
triangles: List of triangles (List) of 3 tupules, each tupule (x,y,z) is a vertex of the triangle
    [[(xa,ya,za),(xb,yb,zb),(xc,yc,zc)],..]         
normals: List of tupules (x,y,z) representing normals of the corresponding triangle in list
    [(x,y,z),...]
header: string
triangle_numbers: int
*Assign x_max,x_min, y_max... after creation of stl_object using parameters

```


### Methods:

- `read_from_file`

```
stl_object.read_from_file('file_path/file_name') -> None -- fill an empty stl_object

```

- `display`

```
stl_object.display(axis='on'/'off') -> None -- display an stl object
```

- `rotated_max_min`

```
stl_object.rotated_max_min(direction) -> float,float,float,float,float,float,numpy.array 
-- returns x_max_new,x_min_new,y_max_new,y_min_new,z_max_new,z_min_new,rot_mat with 'direction' towards z axis

direction: [x,y,z] direction of z axis w.r.t original coordinates system
```
### Example:
```
from python_STL import stl_object

object_=stl_object.stl_object()
object_.read_from_file('3d.stl')
object_.display()

```

------------------------------

## stl_slicer
Contains function `slice` to create planar slices from a `stl_object`

```
slice(self,S,display=True,direction=[0,0,1]) -> List of Lines, where Lines is a list of two point, where a point is a tupule of three floats (x,y,z)

display the slices if display= True

S: Slice layer height (units in original system)
direction: direction of Z axis (w.r.t. original coordinate) along which the objects is sliced
```
### Example:
```

from python_STL import stl_object,stl_slicer

object_=stl_object.stl_object()
object_.read_from_file('3d.stl')
stl_slicer.slice(object_,S=10)
```
*Note that this code was not written to be used to print the objects. This is just to visualise the process of slicing used in 3D printing. The current version does not include infill and **does not produce the G codes**. However, the code can be modified to produce printable tool paths.*



-------------------------------


