Merge "out_p6-p4-p8.msh";

//CreateTopology;

//Mesh.RemeshAlgorithm = 1; // automatic
//Mesh.RemeshParametrization = 7; // conformal finite element

cell_count = 7;
For i In {1:cell_count}
  Surface Loop(i+10) = {i};
  Volume(i+20) = {i+10};
EndFor

Mesh.Algorithm = 6; // Frontal
Mesh 3;
Save "out.msh";

//Mesh.SaveAll = 0; // default = 0

//Mesh.SurfaceEdges = 1;
//Mesh.SurfaceFaces = 0;
//Mesh.SurfaceNumbers = 0;
//Mesh.Tetrahedra = 0;
//Mesh.VolumeEdges = 1;
//Mesh.VolumeNumbers = 0;

//Mesh.ElementOrder = 2;
//Mesh.SecondOrderIncomplete = 1;
//Mesh.Format = 39;         // Abaqus format
//Mesh 2; // for 2D
//Save "file_name.inp"; // export in the same directory as geo file
