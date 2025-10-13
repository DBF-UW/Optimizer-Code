clc; clear; close all;

%% Parameters
straight_len = 1000; % 1000 ft in meters
R_turn = 7.65 * 3.28;                  % U-turn radius (m) -- increased for clarity
R_loop = 30;                  % loop radius (m)
N = 200;                      % resolution per curve

%% Straight 1 (along +x)
x1 = linspace(0, straight_len, N);
y1 = zeros(1,N);
z1 = zeros(1,N);

%% 180° Turn 1 (facing outward, bulges downward)
theta1 = linspace(-pi/2, pi/2, N);
x2 = straight_len + R_turn*cos(theta1);
y2 = -R_turn*sin(theta1) - R_turn;  % shifted down
z2 = zeros(1,N);

%% Half straight (heading back in -x)
half_straight = straight_len/2;
x3 = linspace(x2(end), x2(end)-half_straight, N);
y3 = ones(1,N)*y2(end);
z3 = zeros(1,N);

%% Loop (full 360 in XY, tangent to straight)
phi = linspace(0,2*pi,N);
x4 = x3(end) + R_loop*cos(phi);
y4 = y3(end) + R_loop*sin(phi);
z4 = zeros(1,N) + 20;

%% Half straight continuation (still heading -x)
x5 = linspace(x4(end), x4(end)-half_straight-30, N);
y5 = ones(1,N)*y4(end);
z5 = zeros(1,N);

%% 180° Turn 2 (facing outward opposite, bulges upward)
theta2 = linspace(1*pi/2, 1.5*pi, N);
x6 = x5(end) + R_turn*cos(theta2);
y6 = y5(end) - R_turn*sin(theta2) + R_turn; % shifted up
z6 = zeros(1,N);

%% Connect back to origin (Straight 2)
x7 = linspace(x6(end), 0, N);
y7 = zeros(1,N);
z7 = zeros(1,N);

% make a circle for the loop
x = R_turn*cos(phi) + straight_len/2
y = R_turn*sin(phi) - R_turn*3

%% Plot
set(gca, 'FontSize', 14)
figure; hold on; grid on; axis equal; ylim([-R_turn*4-5, 5+R_turn*4]); xlim([-1*R_turn, straight_len+R_turn])
plot3(x1,y1,z1, 'Color',[0.5 0 0.5], 'LineWidth',2) % Straight 1
plot3(x2,y2,z2,'k','LineWidth',2) % Turn 1
plot3(x3,y3,z3,'Color', [1 0.8823 0.326], 'LineWidth',2) % Half straight
% plot3(x4,y4,z4,'m','LineWidth',2) % Loop
plot3(x5,y5,z5,'Color', [1 0.8823 0.326], 'LineWidth',2) % Half straight
plot3(x6,y6,z6,'k','LineWidth',2) % Turn 2
plot3(x, y, z7, 'k', 'LineWidth',2); legend show;
% plot3(x7,y7,z7,'y','LineWidth',2) % Closing straight

xlabel('X (ft)', 'FontSize', 30); ylabel('Y (ft)', 'FontSize', 30); zlabel('Z (ft)');

title('AIAA Lap - Sectioned Constant Velocity Model', 'FontSize', 30);
set(gca, 'FontSize', 25)
legend('Velocity Straight 1', 'Velocity turn', 'Velocity Straight 2', 'FontSize', 23)
% set(gca, 'FontSize', 14)
% grid on; set(gca,'FontSize',12,'LineWidth',1.2);
legend show;
% view(2) % top-down
