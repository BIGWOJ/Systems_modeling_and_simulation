h1 = str2num(get_param('zbiorniki_lin/Subsystem', 'h1'));
h2 = str2num(get_param('zbiorniki_lin/Subsystem', 'h2'));
Qwe = str2num(get_param('zbiorniki_lin/Subsystem', 'Qwe'));
h_matrix = [24; 12];
model = 'zbiorniki_lin'
[A, B, C, D] = linmod(model, h_matrix, Qwe)
