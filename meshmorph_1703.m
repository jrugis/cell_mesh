%**************************************************************************
% meshmorph.m
% Iteratively smooth a multi-cell mesh file. 
% Output a separate msh file for each cell.
%
mdir = 'mesh3d/';
fname = 'out_N4_p3-p2-p4';
%
iterations = 10; % number of smoothing iterations

%**************************************************************************
% input from multi-cell mesh file
fid = fopen(strcat(mdir,fname,'.mesh'),'r');
while ~startsWith(fgetl(fid),'Vertices')
end
Vn = sscanf(fgetl(fid),'%d');
V = transpose(fscanf(fid,'%f %f %f %*d',[3,Vn])); % vertices
V = [V(:,1)-35.3 35.3-V(:,2) 11.80-V(:,3)]; % vertex translation
while ~startsWith(fgetl(fid),'Triangles')
end
ntris = sscanf(fgetl(fid),'%d');
tris = transpose(fscanf(fid,'%d %d %d %d',[4,ntris])); % triangles
cells = transpose(unique(tris(:,4))); % list of cell ids
fclose(fid);
fprintf('  vertices: %d\n',Vn);

%**************************************************************************
% identify mesh connectivity
%**************************************************************************
% create labelled faces
Fn = ntris/2;
Fv = zeros(Fn,3); % faces
Fl = zeros(Fn,2); % face labels
for i = (1:Fn)
    Fv(i,:) = tris(2*i,1:3);
    Fl(i,:) = [tris(2*i-1,4),tris(2*i,4)];
end
fprintf('     faces: %d\n',Fn);

%**************************************************************************
% create edges, face edges, edge face count
Ev = meshEdges(Fv); % edges
En = size(Ev,1);
Fe = cell2mat(meshFaceEdges(V,Ev,Fv));
Efn = transpose(sum(Fe(:)==(1:En))); % face valence per edge
fprintf('     edges: %d\n',En);

%**************************************************************************
% find cells
%**************************************************************************
% separate the cells
tris = unique(tris,'rows','stable'); % remove outer face duplicates
cells = transpose(unique(tris(:,4)));
ncells = max(cells);
cell_tris = cell(ncells,1);            % mesh triangles
cell_edges = cell(ncells,1);           % mesh edges
cell_vol = cell(ncells,iterations+1);  % volume 
cell_surf = cell(ncells,iterations+1); % surface area
cell_cent = cell(ncells,iterations+1); % centroid
for c = cells
    fprintf('separate cell: %d',c);
    temp = tris((tris(:,4) == c),1:3);
    cell_tris{c} = unifyMeshNormals(temp,V,'alignTo','out');
    cell_edges{c} = meshEdges(cell_tris{c});
    cell_surf{c,1} = meshSurfaceArea(V,cell_edges{c},cell_tris{c});
    [cell_cent{c,1},cell_vol{c,1}] = centroid(V,cell_tris{c});
    fprintf('    volume: %4.2f  surface area: %4.2f\n',...
        cell_vol{c,1},cell_surf{c,1});
end

%**************************************************************************
% iterative smoothing
%**************************************************************************
for i = 1:iterations
    fprintf('iteration: %d\n',i);
    % cell smoothing
    for c = cells
        % save mesh in progress
        ncell_tris = size(cell_tris{c},1);
        fid = fopen(strcat(mdir,'morph/',fname,...
            sprintf('-N%d_%d',c,i-1),'.msh'),'w');
        fprintf(fid,'$MeshFormat\n');
        fprintf(fid,'2.2 0 8\n');
        fprintf(fid,'$EndMeshformat\n');
        fprintf(fid,'$Nodes\n');
        fprintf(fid,'%d\n',Vn);
        for n = 1:Vn
            fprintf(fid,'%d %f %f %f\n',n,V(n,:));
        end
        fprintf(fid,'$EndNodes\n');
        fprintf(fid,'$Elements\n');
        fprintf(fid,'%d\n',ncell_tris);
        for n = 1:ncell_tris
            fprintf(fid,'%d 2 2 0 %d %d %d %d\n',n,c,cell_tris{c}(n,:));
        end
        fprintf(fid,'$EndElements\n');
        fclose(fid);

        % smooth the cell mesh
        FV = struct('faces',cell_tris{c},'vertices',V);
        FVs = smoothpatch(FV,1,5,0.1);  % (FV,1,5,0.01)
        V = FVs.vertices;
        fprintf('cell: %d',c);

        % adjust the volume (using simple sphere volume formula)
        [ccent,cvol] = centroid(V,cell_tris{c});
        %fprintf('  center: %4.2f  %4.2f %4.2f\n',ccent(:));
        mult = nthroot(((cell_vol{c,1}-cvol)/4.189),3)/cell_vol{c,1};
        %fprintf('  %4.8f  ',mult);
        cellVi = unique(cell_tris{c});
        V(cellVi,:) = V(cellVi,:) + mult*(V(cellVi,:)-ccent);

        % store the volume, surface area and centroid
        cell_vol{c,i+1} = meshVolume(V,cell_edges{c},cell_tris{c});
        cell_surf{c,i+1} = meshSurfaceArea(V,cell_edges{c},cell_tris{c});
        cell_cent{c,i+1} = ccent;
        fprintf('    volume: %4.2f  surface area: %4.2f\n',...
            cell_vol{c,i+1},cell_surf{c,i+1});
    end
end

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
    fprintf(fid,'%d\n',Vn);
    for i = 1:Vn
        fprintf(fid,'%d %f %f %f\n',i,V(i,:));
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
% save cell morph stats
csvwrite(strcat(mdir,'cell_vol.csv'), cell2mat(cell_vol));
csvwrite(strcat(mdir,'cell_surf.csv'), cell2mat(cell_surf));
csvwrite(strcat(mdir,'cell_cent.csv'), cell2mat(cell_cent));
% plot cell morph stats
%A = transpose(cell2mat(cell_vol));
%A = transpose(cell2mat(cell_cent));
%A = transpose(cell2mat(cell_surf));
%hold on;
%for i = 1:7
%    plot(100*(A(:,i)-A(1,i))/A(1,i));
%end
%hold off;

%**************************************************************************
%**************************************************************************
