clc %Czyszczenie konsoli
close all %Zamykanie wszystkich okienek
clear all %Czyszczenie wszystkich zmiennych

%Zadanie 1

%1
f1 = @(x) sin(x) + cos(x);

f1(7)
%f1([5,4,3,2,1])

%2
f2 = @(x) exp(x) + log(x);

%3
%operacje tablicowe = mnożenie z kropką
%operacje macierzowe = mnożenie bez kropki
f3 = @(x,y) sin(x) .* cos(y);

%Zadanie 2

%Krok 0.05
x = 0.1:0.05:4;
figure %Wyświetlenie pustego okienka wykresowego
%hold on, żeby parę wykresów na jednym dać
hold on
plot(x, f1(x), 'red', LineWidth=2)
plot(x, f2(x), 'blue')
legend('sin(x)+cos(x)', 'e^x+log(x)')
title('Wykresy')
xlabel('Oś x')
ylabel('Oś y')
grid on

%Zadanie 3

x = linspace(-2*pi, 2*pi, 100);
y = x;

%Przypisanie dwóch zmiennych
[X, Y] = meshgrid(x, y);

figure
hold on
mesh(X, Y, f3(X, Y))

%Rysowanie punktów
plot3(2*pi, -2*pi, 0, 'ro')
%Wyjściowy kąt obrotu 
view(-30, 30)

%Zadanie 4

%7 punktów
%rand(1, ilość_punktów)*(max-min)+min
x = rand(1,7)*(5-2)+2;
y = rand(1,7)*4+3;

function zadanie_4(a,b)
    figure
    hold on
    plot(a, b, 'rs', markersize=15)
    plot(a,b, 'k--', LineWidth=3)
end

zadanie_4(x, y)