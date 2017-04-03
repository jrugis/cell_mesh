%**************************************************************************
% meshmorph.m
% Iteratively smooth a multi-cell mesh file. 
% Output a separate gmsh .msh file for each cell.
%
mdir = 'mesh3d/';
fname = 'out_N4_p3-p2-p4';
%
iterations = 10; % number of smoothing iterations

%**************************************************************************
% paths to 3rd party matlab toolboxs
path(path, '~/Downloads/alecjacobson-gptoolbox-00c124c/mesh');
path(path, '~/Downloads/geom3d/meshes3d');
path(path, '~/Downloads/geom3d/geom3d');
path(path, '~/Downloads/unifyMeshNormals');
path(path, '~/Downloads/smoothpatch_version1b');
path(path, '~/Downloads/toolbox_graph/toolbox_graph/');
path(path, '~/Downloads/toolbox_graph/toolbox_graph/toolbox/');

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
cell_curv = cell(ncells,iterations+1); % curvature
for c = cells
    fprintf('separate cell: %d',c);
    temp = tris((tris(:,4) == c),1:3);
    cell_tris{c} = unifyMeshNormals(temp,V,'alignTo','out');
    cell_edges{c} = meshEdges(cell_tris{c});
    cell_surf{c,1} = meshSurfaceArea(V,cell_edges{c},cell_tris{c});
    [ccent,cell_vol{c,1}] = centroid(V,cell_tris{c});
    fprintf('    volume: %4.2f  surface area: %4.2f',...
        cell_vol{c,1},cell_surf{c,1});
    % compute and store the curvature
    options.curvature_smoothing = 0;
    options.verb = 0;
    [Umin,Umax,Cmin,Cmax,Cmean,Cgauss,Normal] = ...
        compute_curvature(transpose(V),...
        transpose(cell_tris{c}),options);
    cell_curv{c,1} = Cmean(unique(cell_tris{c}));
    fprintf('  curvature std: %4.4f\n',std(cell_curv{c,1}));
    % check mesh Euler characteristic
    %if size(cell_curv{c,1})-size(cell_edges{c})+size(cell_tris{c}) == 2
    %    fprintf('ok\n');
    %end
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
        fprintf('    volume: %4.2f  surface area: %4.2f',...
            cell_vol{c,i+1},cell_surf{c,i+1});

        % compute and store the curvature
        [Umin,Umax,Cmin,Cmax,Cmean,Cgauss,Normal] = ...
            compute_curvature(transpose(V),...
            transpose(cell_tris{c}),options);
        cell_curv{c,i+1} = Cmean(unique(cell_tris{c}));
        fprintf('  curvature std: %4.4f\n',std(cell_curv{c,i+1}));
    end
end
% plot curvature histogram
%figure;
%hold on;
%histogram(cell_curv{1,1},...
%    'Normalization','probability','NumBins',100,'Binlimits',[-0.5,0.5]);
%histogram(cell_curv{1,11},...
%    'Normalization','probability','NumBins',100,'Binlimits',[-0.5,0.5]);
%hold off;

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

%**************************************************************************
%**************************************************************************
