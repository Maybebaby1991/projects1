
def get_grid(fich):
    import numpy as np

    nk = 0
    with open(fich, "r") as f:
        for line in f:
            nk += 1

    grid = np.zeros([nk, 3])
    nk = 0
    with open(fich, "r") as f:
        for line in f:
            grid_line = line.split()
            grid[nk][0] = grid_line[0]
            grid[nk][1] = grid_line[1]
            grid[nk][2] = grid_line[2]
            nk += 1

    return grid


# ----------------------------------------------------------------------------------------#
def read_file(fich, grid):
    import numpy as np

    clmn = int(0)
    data = {}
    line_numb = 0
    kk = np.zeros(3)
    hole = False
    with open(fich, "r") as f:
        initial = True
        for line in f:
            data_line = line.split()
            if len(data_line) != 0:
                datai = []
                if initial:
                    clmn = len(data_line)
                    for i in range(0, clmn): # chek if we have hole representation
                        if float(data_line[i]) > 0.9:
                            hole = True
                    initial = False
                for j in range(0, 3):
                    kk[j] = grid[line_numb][j]
                    if abs(float(kk[j])) < 1.e-6:
                        kk[j] = 0.0
                key = str(kk[0]) + " " + str(kk[1]) + " " + str(kk[2])
                for i in range(0, clmn):
                    if hole:
                        datai.append(1 - float(data_line[i]))
                    else:
                        datai.append(float(data_line[i]))

                    
                data[key] = datai
                line_numb += 1

    return clmn, data


# def read_file_FIX_P(fich, grid):
#     clmn = int(0)
#     data = {}
#     line_numb = 0
#     kk = np.zeros(3)
#     with open(fich, "r") as f:
#         initial = True
#         for line in f:
#             data_line = line.split()
#             if not (float(data_line[0])==0 and float(data_line[1])==0) :
#                 if len(data_line) != 0:
#                     datai = []
#                     if initial:
#                         clmn = len(data_line)
#                         initial = False
#                     for j in range(0, 3):
#                         kk[j] = grid[line_numb][j]
#                         if abs(float(kk[j])) < 1.e-6:
#                             kk[j] = 0.0
#                     key = str(kk[0]) + " " + str(kk[1]) + " " + str(kk[2])
#                     for i in range(0, clmn):
#                         datai.append(float(data_line[i]))
#                     data[key] = datai
#                     line_numb += 1

#     print(line_numb)

#     return clmn, data

# ----------------------------------------------------------------------------------------#
def get_color_max(fich, Edia_0, clmn):
    import numpy as np

    color_max = np.zeros(clmn) - 1000000000000000000
    color_min = np.zeros(clmn) + 1000000000000000000
    line_numb = 0
    with open(fich, "r") as f:
        for line in f:
            kk = line.split()
            if len(kk) != 0:
                for num_row in range(0, clmn):
                    if color_max[num_row] < (float(kk[num_row]) - Edia_0[num_row][line_numb]):
                        color_max[num_row] = (
                            float(kk[num_row]) - Edia_0[num_row][line_numb])
                    if color_min[num_row] > (float(kk[num_row]) - Edia_0[num_row][line_numb]):
                        color_min[num_row] = (
                            float(kk[num_row]) - Edia_0[num_row][line_numb])
            line_numb += 1
    # print("color_max", color_max)
    # print("color_min", color_min)
    return color_max, color_min
    # ----------------------------------------------------------------------------------------#


def get_x(fich):
    import numpy as np
    x = [[], [], []]
    initial = True
    readon = True
    kk = np.zeros(3)
    with open(fich, "r") as f:
        for line in f:
            kk = line.split()
            if len(kk) != 0:
                if not initial:
                    for i in range(0, 3):
                        if abs(float(kk[i])) < 1.e-6:
                            kk[i] = 0.0
                        if float(x[i][-1]) < float(kk[i]):
                            readon = True
                        else:
                            readon = False
                        if readon:
                            x[i].append(kk[i])
                if initial:
                    for i in range(0, 3):
                        x[i].append(kk[i])
                    initial = False
        return x


