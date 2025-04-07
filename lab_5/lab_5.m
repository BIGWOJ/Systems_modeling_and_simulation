clc;
close all;
clear all;

function [x, y] = generate_spring(L, r, theta, x1, y1)
    spring_length = L + r;    
    theta = -(theta) - pi/2; 
    amp = 0.1; % szerokosc sprezyny
    coil_number = 30; % gestosc
    
    
    x_spring = 0: 0.01 : (spring_length - 0.2); % 0.2 na zaczepienie
    x_coils = linspace(0, pi * coil_number, length(x_spring)); 
    % zmapowanie y dla sinusoidy na wsp. na linie wahadla
    coords = [x_spring, spring_length; sin(x_coils) * amp, 0];
    
    R = [cos(theta) -sin(theta); sin(theta) cos(theta)]; 
    rotcoord = R*coords;

    x = x1 + rotcoord(1, :);
    y = y1 + rotcoord(2, :);
end

out = sim("lab_5_simulink.slx");
L = out.l_output.Data;
r = out.r_output.Data;
theta = out.theta.Data;

x_min = inf;
x_max = -inf;
y_min = inf;
y_max = -inf;

for i = 1:length(r)
    [x, y] = generate_spring(L + r(i), r(i), theta(i), 0, 0);
    x_min = min(x_min, min(x));
    x_max = max(x_max, max(x));
    y_min = min(y_min, min(y));
    y_max = max(y_max, max(y));
end

figure
hold on
axis([x_min-1, x_max+1, y_min-1, y_max+1]);
axis manual;

for i = 1:length(theta)
    %cla czyści zawartość wykresu pozostawiając takie same osie,
    %clf czyści cały wykres, wraz z osiami
    cla;
    [x, y] = generate_spring(L + r(i), r(i), theta(i), 0, 0);
    plot(x, y);
    scatter(x(end), y(end), 100, 'filled')
    pause(0.01);
end