%**************************************************************************
% mesh2msh.m
% Iteratively smooth a multi-cell mesh file. 
% Output a separate msh file for each cell.
%
mdir = 'mesh3d/';
fname = 'out_p6-p4-p8';

%**************************************************************************
% input from multi-cell mesh file
fid = fopen(strcat(mdir,fname,'.mesh'),'r');
while ~startsWith(fgetl(fid),'Vertices')
end
nverts = sscanf(fgetl(fid),'%d');
verts = transpose(fscanf(fid,'%f %f %f %*d',[3,nverts]));
verts = [verts(:,1)-35.3 35.3-verts(:,2) 11.80-verts(:,3)];
while ~startsWith(fgetl(fid),'Triangles')
end
ntris = sscanf(fgetl(fid),'%d');
tris = transpose(fscanf(fid,'%d %d %d %d',[4,ntris]));
fclose(fid);
tris = unique(tris,'rows','stable'); % remove outer face duplicates

%**************************************************************************
% separate the cells
cells = transpose(unique(tris(:,4)));
ncells = max(cells);
cell_tris = cell(ncells); % pre-allocate
cell_edges = cell(ncells); % pre-allocate
for c = cells
    fprintf('separate cell: %d \n',c);
    temp = tris((tris(:,4) == c),1:3);
    cell_tris{c} = unifyMeshNormals(temp,verts,'alignTo','out');
    cell_edges{c} = meshEdges(cell_tris{c});
end

%**************************************************************************
% create common edge array for each cell pair
%common_edges = cell(0,1);
%for i = (1:ncells-1)
%    for j = (i+1:ncells)
%        fprintf('%d:%d\n',i,j);
%        common_edges{size(common_edges,1)+1,1} = ...
%            cell_edges{i}(ismember(cell_edges{i},cell_edges{j},'rows'),:);
%   end
%end
%
%hold on;
%or ee = transpose(common_edges{7})
%    A = verts(ee,:);
%    plot3(A(:,1),A(:,2),A(:,3));
%end
%hold off;

%*********
%return;
%*********

%**************************************************************************
% iterative cell smoothing
for i = 1:100
    fprintf('smoothing iteration %d\n',i);
    for c = cells
        FV = struct('faces',cell_tris{c},'vertices',verts);
        FVs = smoothpatch(FV,1,5,0.01);
        verts = FVs.vertices;
    end
end

%**************************************************************************
% check results: plot cells and lumen 
hold on;
for c = cells
    fprintf('plot cell: %d\n',c);
    plot_mesh(cell_tris{c},verts,c);
end
[F,V] = stlread('../meshes/real/blender/tubes.stl');
plot_mesh(F,V,1);
hold off;

%**************************************************************************
% output a msh file for each cell
for c = cells
    fprintf('output msh cell: %d  ',c);
    ncell_tris = size(cell_tris{c},1);
    fprintf('  triangles: %d\n',ncell_tris);
    fid = fopen(strcat(mdir,fname,sprintf('-%d',c),'.msh'),'w');
    fprintf(fid,'$MeshFormat\n');
    fprintf(fid,'2.2 0 8\n');
    fprintf(fid,'$EndMeshformat\n');
    fprintf(fid,'$Nodes\n');
    fprintf(fid,'%d\n',nverts);
    for i = 1:nverts
        fprintf(fid,'%d %f %f %f\n',i,verts(i,:));
    end
    fprintf(fid,'$EndNodes\n');
    fprintf(fid,'$Elements\n');
    fprintf(fid,'%d\n',ncell_tris);
    for i = 1:ncell_tris
        fprintf(fid,'%d 2 2 0 %d %d %d %d\n',i,c,cell_tris{c}(i,:));
    end
    fprintf(fid,'$EndElements\n');
    fclose(fid);
end

%**************************************************************************