# ----------------------------------------------------------------------------------------#
def from_cart_to_crys(xx, yy):
    import numpy as np
    a = 2.5
    # a = 2.895
    x = a / (4 * np.pi) * yy + np.sqrt(3.) * a / (4. * np.pi) * xx
    y = -a / (4 * np.pi) * yy + np.sqrt(3.) * a / (4. * np.pi) * xx
    x = x.flatten()
    y = y.flatten()
    # print(x.shape, y.shape)
    for idx, j in enumerate(x):
        while (np.abs(x[idx]) > 0.5):
            x[idx] = x[idx] - np.sign(x[idx])
            # print(np.sign(x[idx]), x[idx])
    for idx, j in enumerate(y):
        while (np.abs(y[idx]) > 0.5):
            y[idx] = y[idx] - np.sign(y[idx])

    return x, y


def create_data_data0(data, data0, nx, ny, x, y, ii, jj, fixed_x, num_col):
    import numpy as np
    z = (np.arange(nx * ny).reshape(ny, nx) * 0.1)
    value = 0.0
    for j in y:  # normal printing
        for i in x:
            if ii == 2 and jj == 1:
                value = data[str(fixed_x) + " " + str(j) + " " + str(i)][num_col] - \
                    data0[str(fixed_x) + " " + str(j) + " " + str(i)][num_col]
            if ii == 2 and jj == 0:
                value = data[str(j) + " " + str(fixed_x) + " " + str(i)][num_col] - \
                    data0[str(j) + " " + str(fixed_x) + " " + str(i)][num_col]
            if ii == 1 and jj == 0:
                value = data[str(j) + " " + str(i) + " " + str(fixed_x)][num_col] - \
                    data0[str(j) + " " + str(i) + " " + str(fixed_x)][num_col]
            z[list(y).index(j)][list(x).index(i)] = value
    return z


def create_data(data, nx, ny, x, y, ii, jj, fixed_x, num_col):
    import numpy as np
    z = (np.arange(nx * ny).reshape(ny, nx) * 0.1)
    value = 0.0
    for j in y:  # normal printing
        for i in x:
            if ii == 2 and jj == 1:
                value = data[str(fixed_x) + " " + str(j) +
                             " " + str(i)][num_col]
            if ii == 2 and jj == 0:
                value = data[str(j) + " " + str(fixed_x) +
                             " " + str(i)][num_col]
            if ii == 1 and jj == 0:
                value = data[str(j) + " " + str(i) + " " +
                             str(fixed_x)][num_col]
            z[list(y).index(j)][list(x).index(i)] = value
    return z





# find points with minimums of energy to draw a picture of it later
def find_energy_min(r, E_matr, fixed_x, ii, jj):
    import numpy as np
    from cbwe_Python_source.plot_BZ_preparation import from_cart_to_crys
    from cbwe_Python_source.plot_BZ_preparation import create_data
    from scipy import interpolate

    xx = np.array(r[ii])
    x = xx.astype(float)
    yy = np.array(r[jj])
    y = yy.astype(float)

    nx = len(x)
    ny = len(y)

    # E_matr =  create_data(E_matr,  nx, ny, x, y, ii, jj, fixed_x, 2) # with excitons
    E_matr =  create_data(E_matr,  nx, ny, x, y, ii, jj, fixed_x, 0) # IPA
    E_interp = interpolate.interp2d(x, y, E_matr, kind='linear')

    Xcart, Ycart = np.meshgrid(
        np.linspace(-2, 2, 500), np.linspace(-2, 2, 500))
    xcrys, ycrys = from_cart_to_crys(Xcart, Ycart)

    E_interp_shaped = np.zeros(len(xcrys))

    for idx, x in enumerate(xcrys):
        E_interp_shaped[idx]    = E_interp(xcrys[idx], ycrys[idx])

    len_E = int(np.sqrt(len(E_interp_shaped)))
    E_interp_shaped   = E_interp_shaped.reshape( len_E,   len_E)

    
    n_min = 6 # six minimums
    Emin_x = np.zeros(n_min)
    Emin_y = np.zeros(n_min)
    for n_min_iter in range(0,n_min):
        Emin = 1000000000;
        for kx in range(0,len_E):
            for ky in range(0,len_E):
                if (E_interp_shaped[kx][ky] < Emin):
                    Emin = E_interp_shaped[kx][ky]
                    Emin_x[n_min_iter] = kx
                    Emin_y[n_min_iter] = ky
        for dkx in range(-10,10):
            for dky in range(-10,10):
                E_interp_shaped[int(Emin_x[n_min_iter]) + dkx][int(Emin_y[n_min_iter]) + dky] = Emin + 10


    
    return Emin_x, Emin_y





