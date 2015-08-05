%% Get Data

xdata = linspace(0,1,20);
ydata = linspace(0,2,20);

%% Linear Fitting

p=polyfit(xdata,ydata,1);  

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
plot( xdata, ydata, 'b*', 'LineWidth', 2, 'MarkerSize',10);
plot( xfit, yfit, 'r-', 'LineWidth', 2);
% plot( xdata(1:20:end), ydata(1:20:end), 'ro', 'MarkerSize', 8,'LineWidth', 2);

%%%%% Plot Range
% ylim([0,1])

%%%%% Labels and Titles
xlabel('Cell Mass')
ylabel('Frequency')
%title('This is a Title')

%%%%% Paper setting
set(gcf,'units','pixel');
set(gcf,'position',[0,0,600,450]*1.2);

%%%%% Output to Tiff
% function [] = outputfig( f, filename, reztime)
outputfig(gcf,'5th_order',2)