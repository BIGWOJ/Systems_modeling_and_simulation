clc
close all
clear all

out = sim("lab_4_simulink.slx");
x = out.x_output.Data;
y = out.y_output.Data;

figure
hold on
xlim([-10,10]);
ylim([-10,10]);
rectangle('Position', [-5 -5 10 10], 'Curvature', [1 1]);
plot(x, y, 'b');

for i=1:length(x)
    satelitte = plot(x(i), y(i), 'ko');
    pause(0.01)
    delete(satelitte)
end

