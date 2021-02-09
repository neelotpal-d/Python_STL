# Python_STL

This repository contains python codes related objects stored as a binary STL file.

## plot_STL

This is the code to display a binary STL file. Replace the value of the variable `file_name` with the name/path of your STL file


------------------------------

## slice_STL

This is the code to slice (planar, same layer thickness) the object stored in the binary STL file in the z direction.
Replace the `file_name` and the distance between the slices, `S`. To determine `S`, the values of `z_min` and `z_max` can be observed.

*Note that this code was not written to be used to print the objects. This is just to visualise the process of slicing used in 3D printing. The current version does not include infill. However, the code can be modified to produce printable tool paths.*

-------------------------------


