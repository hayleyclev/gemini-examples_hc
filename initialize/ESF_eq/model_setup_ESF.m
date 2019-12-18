%% Set paths to other GEMINI repos
cwd = fileparts(mfilename('fullpath'));
gemini_root = [cwd, filesep, '../../../GEMINI'];
addpath([gemini_root, filesep, 'script_utils'])
addpath([gemini_root, filesep, 'setup/gridgen'])
addpath([gemini_root, filesep, '../GEMINI-scripts/setup/gridgen'])
addpath([gemini_root, filesep, 'setup'])
geminiscripts_root = [cwd, filesep, '../../../GEMINI-scripts'];
addpath([geminiscripts_root,filesep,'setup/gridgen']);


%% EQuatorial grid
dtheta=5.75;
dphi=10;
lp=128;
lq=256;
lphi=48;
altmin=80e3;
glat=12;
glon=360-76.9;     %Jicamarca
gridflag=1;
flagsource=0;
iscurv=true;


%% MATLAB GRID GENERATION
xg=makegrid_tilteddipole_3D(dtheta,dphi,lp,lq,lphi,altmin,glat,glon,gridflag);
%xg=makegrid_tilteddipole_varx2_3D(dtheta,dphi,lp,lq,lphi,altmin,glat,glon,gridflag);
%xg=makegrid_tilteddipole_varx2_oneside_3D(dtheta,dphi,lp,lq,lphi,altmin,glat,glon,gridflag);


%% GEOGRAPHIC COORDINATES OF NEUTRAL SOURCE (OR GRID CENTER)
% % Iowa example
% neuinfo.sourcelat=38.9609;
% neuinfo.sourcelong=360-94.088;
% neuinfo.neugridtype=3;    %1 = Cartesian neutral grid (2D), 2 - axisymmetric (2D), 3 - 3D Cartesian
% neuinfo.zmin=0;
% neuinfo.zmax=375;
% neuinfo.xmin=-1200;
% neuinfo.xmax=1200;
% neuinfo.ymin=-1200;
% neuinfo.ymax=1200;
% neuinfo.rhomax=[];        %meaningless in 3D situations


%% FOR USERS INFO CONVERT SOURCE LOCATION TO GEOMAG for input file
% [sourcetheta,sourcephi]=geog2geomag(neuinfo.sourcelat,neuinfo.sourcelong);
% sourcemlat=90-sourcetheta*180/pi;
% sourcemlon=sourcephi*180/pi;

neuinfo=[];


%% PLot the grid
ha=plotgrid(xg,flagsource,neuinfo);


%% GENERATE SOME INITIAL CONDITIONS FOR A PARTICULAR EVENT - the iowa event
%in this case
UT=5.25;
dmy=[06,08,2016];
activ=[150,150,4];    %apparently this used the MSIS matlab defaults


%% USE OLD CODE FROM MATLAB MODEL
nmf=5e11;
nme=2e11;
[ns,Ts,vsx1]=eqICs3D(xg,UT,dmy,activ,nmf,nme);    %note that this actually calls msis_matlab - should be rewritten to include the neutral module form the fortran code!!!


%% WRITE THE GRID AND INITIAL CONDITIONS
outdir = [gemini_root, filesep, '../simulations/input/ESF_eq/'];
simlabel='ESF_eq';
writegrid(xg,outdir);
time=UT*3600;   %doesn't matter for input files
writedata(dmy,time,ns,vsx1,Ts,outdir,simlabel);
