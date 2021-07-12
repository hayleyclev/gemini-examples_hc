run ~/Projects/mat_gemini-scripts/setup.m;

%MOORE, OK GRID (FULL)
p.dtheta=20;
p.dphi=10;
p.lp=350;
%lq=384;
p.lq=256;
%lphi=192;
p.lphi=96;
p.altmin=80e3;
p.glat=39;
p.glon=262.51;
p.gridflag=0;


%MATLAB GRID GENERATION

if ~exist('xg', 'var')
  % xg = gemini3d.grid.tilted_dipole(p);
  %xg= gemini3d.grid.makegrid_tilteddipole_varx2_3D(p);
  xg=gemscr.grid.makegrid_tilteddipole_varx2_3D(p.dtheta,p.dphi,p.lp,p.lq,p.lphi,p.altmin,p.glat,p.glon,p.gridflag);
end

p=gemini3d.read.config("./config.nml");    % eq2dist needs a populated config struct.
p.eq_dir='~/simulations/raid/Perkins_eq/';
lx1=xg.lx(1); lx2=xg.lx(2); lx3=xg.lx(3);


%INTERPOLATE ONTO THE NEW GRID
dat = gemini3d.model.eq2dist(p, xg);
lsp=size(dat.ns,4);


%FORCE A LONGITUDINAL CONSTANCY TO THE PARAMETERS (SINCE USING PERIODIC DOMAIN)
nsislice=dat.ns(:,:,floor(xg.lx(3)/2),:);
Tsislice=dat.Ts(:,:,floor(xg.lx(3)/2),:);
vs1islice=dat.vs1(:,:,floor(xg.lx(3)/2),:);
for ix3=1:xg.lx(3)
  nsi(:,:,ix3,:)=nsislice;
  Tsi(:,:,ix3,:)=Tsislice;
  vs1i(:,:,ix3,:)=vs1islice;
end


%%NOW ADD SOME NOISE TO SEED PERKINS INSTABILITY, ADD DIFFERENT NOISE AT EACH POINT
%nsi=nsi+0.1*nsi.*randn(size(nsi));
%nsi=max(nsi,1e8);

%%NOISE; ADD AS AN ADJUSTMENT TO DENSITY PROFILE

%{
  for ix3=1:lx3
    for ix2=5:lx2
      noise=randn(1);
      for isp=1:lsp
        nsi(:,ix2,ix3,isp)=nsi(:,ix2,ix3,isp)+0.001*nsi(:,ix2,ix3,isp).*noise;
      end
    end
  end
%}
nsi=max(nsi,1e7);
nsi(:,:,:,7)=sum(nsi(:,:,:,1:6),4);

dint = struct("ns", nsi, "Ts", Tsi, "vs1", vs1i, "time", dat.time);

%WRITE OUT THE RESULTS TO A NEW FILE
p.outdir= '~/simulations/raid/Perkins';

gemini3d.write.grid(p,xg)
gemini3d.write.state(p.outdir, dint)
system(['cp config.nml ',p.outdir,'/inputs/']);