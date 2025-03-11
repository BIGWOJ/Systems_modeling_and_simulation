clc
close all
clear all
%Zadanie 1
x = -3:0.5:3;
y = [-0.25, -0.5, -0.75, -0.5, 0.25, 0, 0.25, 0.5, 0.25, 0, -0.15, -0.5, -0.25];
%figure
%plot(x, y, "*")

%Zadanie 2
Xp = -1.25;
Yp = 0;

y1 = interp1(x, y, Xp, "nearest");
nearest_error = abs(Yp - y1)

y1 = interp1(x, y, Xp, "linear");
linear_error = abs(Yp - y1)

y1 = interp1(x, y, Xp, "spline");
spline_error = abs(Yp - y1)

y1 = interp1(x, y, Xp, "cubic");
cubic_error = abs(Yp - y1)
%Najlepszą metodą okazała się spline - najmniejszy błąd

%Zadanie 3
xx = linspace(-3, 3, 100);
y1 = interp1(x, y, xx, "nearest");
figure
plot(x, y, "k*")

hold on
plot(xx, y1, "r")

y1 = interp1(x, y, xx, "linear");
plot(xx, y1, "b")

y1 = interp1(x, y, xx, "spline");
plot(xx, y1, "g")

y1 = interp1(x, y, xx, "cubic");
plot(xx, y1, "c")
legend("punkty", "nearest", "linear", "spline", "cubic")
%Najlepszą metodą okazało się spline

%Zadanie 4
xx = linspace(-3, 3, 100);
figure

for i = 1: 12
    subplot(3, 4, i)
    hold on
    p = polyfit(x, y, i);
    yy = polyval(p, xx);
    plot(x, y, "k*")
    plot(xx, yy)
end
%Najlepszym stopniem wielomianu jest 10. stopień

%Zadanie 5
p = polyfit(x, y, 10);
yy = polyval(p, Xp);
y1 = interp1(x, y, Xp, "spline");
error = abs(yy - Yp)

%Błąd jest trochę większy niż spline = 0.1058