def plot_data_subplots(Xcart, Ycart, zi_cond, P_cond_i, Re_P_vc_i, Im_P_vc_i, angle_Pvc, title_subplots, 
    save_marker, color_min, color_max,
    Emin_x, Emin_y,
    folder_of_set, Ey,Ez, t, time_snapshot, num_of_step):
    import numpy as np
    import matplotlib.pyplot as plt

    au_to_eV = 27.211324570273 #
    au_to_meV = 1000*au_to_eV #

    plt.figure(figsize=(20, 16))
    
    plt.suptitle("t = " + str(round(time_snapshot[int(num_of_step)], 2)) + " fs" + " \n" + folder_of_set)
    plt.subplots_adjust(wspace=0, hspace=1)

    # Electric field
    ax1 = plt.subplot2grid((5, 4), (0, 0), rowspan=1, colspan=4)
    ax1.plot(t, Ey, color='b', label = "Ex")
    ax1.plot(t, Ez, color='g', label = "Ey")
    ax1.legend()
    ax1.axvline(x=time_snapshot[int(num_of_step)], color='r')
    ax1.set_xlabel("t (fs)")
    ax1.title.set_text('E(t)')

    # Polar plot for vector potential
    # ax2 = plt.subplot2grid((3, 3), (0, 2), rowspan=1,
    #                        colspan=1, projection='polar')

    # ax2.scatter(np.arctan2(Az[int(label)], Ay[int(label)]),
    #             np.sqrt(Ay[int(label)] * Ay[int(label)] + Az[int(label)] * Az[int(label)]), s=10, c='r', zorder=10)
    # ax2.plot(np.arctan2(Az, Ay), np.sqrt(Ay * Ay + Az * Az), zorder=4)
    # theta = np.ones(2) * np.arctan2(Az[int(label)], Ay[int(label)])
    # r = np.array([0, np.max(np.sqrt(Ay * Ay + Az * Az) * 1.1)])
    # ax2.set_rlim(0, np.max(np.sqrt(Ay * Ay + Az * Az) * 1.1))
    # ax2.plot(theta, r, color='red', zorder=5)
    # ax2.set_rticks([])

    # Energy
    cmap_energ=plt.get_cmap('jet')
    cmap_population=plt.get_cmap('jet')

    # ax3 = plt.subplot2grid((3, 6), (1, 0), rowspan=2, colspan=2)
    # # z_diff = np.subtract(zi, np.flipud(zi))
    # im = ax3.pcolormesh(Xcart, Ycart, zi_core, cmap=cmap_energ)  # bwr'))
    # # im.set_clim(0.6*np.amax(zi), np.amax(zi))
    # ax3.set_xlabel("$k_x$")
    # ax3.set_ylabel("$k_y$")
    # plt.colorbar(im)
    # ax3.title.set_text("Core band energy shift")
    # ax3.set_aspect('equal')

    if len(title_subplots) < 5:
        axEc = plt.subplot2grid((5, 4), (1, 0), rowspan=2, colspan=2)
        # im = axEc.pcolormesh(Xcart, Ycart, au_to_meV*zi_cond,  vmin= 0.9*au_to_meV*color_min[2],vmax= 2*au_to_meV*color_max[2], cmap=cmap_energ, shading='auto')  # bwr'))
        im = axEc.pcolormesh(Xcart, Ycart, au_to_meV*zi_cond,   cmap=cmap_energ, shading='auto')  # bwr'))

        # im.set_clim(0.6*np.amax(zi), np.amax(zi))


        axEc.set_xlabel("$k_x$")
        axEc.set_ylabel("$k_y$")
        # plt.set_clim(0.,0.95*color_max);
        plt.colorbar(im)
        axEc.title.set_text(title_subplots[1])
        axEc.set_aspect('equal')
        plt.text(-1.7, 0.5, "K", fontsize=20)
        plt.text(0.15, 1.5, "K'", fontsize=20)
        for i in range(0,6):
            plt.scatter(Xcart[int(Emin_x[i])][ int(Emin_y[i])],Ycart[int(Emin_x[i])][ int(Emin_y[i])],color='black')
        # plt.plot(Emin_x, Emin_y, color = "black", marker = "*")

    axPc = plt.subplot2grid((5, 4), (1, 2), rowspan=2, colspan=2)
    im = axPc.pcolormesh(Xcart, Ycart, P_cond_i,  cmap=cmap_population, shading='auto')  # bwr'))
    # im.set_clim(0.6*np.amax(zi), np.amax(zi))
    axPc.set_xlabel("$k_x$")
    axPc.set_ylabel("$k_y$")
    plt.colorbar(im)
    axPc.title.set_text(title_subplots[2])
    axPc.set_aspect('equal')
    # plt.text(-1.7, 0.5, "K", fontsize=20)
    # plt.text(0.15, 1.5, "K'", fontsize=20)


    axRe_pvc = plt.subplot2grid((5, 4), (3, 0), rowspan=2, colspan=2)

    im = axRe_pvc.pcolormesh(Xcart, Ycart, angle_Pvc, cmap=cmap_population, shading='auto')  # bwr'))
    
    for i in range(0,6):
        plt.scatter(Xcart[int(Emin_x[i])][ int(Emin_y[i])],Ycart[int(Emin_x[i])][ int(Emin_y[i])],color='black')
    # im.set_clim(0.6*np.amax(zi), np.amax(zi))
    axRe_pvc.set_xlabel("$k_x$")
    axRe_pvc.set_ylabel("$k_y$")
    plt.colorbar(im)
    axRe_pvc.title.set_text(title_subplots[3])
    axRe_pvc.set_aspect('equal')
    # plt.text(-1.7, 0.5, "K", fontsize=20)
    # plt.text(0.15, 1.5, "K'", fontsize=20)

    if len(title_subplots) > 4:
        axIm_pvc = plt.subplot2grid((5, 4), (3, 2), rowspan=2, colspan=2)
        P_cond_i_pintLog = np.log10( np.array(P_cond_i))
        im = axIm_pvc.pcolormesh(Xcart, Ycart, P_cond_i_pintLog, cmap=cmap_energ, shading='auto')  # bwr'))
        # im.set_clim(0.6*np.amax(zi), np.amax(zi))
        axIm_pvc.set_xlabel("$k_x$")
        axIm_pvc.set_ylabel("$k_y$")
        plt.colorbar(im)
        axIm_pvc.title.set_text(title_subplots[4])
        axIm_pvc.set_aspect('equal')
        # plt.text(-1.7, 0.5, "K", fontsize=20)
        # plt.text(0.15, 1.5, "K'", fontsize=20)

    if len(title_subplots) > 5:
        axEc = plt.subplot2grid((5, 4), (1, 0), rowspan=2, colspan=2)
        # im = axEc.pcolormesh(Xcart, Ycart, au_to_meV*zi_cond,  vmin= 0.9*au_to_meV*color_min[2],vmax= 2*au_to_meV*color_max[2], cmap=cmap_energ, shading='auto')  # bwr'))
        AbsP = np.array(Re_P_vc_i) * np.array(Re_P_vc_i) + np.array(Im_P_vc_i) * np.array(Im_P_vc_i)
        im = axEc.pcolormesh(Xcart, Ycart, AbsP,   cmap=cmap_energ, shading='auto')  # bwr'))
        # im.set_clim(0.6*np.amax(zi), np.amax(zi))
        axEc.set_xlabel("$k_x$")
        axEc.set_ylabel("$k_y$")
        # plt.set_clim(0.,0.95*color_max);
        plt.colorbar(im)
        axEc.title.set_text(title_subplots[5])
        axEc.set_aspect('equal')

    # namefile = folder_of_set+ "/" + save_marker + "/Xcart" + ".txt"
    # np.savetxt(namefile, Xcart)

    # namefile = folder_of_set+ "/" + save_marker + "/Ycart" + ".txt"
    # np.savetxt(namefile, Ycart)

    # namefile = folder_of_set+ "/" + save_marker + "/Pvc" + num_of_step + ".txt"
    # np.savetxt(namefile, AbsP)

    plt.savefig(folder_of_set+"/" + save_marker + "/Ek_" + num_of_step + ".png")
    plt.clf()
    plt.close('all')



