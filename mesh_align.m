mdir = 'mesh3d/';
fname = 'out_p6-p4-p8';

% input from file
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
ntris = size(tris,1);

% get separate cells
cells = transpose(unique(tris(:,4)));
for cell = cells
    fprintf('  cell: %d\n',cell);
    cell_tris = tris((tris(:,4) == cell),1:3);
    ncell_tris = size(cell_tris,1);
    fprintf('    triangles: %d\n',ncell_tris);
    hold on;
    plot_mesh(cell_tris,verts,cell);
    [F,V] = stlread(sprintf('../meshes/real/blender/cell0%d.stl',cell));
    plot_mesh(F,V,cell+7);
    break;
end

[F,V] = stlread('../meshes/real/blender/tubes.stl');
plot_mesh(F,V,1);
hold off;

