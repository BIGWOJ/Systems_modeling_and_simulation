clc;
close all;
clear all;

out = sim("lab_6_simulink.slx");
r = out.r.Data;
theta = out.theta.Data;
m1 = str2num(get_param("lab_6_simulink/Subsystem", 'm1'));
m2 = str2num(get_param("lab_6_simulink/Subsystem", 'm2'));
R = str2num(get_param("lab_6_simulink/Subsystem", 'R'));

x = -r .* sin(theta);
y = -r .* cos(theta);

min_y = -(r(1) + max(r)) - 1;
figure;
hold on;
axis([-2, 2, min_y, 1]);
axis manual;

plot([-1, 0], [0, 0], LineWidth=3, Color='r')
plot(0, 0, 'b.', 'MarkerSize', 50000*R);
plot(-1, 0, 'b.', 'MarkerSize', 50000*R);

square_size = 0.25 * m2;
weight_square = rectangle('Position', [0, 0, square_size, square_size], FaceColor='b');
pendulum = plot(NaN, NaN, 'b.', 'MarkerSize', 75 * m1);
line_handle_pendulum = plot([-1, -1], [0, 0], 'r', LineWidth=2);
line_handle_weight = plot([-1, -1], [0, 0], 'r', LineWidth=2);

for i = 1:length(theta)
    set(pendulum, 'XData', -x(i), 'YData', y(i));
    set(line_handle_pendulum, 'XData', [0, -x(i)], 'YData', [0, y(i)])
    line_position = -(r(1) + r(i));
    set(line_handle_weight, 'XData', [-1, -1], 'YData', [0, line_position]);
    set(weight_square, 'Position', [-1.1, line_position-square_size, square_size, square_size]);
    pause(0.01);
end