def calculate_K_Kprime_difference(nK_minus_nKpime, t_nK_minus_nKpime,
        namefolder, folder_of_set, label, time_snapshot, i):
    import numpy as np

    P_cond_file = np.loadtxt(namefolder + "/Output/P_cond_in_eigenstate_" + label + ".txt", unpack=True)
    P_cond = np.array(P_cond_file[0])

    Nk= int(np.sqrt(len(P_cond))) ; # number of points in BZ
    # P_matrix_c = np.zeros(Nk,Nk)
    N_K_valley = 0
    N_Kprime_valley = 0

    for ik in range (0, Nk*Nk):
        ikx =  ik // Nk 
        iky =  ik % Nk 


        if (ikx + iky > Nk):
            N_K_valley += P_cond[ik]
        elif (ikx + iky < Nk):
            N_Kprime_valley += P_cond[ik]

    N_K_valley /= Nk*Nk
    N_Kprime_valley /= Nk*Nk
    print("N_Kprime_valley - N_K_valley ", (N_Kprime_valley - N_K_valley)/(N_Kprime_valley + N_K_valley) )
    print("time_snapshot ", time_snapshot[i])
    nK_minus_nKpime.append((N_Kprime_valley - N_K_valley)/(N_Kprime_valley + N_K_valley))
    t_nK_minus_nKpime.append(time_snapshot[i])

    return nK_minus_nKpime, t_nK_minus_nKpime 


