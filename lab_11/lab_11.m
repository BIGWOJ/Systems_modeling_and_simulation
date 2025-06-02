clc;
clear all;
close all;

%Zadanie 1
load('data2.mat');

%x'' = a11 *x' + a12 *y' + a13*x + a14 *y
%y'' = a21 *x' + a22 *y' + a23*x + a24 *y

%          x''         y''
X = [data2(:,1) data2(:,2)]';

%           a1*x'     a2*y'      a3*x          a4*y
Z = [data2(:,3), data2(:,4), data2(:,5), data2(:,6)]';

Rs = X*Z';
Ps = Z*Z';
A1 = Rs*Ps ^-1; %A1 = [a11 a12 a13 a14; a21 a22 a23 a24];

%Testowanie modelu
load('data1.mat');

%x'' = a11       *x'      + a12         *y' +     a13    * x     +    a14     *y
x2 = A1(1,1) * data1(:,3) + A1(1,2)*data1(:,4) + A1(1,3)*data1(:,5) + A1(1,4) * data1(:,6);
%y'' = a21 *x' + a22 *y' + a23*x + a24 *y
y2 = A1(2,1) * data1(:,3) + A1(2,2)*data1(:,4) + A1(2,3)*data1(:,5) + A1(2,4) * data1(:,6);

mse_x = mean((x2 - data1(:,1)) .^2);
mse_y = mean((y2 - data1(:,2)) .^2);
mse1 = (mse_x + mse_y) / 2;



%Zadanie 2

%           a1*x'     a2*y'      a3*x          a4*y      a5x'y'

Z = [data2(:,3).^2, data2(:,4).^2, data2(:,5), data2(:,6), data2(:,3) .* data2(:,4)]';
Rs = X*Z';
Ps = Z*Z';
A2 = Rs*Ps ^-1;

x3 = A2(1,1) * data1(:,3).^2 + A2(1,2)*data1(:,4).^2 + A2(1,3)*data1(:,5) + A2(1,4) * data1(:,6) + A2(1,5) * data1(:,3) .* data1(:,4);
y3 = A2(2,1) * data1(:,3).^2 + A2(2,2)*data1(:,4).^2 + A2(2,3)*data1(:,5) + A2(2,4) * data1(:,6) + A2(2,5) * data1(:,3) .* data1(:,4);

Rs = X*Z';
Ps = Z*Z';
A2 = Rs*Ps ^-1;

mse_x = mean((x3 - data1(:,1)) .^2);
mse_y = mean((y3 - data1(:,2)) .^2);
mse_2 = (mse_x + mse_y) / 2




%Zadanie 3

h = 2^-8;
t = 500;

%Warunki początkowe
x0(1) = data1(1,5);
y0(1) = data1(1,6);
x1(1) = data1(1,3);
y1(1) = data1(1,4);

x2(1) = A1(1,1) * x1(end) + A1(1,2)*y1(end) + A1(1,3)*x0(end) + A1(1,4) * y0(end);
y2(1) = A1(2,1) * x1(end) + A1(2,2)*y1(end) + A1(2,3)*x0(end) + A1(2,4) * y0(end);

for i = h:h:t
    x0(end+1) = x0(end) + h*x1(end);
    y0(end+1) = y0(end) + h*y1(end);

    x1(end+1) = x1(end) + h*x2(end);
    y1(end+1) = y1(end) + h*y2(end);

    x2(end+1) = A1(1,1) * x1(end) + A1(1,2)*y1(end) + A1(1,3)*x0(end) + A1(1,4) * y0(end);
    y2(end+1) = A1(2,1) * x1(end) + A1(2,2)*y1(end) + A1(2,3)*x0(end) + A1(2,4) * y0(end);
end

figure;
hold on;

plot(data1(:,5), data1(:,6), 'r.')
plot(x0, y0, 'g--')
