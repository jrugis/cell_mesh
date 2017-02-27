function [] = plot_mesh(tris,verts,color)

x = verts(:,1);
y = verts(:,2);
z = verts(:,3);
c = color * ones(size(x));
xlabel('X');
ylabel('Y');
zlabel('Z');
axis equal;
%axis square;
%zoom on;
%set(gca,'cameraviewanglemode','manual');
%camva('manual');
trimesh(tris,x,y,z,c);
