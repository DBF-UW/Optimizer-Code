import aerosandbox as asb
import aerosandbox.numpy as np
import matplotlib.pyplot as plt
import constants
import unit_conversion  as uc   
import aircraft
import constraints
import simple_lap_simulator    
import mission_sim
from mpl_toolkits.mplot3d import Axes3D

opti = asb.Opti()
airfoil_name = "naca0012"  # or any valid airfoil string

mantaRay = aircraft.Aircraft(opti, airfoil_name)
M2lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=True, banner=False)
M3lapper = simple_lap_simulator.LapSimulator(opti, mantaRay, payload=False, banner=True)
constraints.constraints(opti, mantaRay)
M2_score = mission_sim.M2(mantaRay, M2lapper) 
M3_score = mission_sim.M3(mantaRay, M3lapper)
GM_score = mission_sim.GM(mantaRay)

ultimate_sols = []
run_until = 100
MAX_PASSENGERS = opti.parameter()
opti.subject_to([mantaRay.passengers < MAX_PASSENGERS])

for j in np.arange(3, run_until+1):

    print("Max Passengers: ", j)
    opti.set_value(MAX_PASSENGERS, j)
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
    test_vals = np.arange(3, j+1)
    sols = []

    for i in test_vals:
        print("Trying: ", i)
        
        opti.maximize(score - 400*(mantaRay.passengers-i)**2)

        try:
            sol = opti.solve(verbose=False)
        except RuntimeError as e:   # CasADi solver error
            print(f"Solver failed for passengers: {i}")
            score = 0
        
        sols.append(sol)

    ultimate_sols.append(sols)

graph_points = []

for i in np.arange(0, len(ultimate_sols)): #iterate thru max passenger counts
    graph_point_row = []
    for j in np.arange(0, len(ultimate_sols)): #iterate through the scores of each passenger count in that max pass situation
        if j <= i:
            graph_point_row.append(ultimate_sols[i][j].value(score))
        else:
            graph_point_row.append(np.nan)
    graph_points.append(graph_point_row)

X, Y = np.meshgrid(np.arange(len(ultimate_sols)), np.arange(len(ultimate_sols)))
Z = np.array(graph_points)

print(Z)

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection="3d")

# Surface plot with heatmap coloring
surf = ax.plot_surface(X, Y, Z,
                       cmap="viridis",
                       edgecolor="none",
                       antialiased=True,
                       linewidth=0)

'''
# Add contour lines projected onto "floor" for clarity
ax.contourf(X, Y, graph_points, zdir='z', offset=np.nanmin(graph_points)-1,
            cmap="viridis", alpha=0.7)

fig.colorbar(surf, shrink=0.5, aspect=10, label="Score")
'''
ax.set_title("3D Surface of Triangular Matrix with Heatmap Coloring")
ax.set_xlabel("Passenger Count")
ax.set_ylabel("Maximum Passenger Count")
ax.set_zlabel("Score")

plt.show()
    









