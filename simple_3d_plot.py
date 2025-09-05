import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    
import mission_sim
opti = asb.Opti()
airfoil_name = "naca0012"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
M2lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True, banner=False)
M3lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=False, banner=True)
constraints.constraints(opti, mantaRay)
M2_score = mission_sim.M2(mantaRay, M2lapper) 
M3_score = mission_sim.M3(mantaRay, M3lapper)
GM_score = mission_sim.GM(mantaRay)

MAX_PASSENGERS = 81
opti.subject_to([mantaRay.passengers < MAX_PASSENGERS])
#find and save score for best GM airplane
opti.minimize(GM_score)  
solution1 = opti.solve(verbose=False)
GM_min_score = solution1.value(GM_score)
print("GM min score is:", GM_min_score)

#find and save score for best M2 airplane
opti.maximize(M2_score) 
solution2 = opti.solve(verbose=False)
M2_max_score = solution2.value(M2_score)
print("M2 max score is:", M2_max_score)

#find and save score for best M3 airplane
opti.maximize(M3_score) 
solution3 = opti.solve(verbose=False)
M3_max_score = solution3.value(M3_score)
print("M3 max score is:", M3_max_score)

#normalized score equation
score = GM_min_score/GM_score + (1+ M2_score/M2_max_score) + (2+M3_score/M3_max_score) + 1


def make3dData(variable_1, min_1, max_1, variable_2, min_2, max_2):
    x_vals = np.arange(min_1, max_1 + 1)
    y_vals = np.arange(min_2, max_2 + 2)
    sols = []

    for y in y_vals:
        row = []
        for x in x_vals:
            print("Trying: ", x, ",", y)
            opti.maximize(score - 400*(variable_1-x)**2 - 400*(variable_2-y)**2)

            try:
                sol = opti.solve(verbose=False)
            except RuntimeError as e:
                print("Solve Failed")
                sol = np.nan
            
            row.append(sol)
        sols.append(row)
    
    return (sols)


def make3dPlot(sols, display_variable, x_title, y_title, z_title):
    nrows = len(sols)
    ncolumns = len(sols[0])

    X, Y = np.meshgrid(range(ncolumns), range(nrows))
    Z = np.zeros((nrows, ncolumns))
    #Test = np.zeros((ncolumns, nrows))
    for i in range(nrows):
        for j in range(ncolumns):
            Z[i, j] = sols[i][j].value(display_variable)
            #Test[i, j] = sols[i][j].value(mantaRay.passengers)
    
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    surf = ax.plot_surface(X, Y, Z, cmap="viridis")
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_zlabel(z_title)

    print(Z)

    plt.show()

sols = make3dData(mantaRay.passengers, 3, 81, mantaRay.cargo, 1, 27)

make3dPlot(sols, score, "passengers", "cargo", "score")
make3dPlot(sols, M2_score, "passengers", "cargo", "M2 score")
make3dPlot(sols, M3_score, "passengers", "cargo", "M3 score")
make3dPlot(sols, mantaRay.banner_length, "passengers", "cargo", "Banner Length")
make3dPlot(sols, M2lapper.turn_load_factor, "passengers", "cargo", "M2 G's")
make3dPlot(sols, M2lapper.lap_time, "passengers", "cargo", "M2 Lap Time")
make3dPlot(sols, M2lapper.straight_speed, "passengers", "cargo", "M2 Flight Speed")
