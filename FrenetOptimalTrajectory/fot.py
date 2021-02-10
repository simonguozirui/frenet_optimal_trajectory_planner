import fot_wrapper
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patch
import sys, getopt
from pathlib import Path


def main(show_animation=False, show_info=False, save_frame=False):

    conds = {
        's0': 0,
        'target_speed': 20,
        'wp': [[0, 0], [50, 0], [150, 0]],
        'obs': [[48, -2, 52, 2],
                [98, -4, 102, 2],
                [98, 6, 102, 10],
                [128, 2, 132, 6]],
        'pos': [0, 0],
        'vel': [0, 0],
    } # paste output from debug log

    initial_conditions = {
        'ps': conds['s0'],
        'target_speed': conds['target_speed'],
        'pos': np.array(conds['pos']),
        'vel': np.array(conds['vel']),
        'wp': np.array(conds['wp']),
        'obs': np.array(conds['obs'])
    }

    hyperparameters = {
        "max_speed": 25.0,
        "max_accel": 15.0,
        "max_curvature": 15.0,
        "max_road_width_l": 5.0,
        "max_road_width_r": 5.0,
        "d_road_w": 0.5,
        "dt": 0.2,
        "maxt": 5.0,
        "mint": 2.0,
        "d_t_s": 0.5,
        "n_s_sample": 2.0,
        "obstacle_clearance": 0.1,
        "kd": 1.0,
        "kv": 0.1,
        "ka": 0.1,
        "kj": 0.1,
        "kt": 0.1,
        "ko": 0.1,
        "klat": 1.0,
        "klon": 1.0,
        "num_threads": 4,
    }
    # static elements of planner
    wx = initial_conditions['wp'][:, 0]
    wy = initial_conditions['wp'][:, 1]
    obs = np.array(conds['obs'])

    # simulation config
    # show_animation = False
    sim_loop = 200
    area = 40
    total_time = 0
    time_list = []
    for i in range(sim_loop):
        # run FOT and keep time
        print("Iteration: {}".format(i))
        start_time = time.time()
        result_x, result_y, speeds, ix, iy, iyaw, d, s, speeds_x, \
            speeds_y, misc, costs, success = \
            fot_wrapper.run_fot(initial_conditions, hyperparameters)
        end_time = time.time() - start_time
        print("Time taken: {}".format(end_time))
        total_time += end_time
        time_list.append(end_time)
        
        # reconstruct initial_conditions
        if success:
            initial_conditions['pos'] = np.array([result_x[1], result_y[1]])
            initial_conditions['vel'] = np.array([speeds_x[1], speeds_y[1]])
            initial_conditions['ps'] = misc['s']
            if show_info:
                print(costs)
        else:
            print("Failed unexpectedly")
            break

        # break if near goal
        if np.hypot(result_x[1] - wx[-1], result_y[1] - wy[-1]) <= 3.0:
            print("Goal")
            break

        if show_animation:  # pragma: no cover
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect(
                'key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None]
            )
            plt.plot(wx, wy)
            if obs.shape[0] == 0:
                obs = np.empty((0, 4))
            ax = plt.gca()
            for o in obs:
                rect = patch.Rectangle((o[0], o[1]),
                                       o[2] - o[0],
                                       o[3] - o[1])
                ax.add_patch(rect)
            plt.plot(result_x[1:], result_y[1:], "-or")
            plt.plot(result_x[1], result_y[1], "vc")
            plt.xlim(result_x[1] - area, result_x[1] + area)
            plt.ylim(result_y[1] - area, result_y[1] + area)
            plt.xlabel("X axis")
            plt.ylabel("Y axis")
            plt.title("v[m/s]:" + str(
                      np.linalg.norm(initial_conditions['vel']))[0:4]
            )
            plt.grid(True)
            if save_frame:
                Path("img/frames").mkdir(parents=True, exist_ok=True)
                plt.savefig("img/frames/{}.jpg".format(i))
            plt.pause(0.1)

    print("Finish")
    print("Total time for {} iterations taken: {}".format(i, total_time))
    print("Average time per iteration: {}".format(total_time / i))
    print("Max time per iteration: {}".format(max(time_list)))

    plt.plot(time_list)
    plt.hlines(total_time/i, 0, i, colors = 'c', label = 'average time', linestyles = 'dashed')
    plt.xlabel("Iteration #")
    plt.ylabel("Time Per Iteration")
    plt.title("Planning Execution Time Per Iteration")
    plt.gcf().canvas.mpl_connect(
        'key_release_event',
        lambda event: [exit(0) if event.key == 'escape' else None]
    )
    plt.show()

if __name__ == '__main__':
    argument_list = sys.argv[1:]
    short_options = "dvs"
    long_options = ["display", "verbose", "save"]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        print (str(err))
        sys.exit(2)

    enable_verbose, enable_saving, enable_display = False, False, False

    for current_argument, current_value in arguments:
        if current_argument in ("-d", "--display"):
            print ("Showing Animation, Ensure you have X11 forwarding server open")
            enable_display = True
        elif current_argument in ("-v", "--verbose"):
            print ("Enabling verbose mode, showing all state info")
            enable_verbose = True
        elif current_argument in ("-s", "--save"):
            print ("Saving each frame of simulation")
            enable_display, enable_saving = True, True

    main(enable_display, enable_verbose, enable_saving)
