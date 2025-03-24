clc
close all
clear all

out = sim("lab_3_3.slx");
x = out.x;

L = str2double(get_param('lab_3_3/Subsystem', 'l'))
m = str2double(get_param('lab_3_3/Subsystem', 'm'))

FigureName = 'Wizualizacja wahadla';
Fig = figure('Name', FigureName);

for i=1:length(x)
    fi0 = x(i);
    %rysowanie linki
    p = plot([0 -L*sin(fi0)],[0 -L*cos(fi0)],'Color','r','LineWidth',2);
    hold on
    %rysowanie kulki
    s = plot(-L*sin(fi0), -L*cos(fi0), 'b.','MarkerSize',5*m);
    hold off
    %ustawianie zakresu osi
    axis([-1.1*L 1.1*L -1.1*L 1.1*L])
    %hold on, hold off
    pause(0.01)
end


