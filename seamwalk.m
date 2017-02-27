%
% seam - array of vertices for one seam 
% iv   - index of current seam vertex
% r    - index of next seam edge
% iVhv - indices of seam end-points
% Ehit - flags to mark seam edge already hit
% Evh  - all of the seam edges
%
function [seam, Ehit] = seamwalk(seam,iv,r,iVhv,Ehit,Ehv)
edge = Ehv(r,:); % note: this edge already flagged as hit
if edge(1)==iv % get the other end of the edge
    iv = edge(2);
else
    iv = edge(1);
end
seam = [seam iv]; % add vertex to the seam
if any(iVhv==iv) % at end-point?
    return;
end 
[r, c] = find(Ehv==iv & ~ismember(Ehv,edge,'rows')); % find the next edge
Ehit(r) = 1; % flag edge as hit
[seam, Ehit] = seamwalk(seam,iv,r,iVhv,Ehit,Ehv); % keep walking!


