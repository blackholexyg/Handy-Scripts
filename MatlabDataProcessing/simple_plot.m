%% Data

xdata = linspace(0,1,20)+rand(1,20)*0.1;
ydata = linspace(0,2,20)+rand(1,20)*0.1;

%% Linear Fitting

p = polyfit(xdata,ydata,1);
xfit = linspace(min(xdata),max(xdata),100);  
yfit = polyval(p,xfit);

%% Plot

f = figure;
hold on;
box on;

%%%%% Set font for current axis
% set(gca,'FontName','Arial');
set(gca,'FontSize',18)

%%%%% Plot data
plot(xdata,ydata,'b*','MarkerSize',10);
plot(xfit,yfit,'r--','LineWidth',2);

% Line Style Specifiers
% '-', Solid line (default)
% '--', Dashed line
% ':', Dotted line
% '-.', Dash-dot line

% Color Specifiers
% [1 1 0],y,yellow
% [1 0 1],m,magenta
% [0 1 1],c,cyan
% [1 0 0],r,red
% [0 1 0],g,green
% [0 0 1],b,blue
% [1 1 1],w,white
% [0 0 0],k,black

% Marker Specifiers
% '+', Plus sign
% 'o', Circle
% '*', Asterisk
% '.', Point
% 'x', Cross
% 'square' or 's', Square
% 'diamond' or 'd', Diamond
% '^', Upward-pointing triangle
% 'v', Downward-pointing triangle
% '>', Right-pointing triangle
% '<', Left-pointing triangle
% 'pentagram' or 'p', Five-pointed star (pentagram)
% 'hexagram' or 'h', Six-pointed star (hexagram)

% Related Properties
% LineWidth — Specifies the width (in points) of the line.
% MarkerEdgeColor — Specifies the color of the marker or the edge color for filled markers (circle, square, diamond, pentagram, hexagram, and the four triangles).
% MarkerFaceColor — Specifies the color of the face of filled markers.
% MarkerSize — Specifies the size of the marker in points (must be greater than 0).

%%%%% Plot Range
xlim([0,1])
ylim([0,2])

%%%%% Ticks
% set(gca, 'XTick', [0.3,0.7])
% set(gca, 'YTick', [])

%%%%% Labels and Titles
xlabel('X Data')
ylabel('Y Data')
title('Title')

%%%%% Figure Size
width = 5.0;
height = 4.0;
set(gcf,'Units','inches');
set(gcf,'Position',[0,0,width,height]);

%%%%% Paper Setting & Print

% Tiff format
set(gcf,'PaperUnits','inches');
set(gcf,'PaperPositionMode', 'auto');
print(gcf,'figure_name.tiff','-dtiff','-r192')

% Pdf version
letter_width = 8.5;
letter_height = 11.0;
A4_width = 8.3;
A4_height = 11.7;
set(gcf,'PaperUnits','inches');
set(gcf,'PaperSize',[letter_width,letter_height]);
print(gcf,'figure_name.pdf','-dpdf','-painters')