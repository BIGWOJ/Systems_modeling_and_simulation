fig = figure('NumberTitle', 'off', 'Position', [800 250 900 1000]);

controls_div = uipanel(fig, 'Position', [0.02 0.02 0.95 0.3]);

uicontrol(controls_div, 'Style', 'text', 'String', 'Grawitacja (g):', 'Position', [10 250 100 20]);
grav_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '9.81', 'Position', [120 250 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'Tłumienie (k):', 'Position', [10 200 100 20]);
damp_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '1', 'Position', [120 200 100 20], 'Callback', @run_simulation);


uicontrol(controls_div, 'Style', 'text', 'String', 'Długość (l):', 'Position', [310 250 100 20]);
l_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '4', 'Position', [420 250 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'Masa kulki (m):', 'Position', [310 200 100 20]);
m_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '2', 'Position', [420 200 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'x startowe (x):', 'Position', [310 150 100 20]);
x_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '-1', 'Position', [420 150 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'y startowe (y):', 'Position', [310 100 100 20]);
y_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '-1', 'Position', [420 100 100 20], 'Callback', @run_simulation);


uicontrol(controls_div, 'Style', 'text', 'String', 'X magnesów (xi):', 'Position', [610 250 100 20]);
xi_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '[-1 1 1]', 'Position', [720 250 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'Y magnesów (yi):', 'Position', [610 200 100 20]);
yi_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '[1 1 -1]', 'Position', [720 200 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'Odległość od XY (di):', 'Position', [600 150 120 20]);
di_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '[0.1 0.1 0.1]', 'Position', [720 150 100 20], 'Callback', @run_simulation);

uicontrol(controls_div, 'Style', 'text', 'String', 'Siła magnesów (ai):', 'Position', [610 100 100 20]);
ai_edit = uicontrol(controls_div, 'Style', 'edit', 'String', '[1 -1 1.5]', 'Position', [720 100 100 20], 'Callback', @run_simulation);


simulation_button = uicontrol(controls_div, 'Style', 'pushbutton', 'String', 'Start', 'Position', [350 20 200 30], 'Callback', @run_simulation);

ax_2d = axes('Parent', fig, 'Position', [0.02 0.35 0.45 0.5]);
grid(ax_2d, 'on');
title(ax_2d, '2D');

ax_3d = axes('Parent', fig, 'Position', [0.5 0.35 0.45 0.5]);
view(ax_3d, 3);
grid(ax_3d, 'on');
title(ax_3d, '3D');

Data_struct = struct(...
    'fig', fig,...
    'ax_3d', ax_3d,...
    'ax_2d', ax_2d,...
    'grav_edit', grav_edit,...
    'damp_edit', damp_edit,...
    'l_edit', l_edit,...
    'm_edit', m_edit,...
    'x_edit', x_edit,...
    'y_edit', y_edit,...
    'xi_edit', xi_edit,...
    'yi_edit', yi_edit,...
    'di_edit', di_edit,...
    'ai_edit', ai_edit);
guidata(fig, Data_struct);

run_simulation();


function run_simulation(~, ~)
    figure_data = guidata(gcf);
    fig = figure_data.fig;
    Data_struct = guidata(fig);
    
    g = str2double(get(Data_struct.grav_edit, 'String'));
    k = str2double(get(Data_struct.damp_edit, 'String'));
    l = str2double(get(Data_struct.l_edit, 'String'));
    m = str2double(get(Data_struct.m_edit, 'String'));
    x = str2double(get(Data_struct.x_edit, 'String'));
    y = str2double(get(Data_struct.y_edit, 'String'));
    
    xi_str = get(Data_struct.xi_edit, 'String');
    yi_str = get(Data_struct.yi_edit, 'String');
    di_str = get(Data_struct.di_edit, 'String');
    ai_str = get(Data_struct.ai_edit, 'String');

    xi = str2num(xi_str);
    yi = str2num(yi_str);
    di = str2num(di_str);
    ai = str2num(ai_str);

    set_param('GUI_simulink/Subsystem', 'g', num2str(g));
    set_param('GUI_simulink/Subsystem', 'k', num2str(k));
    set_param('GUI_simulink/Subsystem', 'l', num2str(l));
    set_param('GUI_simulink/Subsystem', 'm', num2str(m));
    set_param('GUI_simulink/Subsystem', 'x', num2str(x));
    set_param('GUI_simulink/Subsystem', 'y', num2str(y));

    set_param('GUI_simulink/Subsystem', 'xi', mat2str(xi));
    set_param('GUI_simulink/Subsystem', 'yi', mat2str(yi));
    set_param('GUI_simulink/Subsystem', 'di', mat2str(di));
    set_param('GUI_simulink/Subsystem', 'ai', mat2str(ai));

    out = sim('GUI_simulink');

    x = out.x.Data;
    y = out.y.Data;

    a = sqrt(x.^2 + y.^2);
    b = sqrt(l^2 - a.^2);
    z = l - b;

    cla(Data_struct.ax_3d);
    cla(Data_struct.ax_2d);

    hold(Data_struct.ax_2d, 'on');
    hold(Data_struct.ax_3d, 'on');

    grid(Data_struct.ax_2d, 'on');
    grid(Data_struct.ax_3d, 'on');

    view(Data_struct.ax_3d, 3);

    x_ranges = [min(min(x)-1, min(xi)-1), max(max(x)+1, max(xi)+1)];
    y_ranges = [min(min(y)-1, min(yi)-1), max(max(y)+1, max(yi)+1)];
   
    axis(Data_struct.ax_2d, [x_ranges(1), x_ranges(2), y_ranges(1), y_ranges(2)]);
    axis(Data_struct.ax_3d, [x_ranges(1), x_ranges(2), y_ranges(1), y_ranges(2), min(z), l+1]);
    
    plot3(Data_struct.ax_3d, xi, yi, di, 'b.', 'MarkerSize', 20);
    plot(Data_struct.ax_2d, xi, yi, 'b.', 'MarkerSize', 20);

    ball3d = plot3(Data_struct.ax_3d, NaN, NaN, NaN, 'r.', 'MarkerSize', 20*m);
    line3d = plot3(Data_struct.ax_3d, NaN, NaN, NaN, 'k', 'LineWidth', 2);

    trajectory_x = [];
    trajectory_y = [];

    for i = 1:length(x)
        set(ball3d, 'XData', x(i), 'YData', y(i), 'ZData', z(i))
        set(line3d, 'XData', [0 x(i)], 'YData', [0 y(i)], 'ZData', [l z(i)])

        trajectory_x = [trajectory_x, x(i)];
        trajectory_y = [trajectory_y, y(i)];
        plot(Data_struct.ax_2d, trajectory_x, trajectory_y, 'k');
        
        pause(0.01);
    end
end
