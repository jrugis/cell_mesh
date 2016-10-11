//
// Execute at command line:
//     gmsh remesh.geo -3
//

//(0) nosplit (1) automatic (2) split metis
Mesh.RemeshAlgorithm=1; 

// 0=harmonic_circle, 1=conformal_spectral, 2=rbf, 3=harmonic_plane, 4=convex_circle, 
// 5=convex_plane, 6=harmonic square, 7=conformal_fe
Mesh.RemeshParametrization=0; 

// 1=MeshAdapt, 2=Automatic, 5=Delaunay, 6=Frontal, 7=BAMG, 8=DelQuad
Mesh.Algorithm=2;

// 1=Delaunay, 2=New Delaunay, 4=Frontal, 5=Frontal Delaunay, 6=Frontal Hex, 7=MMG3D, 9=R-tree
Mesh.Algorithm3D=4;

//Mesh.CharacteristicLengthFactor=0.2;
Mesh.CharacteristicLengthMin=0.4; // target length of edge
Mesh.CharacteristicLengthMax=0.6; // target length of edge

Merge "boundingS.stl";
CreateTopology;

Surface Loop(2) = {1};
Volume(3) = {2};

Mesh.Optimize=1;

