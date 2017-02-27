%**************************************************************************
% meshmorph.m
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
% create labelled faces
Fn = ntris/2;
Fv = zeros(Fn,3); % faces
Fl = zeros(Fn,2); % face labels
for i = (1:Fn)
    Fv(i,:) = tris(2*i,1:3);
    Fl(i,:) = [tris(2*i-1,4),tris(2*i,4)];
end
fprintf('     faces: %d\n',Fn);
% check results: plot tris
%temp1 = unique(Fl,'rows')
%temp2 = ismember(Fl,[5 5],'rows');
%plot_mesh(Fv(temp2,:),V,1);

%**************************************************************************
% create edges, face edges, edge face count
Ev = meshEdges(Fv); % edges
En = size(Ev,1);
Fe = cell2mat(meshFaceEdges(V,Ev,Fv));
Efn = transpose(sum(Fe(:)==(1:En))); % face valence per edge
fprintf('     edges: %d\n',En);
%temp1 = unique(Efn);
%temp2 = hist(Efn,unique(Efn));

%**************************************************************************
% find seam edges (i.e. high valence edges) and
%      seam end-points (i.e. high valence vertices in seam)
Ehv = Ev(Efn>2,:); % seam edges
Ehvn = size(Ehv,1);
Ven = transpose(sum(Ehv(:)==(1:Vn))); % seam edge valence per end-point
%while true
%    Ven = transpose(sum(Ehv(:)==(1:Vn)));
%    isingletons = find(Ven==1); % check for singleton vertices
%    if isempty(isingletons); break; end;
%    fprintf('deleting singlestons: %d\n',size(isingletons,1));
%    [row col] = find(Ehv==isingletons);
%    Ehv(row,:) = [];  % delete singleton edges
%end
fprintf('seam edges: %d\n',Ehvn);
iVhv = find(Ven==1 | Ven>2); % indices of seam end-points, incl singletons
fprintf('end-points: %d\n',size(iVhv,1));

% check results: plot seams
%hold on;
%for ehv = transpose(Ehv)
%    A = V(ehv,:);
%    plot3(A(:,1),A(:,2),A(:,3));
%end
%hold off;
%temp1 = unique(Ven);
%temp2 = hist(Ven,unique(Ven));
% check results: plot some high valence seam vertices
%hold on;
%Vhv = V(Ven==5,:);
%scatter3(Vhv(:,1),Vhv(:,2),Vhv(:,3));
%hold off;

%**************************************************************************
% find seam vertices starting from each seam end-point
seams = {};
Ehit = zeros(Ehvn,1); % edge hit flags
for iv = transpose(iVhv) % for each seam end-point
    %fprintf('end point: %d\n',iv);
    [row, col] = find(Ehv==iv); % seam edge fan
    for r = transpose(row) % for each seam edge around end-point
        if Ehit(r)==1; continue; end;
        Ehit(r) = 1;
        %fprintf('  seam edge: %d\n',r);
        n = size(seams,1)+1;
        seams{n,1} = [iv];
        [seams{n,1}, Ehit] = SeamWalk(seams{n,1},iv,r,iVhv,Ehit,Ehv);

    end
end
fprintf('     seams: %d\n',n);
% check results: plot seams
%hold on;
%for iv = seams{1} 
%    A = V(iv,:);
%    scatter3(A(:,1),A(:,2),A(:,3));
%end
%hold off;

%**************************************************************************
%**************************************************************************
%**************************************************************************
