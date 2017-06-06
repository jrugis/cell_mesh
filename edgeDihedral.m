function Beta = edgeDihedral(V,F,faceNormals,edgeFaces)

nb = size(edgeFaces,1); % allocate memory for resulting angles
centroids = zeros(nb,3);
Beta = zeros(nb,1);

for i = 1:nb  % iterate over edges
    centroids(i,:) = [0.1 0.1 0.1];
end

for i = 1:nb  % iterate over edges
    indFace1 = edgeFaces(i,1); % indices of adjacent faces
    indFace2 = edgeFaces(i,2);
    normal1 = faceNormals(indFace1,:); % normal vector of adjacent faces
    normal2 = faceNormals(indFace2,:);
    Beta(i) = vectorAngle3d(normal1,normal2); % angle between two vectors
end
end
