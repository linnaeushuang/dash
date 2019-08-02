import numpy as np
import matplotlib.pyplot as plt
import os

RESULTS_FOLDER = './results/'
NUM_BINS = 100
BITS_IN_BYTE = 8.0
MILLISEC_IN_SEC = 1000.0
M_IN_B = 1000000.0
VIDEO_LEN = 48
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]
K_IN_M = 1000.0
REBUF_P = 4.3
SMOOTH_P = 1
COLOR_MAP = plt.cm.jet  # nipy_spectral, Set1,Paired
SIM_DP = 'sim_dp'
# SCHEMES = ['BB', 'RB', 'FIXED', 'FESTIVE', 'BOLA', 'RL',  'sim_rl', SIM_DP]
#SCHEMES = ['rl_sim', SIM_DP]
SCHEMES = ['rl_sim','mpc_sim','bb_sim','mpcfast_sim']


def main():
    time_all = {}
    bit_rate_all = {}
    buff_all = {}
    bw_all = {}
    raw_reward_all = {}

    for scheme in SCHEMES:
        time_all[scheme] = {}
        raw_reward_all[scheme] = {}
        bit_rate_all[scheme] = {}
        buff_all[scheme] = {}
        bw_all[scheme] = {}

    log_files = os.listdir(RESULTS_FOLDER)
    for log_file in log_files:

        time_ms = []
        bit_rate = []
        buff = []
        bw = []
        reward = []

        #print log_file

        with open(RESULTS_FOLDER + log_file, 'rb') as f:
            if 'BW' in log_file:
                bw_est_time = []
                bw_est = []
                for line in f:
                    parse = line.split()
                    if len(parse) <= 1:
                        break

                    bw_est_time.append(float(parse[0]))
                    time_ms.append(float(parse[0]))
                    bw_est.append(float(parse[1]))
            elif SIM_DP in log_file:
                last_t = 0
                last_b = 0
                last_q = 1
                lines = []
                for line in f:
                    lines.append(line)
                    parse = line.split()
                    if len(parse) >= 6:
                        time_ms.append(float(parse[3]))
                        bit_rate.append(VIDEO_BIT_RATE[int(parse[6])])
                        buff.append(float(parse[4]))
                        bw.append(float(parse[5]))

                for line in reversed(lines):
                    parse = line.split()
                    r = 0
                    if len(parse) > 1:
                        t = float(parse[3])
                        b = float(parse[4])
                        q = int(parse[6])
                        if b == 4:
                            rebuff = (t - last_t) - last_b
                            assert rebuff >= -1e-4
                            r -= REBUF_P * rebuff

                        r += VIDEO_BIT_RATE[q] / K_IN_M
                        r -= SMOOTH_P * np.abs(VIDEO_BIT_RATE[q] - VIDEO_BIT_RATE[last_q]) / K_IN_M
                        reward.append(r)

                        last_t = t
                        last_b = b
                        last_q = q

            else:
                for line in f:
                    parse = line.split()
                    if len(parse) <= 1:
                        break
                    time_ms.append(float(parse[0]))
                    bit_rate.append(int(parse[1]))
                    buff.append(float(parse[2]))
                    bw.append(float(parse[4]) / float(parse[5]) * BITS_IN_BYTE * MILLISEC_IN_SEC / M_IN_B)
                    reward.append(float(parse[6]))

        if SIM_DP in log_file:
            time_ms = time_ms[::-1]
            bit_rate = bit_rate[::-1]
            buff = buff[::-1]
            bw = bw[::-1]

        time_ms = np.array(time_ms)
        time_ms -= time_ms[0]

        # print log_file

        for scheme in SCHEMES:
            if scheme in log_file and 'BW' not in log_file:
                time_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = time_ms
                bit_rate_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = bit_rate
                buff_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = buff
                bw_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = bw
                raw_reward_all[scheme][log_file[len('log_' + str(scheme) + '_'):]] = reward
                break
    plt.subplot(131)
    #for scheme in SCHEMES:
    #    plt.plot(np.multiply(bit_rate_all[scheme]['0'],0.001),label=scheme)
    plt.plot(np.multiply(bit_rate_all['rl_sim']['0'], 0.001), label='rl_sim')
    plt.plot(np.multiply(bit_rate_all['mpc_sim']['0'], 0.001), label='mpc_sim')
    plt.legend()
    plt.ylabel('Bit rate (Mbps)')
    plt.xticks([])

    plt.subplot(132)
    for scheme in SCHEMES:
        plt.plot(buff_all[scheme]['0'],label=scheme)
    plt.legend()
    plt.ylabel('Buffer size (sec)')
    plt.xticks([])

    plt.subplot(133)
    plt.plot(bw_est_time,np.multiply(bw_est,8),label='robustMPC estimation')
    plt.legend()
    plt.ylabel('Throughput (Mbps)')

    plt.show()
if __name__ == '__main__':
    main()
