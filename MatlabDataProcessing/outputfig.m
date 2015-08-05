function [] = outputfig( f, filename, reztime)
% OUTPUT A FIGURE

if nargin < 3
    reztime = 1;
end

figpos=getpixelposition(f); %dont need to change anything here
rez_screen=get(0,'ScreenPixelsPerInch'); %dont need to change anything here
rez_output=rez_screen*reztime; %resolution (dpi) of final graphic
set(f,'paperunits','inches','papersize',figpos(3:4)/rez_screen,'paperposition',[0 0 figpos(3:4)/rez_screen]); %dont need to change anything here
path='.\'; %the folder where you want to put the file
name=[filename '.tiff']; %what you want the file to be called
print(f,fullfile(path,name),'-dtiff',['-r',num2str(rez_output)],'-opengl') %save file 

end

