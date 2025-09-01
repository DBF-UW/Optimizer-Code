def cd_from_geometry(L_ft, W_ft, H_ft, S_wet_ft2):
    a = 1.41716412e-3
    m = 9.47298596e-1
    c = -6.12146300e-4
    b = -8.15046939e-3
    return a * (S_wet_ft2 / (L_ft ** m)) + c * (W_ft * H_ft) + b