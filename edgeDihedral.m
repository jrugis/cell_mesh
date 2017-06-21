function Beta = edgeDihedral(V,F,faceNormals,edgeFaces)

nc = size(faceNormals,1);
centroids = zeros(nc,3);
for i = 1:nc
    centroids(i,:) = sum(V(F(i,:),:))/3.0;
end

nb = size(edgeFaces,1); % allocate memory for resulting angles
Beta = zeros(nb,1);
for i = 1:nb  % iterate over edges
    indFace1 = edgeFaces(i,1); % indices of adjacent faces
    indFace2 = edgeFaces(i,2);
    normal1 = faceNormals(indFace1,:); % normal vector of adjacent faces
    normal2 = faceNormals(indFace2,:);
    Beta(i) = vectorAngle3d(normal1,normal2); % angle between two vectors
    base = centroids(indFace2,:)-centroids(indFace1,:);
    vangle = vectorAngle3d(normal1,base);
    if vangle < (pi/2.0)
        Beta(i) = -Beta(i);
    end
end
end
