%**************************************************************************
% cell_curvature.m
% Calculate the curvature for each of the seven cells 
% using the image stack. 
% Output the standard deviation of the curvature for each cell.
%
mdir = 'layers/';
fnames = dir(strcat(mdir,'cells_*a.tif'));

%**************************************************************************
% paths to 3rd party matlab toolboxs
path(path, '~/Downloads/linecurvature_version1b');

%**************************************************************************
cells = [0.5833;...
         0.4939;...
         0.3723;...
         0.1727;...
         0.7335;...
         0.0512;...
         0.8428];

cell_curv = cell(7,1);
for i = 1:size(fnames) % iterate through image stack
    im = rgb2hsv(imread(strcat(mdir,fnames(i).name)));
    im = im(:,:,1);            % only hue required
    vals = unique(im(:,:,1));  % list of hue values for each cell
    vals = vals(vals>0);       % don't want background in the list
    for v = transpose(vals)
        temp = im;             % make binary image
        temp(temp==v) = 1;
        temp(temp<1) = 0;
        bd = bwboundaries(temp);              % extract boundary curve
        %figure;
        %hold on;
        %scatter(bd{1}(:,1), bd{1}(:,2));
        X = sgolayfilt(bd{1}(:,1),5,35);      % smooth the boundary curve
        Y = sgolayfilt(bd{1}(:,2),5,35);
        K = LineCurvature2D([X,Y]);           % calculate curvatures
        ind = find(abs(cells-v) < 0.001);     % which cell?
        cell_curv{ind} = [cell_curv{ind};K];  % store curvatures
        %scatter(X,Y);
        %fprintf('%d %d %4.4f %4.4f\n',size(bd{1}),v,std(K));
        %fprintf('%d %4.4f %4.4f\n',ind,v,std(K));
    end
end
for i = (1:7)
    c = cell_curv{i,:};
    fprintf('%4.4f\n',std(c));
end






