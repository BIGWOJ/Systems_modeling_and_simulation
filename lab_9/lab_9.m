clc;
clear;
close all;

out = sim('lab_9_simulink');

h1 = out.h1.Data;
h2 = out.h2.Data;
S1 = str2num(get_param('lab_9_simulink/Subsystem', 'S1'));
S2 = str2num(get_param('lab_9_simulink/Subsystem', 'S2'));
Swy1 = str2num(get_param('lab_9_simulink/Subsystem', 'Swy1'));
Swy2 = str2num(get_param('lab_9_simulink/Subsystem', 'Swy2'));

h1_max = max(h1) + 1;
h2_max = max(h2) + 1;

figure;
hold on;

plot([0 S1+S2+2], [0 0], 'k');
plot([0 0], [0 h1_max], 'k');
plot([S1 S1], [Swy1 h1_max], 'k');
plot([S1+1 S1+1], [Swy1 h2_max], 'k');
plot([S1+S2+1 S1+S2+1], [Swy1 h2_max], 'k');
plot([S1 S1+1], [Swy1 Swy1], 'k');
plot([S1+S2+1 S1+S2+2], [Swy2 Swy2], 'k');

RGB_color = [100/255, 200/255, 255/255];
container_1 = fill([0 S1 S1 0], [0 0 0 0], RGB_color, 'EdgeColor', 'None');
valve_1 = fill([S1 S1+1 S1+1 S1], [0 0 Swy1 Swy1], RGB_color, 'EdgeColor', 'None');
container_2 = fill([S1+1 S1+S2+1 S1+S2+1 S1+1], [0 0 0 0], RGB_color, 'EdgeColor', 'None');
valve_2 = fill([S1+S2+1 S1+S2+2 S1+S2+2 S1+S2+1], [0 0 Swy2 Swy2], RGB_color, 'EdgeColor', 'None');

axis([-1, S1+S2+3, -1, max(h1_max, h2_max)+1]);
grid on;
hold off;

for i = 1:length(h1)
    container_1.XData = [0 S1 S1 0];
    container_1.YData = [0 0 h1(i) h1(i)];
    
    valve1_height = min(h1(i), Swy1);
    valve_1.YData = [0 0 valve1_height valve1_height];
    
    container_2.XData = [S1+1 S1+S2+1 S1+S2+1 S1+1];
    container_2.YData = [0 0 h2(i) h2(i)];

    valve2_height = min(h2(i), Swy2);
    valve_2.YData = [0 0 valve2_height valve2_height];
    
    pause(0.02);
end