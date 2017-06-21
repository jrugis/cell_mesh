function [CMean CWeight] = SurfaceCurvature(V,E,F,Vi)
sz = size(V,1);
CMean = zeros(sz,1);
CWeight = zeros(sz,1);

faceNormals = faceNormal(V,F);
edgeFaces = trimeshEdgeFaces(V,E,F);
edgeAngles = edgeDihedral(V,F,faceNormals,edgeFaces);
edgeLengths = meshEdgeLength(V,E,F);
faceAreas = triangleArea3d([V(F(:,1),:)], [V(F(:,2),:)], [V(F(:,3),:)]);
%usedVertices = unique(F);      % list of vertex indices
usedVertices = Vi;

for i = (1:size(usedVertices,1))
    [row col] = find(F==usedVertices(i));
    areaSum = sum(faceAreas(row));
    [row col] = find(E==usedVertices(i));
    angleSum = sum(edgeAngles(row).*edgeLengths(row));
    CMean(i) = 0.75 * angleSum / areaSum;
    CWeight(i) = areaSum / 3.0;
end
end
