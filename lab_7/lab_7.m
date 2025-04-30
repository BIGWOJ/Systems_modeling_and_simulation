clc;
clear;
close all;

out = sim('lab_7_simulink');
phi_1 = out.phi_1;
phi_2 = out.phi_2;

l1 = str2num(get_param('lab_7_simulink/Subsystem', 'l1'));
l2 = str2num(get_param('lab_7_simulink/Subsystem', 'l2'));
m1 = str2num(get_param('lab_7_simulink/Subsystem', 'm1'));
m2 = str2num(get_param('lab_7_simulink/Subsystem', 'm2'));

x_1 = -l1 * sin(phi_1);
y_1 = -l1 * cos(phi_1);
x_2 = x_1 - l2 * sin(phi_2);
y_2 = y_1 - l2 * cos(phi_2);

figure;
hold on;
axis([min(x_2)*1.5, max(x_2)*1.5, min(y_2)*1.5, max(y_2)*1.5]);

rope_1 = plot(NaN, NaN, 'r', LineWidth=2);
rope_2 = plot(NaN, NaN, 'r', LineWidth=2);

mass_1 = plot(NaN, NaN, 'b.', MarkerSize=30*m1);
mass_2 = plot(NaN, NaN, 'b.', MarkerSize=30*m2);

for i = 1:length(phi_1)
    set(rope_1, 'XData', [0, x_1(i)], 'YData', [0, y_1(i)]);
    set(rope_2, 'XData', [x_1(i), x_2(i)], 'YData', [y_1(i), y_2(i)]);
    set(mass_1, 'XData', x_1(i), 'YData', y_1(i));
    set(mass_2, 'XData', x_2(i), 'YData', y_2(i));
    pause(0.02); 
end