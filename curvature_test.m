% paths to 3rd party matlab toolboxs

path(path, '~/Downloads/icosphere');
path(path, '~/Downloads/linecurvature_version1b');
path(path, '~/Downloads/patch_curvature_version1b');
path(path, '~/Downloads/toolbox_graph/toolbox_graph/');
path(path, '~/Downloads/toolbox_graph/toolbox_graph/toolbox/');

r = 1.0;

t = transpose(linspace(0,2*pi,600));
X = r.*sin(t);
Y = r.*cos(t);
%scatter(X,Y);
K = -LineCurvature2D([X,Y]);

[V,F] = icosphere(4);
V = r.*V;

Vt = transpose(r.*V);
Ft = transpose(F);
%options.curvature_smoothing = 2;
%options.verb = 0;
%[Umin,Umax,Cmin,Cmax,Cmean,Cgauss,Normal] = compute_curvature(Vt,Ft,options);

figure('visible','off');
FV = patch('Faces',F,'Vertices',V);
[Cmean,Cgaussian,Dir1,Dir2,Lambda1,Lambda2]=patchcurvature(FV); 
