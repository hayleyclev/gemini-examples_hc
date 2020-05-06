% test a few setups
% for now, just tests that it doesn't error when run

this = fileparts(mfilename('fullpath'));
run([this, '/../setup.m'])

R = [this, '/../initialize'];

%% lint
if exist('checkcode_recursive', 'file')
  checkcode_recursive([this, '/../'])
else
  disp('SKIP: lint check')
end

%% test2d_eq
model_setup([R, '/test2d_eq'])
%% test2d_fang
try
  model_setup([R, '/test2d_fang'])
catch e
  if ~strcmp(e.identifier, 'readgrid:file_not_found')
    rethrow(e)
  end
end
%% test2d_glow
try
  model_setup([R, '/test2d_glow'])
catch e
  if ~strcmp(e.identifier, 'readgrid:file_not_found')
    rethrow(e)
  end
end
%% arcs_eq
model_setup([R, '/arcs_eq'])
%% arcs
try
  model_setup([R, '/arcs'])
catch e
  if ~strcmp(e.identifier, 'readgrid:file_not_found')
    rethrow(e)
  end
end
%% risr2d_eq
model_setup([R, '/risr2d_eq'])
%% risr3d_eq
model_setup([R, '/risr3d_eq'])
