% parameters
mdir = 'mesh3d/';
fname = 'out_p6-p4-p8';

% input
fid = fopen(strcat(mdir,fname,'.mesh'),'r');

while ~startsWith(fgetl(fid),'Vertices')
end
nverts = sscanf(fgetl(fid),'%d');
verts = transpose(single(fscanf(fid,'%f %f %f %*d',[3,nverts])));

while ~startsWith(fgetl(fid),'Triangles')
end
ntris = sscanf(fgetl(fid),'%d');
tris = transpose(int32(fscanf(fid,'%d %d %d %d',[4,ntris])));

fclose(fid);
tris = unique(tris,'rows','stable'); % remove outer face duplicates
ntris = size(tris,1);

% topology
cells = transpose(unique(tris(:,4)));
for cell = cells
    fprintf('  cell: %d\n',cell);
    cell_tris = tris((tris(:,4) == cell),1:3);
    ncell_tris = size(cell_tris,1);
    fprintf('    triangles: %d\n',ncell_tris);
end

% output