def plot_K_Kprime_difference(nK_minus_nKpime, t_nK_minus_nKpime,
        namefolder, folder_of_set, t, Ey, Ez):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    data_K_K_prime = np.array([t_nK_minus_nKpime, nK_minus_nKpime])

    namefile = folder_of_set + "/K_minus_Kprime" + namefolder + ".txt"
    np.savetxt(namefile, data_K_K_prime)

    plt.figure(figsize=(15, 7.5))
    plt.suptitle("Valley difference \n" + folder_of_set)
    plt.subplot(211)
    plt.title("Electric field")
    pl_Ex, = plt.plot(t, Ey, label = 'Ex') # signal
    pl_Ey, = plt.plot(t, Ez, label = 'Ey') # signal
    plt.xlabel("time, fs")
    plt.ylabel("Electric field")
    plt.legend(handles=[pl_Ex, pl_Ey])
    plt.grid(True)
    plt.ticklabel_format(style="sci", scilimits=(0,0), axis="y")



    plt.subplot(212)
    plt.title("n(K) - n(K')/ (n(K) + n(K'))")
    plt.plot(t_nK_minus_nKpime, nK_minus_nKpime) # signal
    plt.xlabel("time, fs")
    plt.ylabel("n(K) - n(K') / (n(K) + n(K'))")
    plt.grid(True)


    plt.savefig(folder_of_set+"/nK_Kprime.png")
    plt.clf()
    plt.close('all')




# plt.show()

# im=plt.pcolormesh(Xcart, Ycart, zi, cmap=plt.get_cmap('Reds'))#bwr'))
# plt.clim(0.,0.9*color_max);
# plt.xlabel("x")
# plt.ylabel("y")
# plt.colorbar(im)
# plt.savefig(outputfile)
# plt.close()


# # ----------------------------------------------------------------------------------------#
# def make_movie(collection, folder_of_set, label_name):
#     from PIL import Image
#     import glob
#     # Create the frames
#     frames = []
#     # imgs = glob.glob(namefolder+"/*.png")
#     imgs = [numeric_string for numeric_string in collection]
#     for i in imgs:
#         new_frame = Image.open(i)
#         frames.append(new_frame)

#     # Save into a GIF file that loops forever
#     # movie_Oct16_X_3_minus_Xstatic_3
#     # movie_Oct10_N_3
#     frames[0].save(folder_of_set + "/" + label_name + ".gif", format='GIF',
#                    dpi=(300, 300),
#                    append_images=frames[1:],
#                    save_all=True,
#                    duration=50, loop=0)
