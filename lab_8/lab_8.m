clc;
clear;
close all;

out = sim('lab_8_simulink');

x = out.x.Data;
y = out.y.Data;
m = str2num(get_param('lab_8_simulink/Subsystem', 'm'));
l = str2num(get_param('lab_8_simulink/Subsystem', 'l'));
xi = str2num(get_param('lab_8_simulink/Subsystem', 'xi'));
yi = str2num(get_param('lab_8_simulink/Subsystem', 'yi'));
di = str2num(get_param('lab_8_simulink/Subsystem', 'di'));

a = sqrt(x.^2 + y.^2);
b = sqrt(l^2 - a.^2);
z = l - b;

figure;
hold on;
view(3);
axis equal;
axis([min(xi)*3, max(xi)*3, min(yi)*3, max(yi)*3, min(z)*1.5, l*1.5]);

plot3(xi, yi, di, 'b.', MarkerSize=20);
ball = plot3(NaN, NaN, NaN, 'r.', MarkerSize=20*m);
line = plot3(NaN, NaN, NaN, 'k', LineWidth=2);
for i = 1:length(x)
    set(ball, 'XData', x(i), 'YData', y(i), 'ZData', z(i))
    set(line, 'XData', [0 x(i)], 'YData', [0 y(i)], 'ZData', [l z(i)])
    pause(0.01);
end

hold off;