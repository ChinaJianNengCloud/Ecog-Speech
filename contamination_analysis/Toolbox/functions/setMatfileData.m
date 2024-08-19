function setMatfileData(mat_file, var_name, data, varargin)

% setMatfileData(mat_file, var_name, data, varargin)
%
% Access data in MatFiles with any index range.
%
% The built-in MATLAB function only allows to access MatFiles data with
% indexes increasing in equally spaced intervals. When it is not the case,
% this function first loads the data corresponding to all consecutive
% indexes within the range and then returns only the required data.
%
% Copyright 2020 INSERM
% Licence: GPL-3.0-or-later
% Author(s): Philémon Roussel

vararg_nb = length(varargin);

if ~isa(mat_file, 'matlab.io.MatFile')
    mat_file = matfile(mat_file, 'Writable', true);
end

is_equally_spaced = true;

S_load(1).type = '.';
S_load(1).subs = var_name;
S_load(2).type = '()';
S_final.type = '()';

if vararg_nb == 1
    if iscell(varargin{1})
        idxs_cellarray = varargin{1};
    end
    
elseif vararg_nb == 0
    setMatfileVar(mat_file, var_name, data)
    return
    
else
    idxs_cellarray = varargin;
end

dim_nb = length(idxs_cellarray);

for d = 1:dim_nb
    
    idx_vals = idxs_cellarray{d};
    if islogical(idx_vals)
        idx_vals = find(idx_vals);
    end
    load_idx_vals = idx_vals;
    
    if isnumeric(idx_vals)
        
        % check if the indexes are equally spaced (taken from MatFile.m)
        max_idx = max(idx_vals);
        min_idx = min(idx_vals);
        
        if numel(idx_vals)>1
            % the difference between the first elements is the stride
            stride = idx_vals(2) - idx_vals(1);
        else
            stride = 1;
        end
        
        if ~isequal(idx_vals(:)', min_idx:stride:max_idx)
            is_equally_spaced = false;
            
            % all consecutive indexes within the range will be loaded
            load_idx_vals = min_idx:max_idx;
            final_idx_vals = find(ismember(load_idx_vals, idx_vals));
        else
            final_idx_vals = ':';
        end
        
    elseif strcmp(idx_vals, ':')
        final_idx_vals = idx_vals;
    else
        error('(getMatfileData) Error: Unknown input argument.' )
    end
    
    S_load(2).subs{d} = load_idx_vals;
    S_final.subs{d} = final_idx_vals;
    
end

if is_equally_spaced
    mat_file = subsasgn(mat_file, S_load, data);
else
    matfile_data = subsref(mat_file, S_load);
    data = subsasgn(matfile_data, S_final, data);
    mat_file = subsasgn(mat_file, S_load, data);
end

end

