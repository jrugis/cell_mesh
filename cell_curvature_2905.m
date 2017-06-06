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

%**************************************************************************
cell_curv = cell(7,1);
cell_pnts = cell(7,1);
for i = 1:size(fnames) % iterate through image stack
    im = rgb2hsv(imread(strcat(mdir,fnames(i).name)));
    im = im(:,:,1);            % only hue required
    vals = unique(im(:,:,1));  % list of hue values for each cell
    vals = vals(vals>0);       % don't want background in the list
    for v = transpose(vals)
        temp = im;             % make binary image
        temp(temp==v) = 1;
        temp(temp<1) = 0;
        bd = bwboundaries(temp); % extract boundary curve
        bd = cellfun(@(x) x*0.0689,bd,'un',0); % scaling from 1024x1024
        if fnames(i).name=='cells_0030_16a.tif'
            %figure;
            %hold on;
            %scatter(bd{1}(:,1), bd{1}(:,2));
            name = int2str(floor(100*v));
            csvwrite(strcat(mdir,'cell_boundary_',name,'.csv'), bd{1});
        end
        X = sgolayfilt(bd{1}(:,1),3,21);   % smooth the boundary curve
        Y = sgolayfilt(bd{1}(:,2),3,21);
        K = -LineCurvature2D([X,Y]);   % curvatures, FLIP SIGN !!!

        ind = find(abs(cells-v) < 0.001);  % which cell?
        if isempty(cell_curv{ind})
            cell_curv{ind} = {[K]}; % the first slice per image
            cell_pnts{ind} = {[X,Y]};
        else
            cell_curv{ind} = [cell_curv{ind}(:);{[K]}]; % subsequent slices
            cell_pnts{ind} = [cell_pnts{ind}(:);{[X,Y]}];
        end
        
        if fnames(i).name=='cells_0030_16a.tif'
            %scatter(X,Y);
            name = int2str(floor(100*v));
            csvwrite(strcat(mdir,'cell_boundary_smooth',name,'.csv'), {X,Y});
        end
        %fprintf('%d %d %4.4f %4.4f\n',size(bd{1}),v,std(K));
        %fprintf('%d %4.4f %4.4f\n',ind,v,std(K));
    end
end
for i = (1:7)
    [sz,loc] = max(cellfun('size',cell_curv{i},1)); % find largest slice loop
    c = cell_curv{i,1}{loc};               % curvature at each point      
    csvwrite(strcat(mdir,'cell',int2str(i),'_curv.csv'), c);
    p = cell_pnts{i,1}{loc};               % coordinates of each point
    %figure;
    %scatter(p(:,1),p(:,2));
    csvwrite(strcat(mdir,'cell',int2str(i),'_pnts.csv'), p);
    l = zeros(size(c));                    % distance between points
    for j = (1:size(l)-1) % from lower index point
        l(j) = sqrt((p(j+1,1)-p(j,1))^2 + (p(j+1,2)-p(j,2))^2);
    end
    w = zeros(size(c));                    % length allocated to each point
    for j = (2:size(w)-1) % skip first and last points
        w(j) = 0.5*(l(j-1)+l(j));
    end
    csvwrite(strcat(mdir,'cell',int2str(i),'_wght.csv'), w);
    fprintf('%4.4f\n',sqrt(var(c(2:end-1),w(2:end-1)))); % weighted std
    figure;
    histogram(c,'Normalization','probability',...  % NOT WEIGHTED!
       'NumBins',20,'Binlimits',[-2,2]);
end

%**************************************************************************
%**************************************************************************
