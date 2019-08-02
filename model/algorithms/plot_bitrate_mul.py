import numpy as np
import matplotlib.pyplot as plt
import os

from typing import List

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
# SCHEMES = ['rl_sim', SIM_DP]
SCHEMES = ['rl_sim_mul', 'bb_sim_mul', 'mpc_sim_mul', 'mpcfast_sim_mul']


def main():
    time_all = {}
    bit_rate_all = {}
    buff_all = {}
    bw_all = {}
    raw_reward_all = {}
    bw_est_all = {}
    bw_est_time_all = {}
    time_trace_all = []
    bw_trace_all = []

    for scheme in SCHEMES:
        time_all[scheme] = {}
        raw_reward_all[scheme] = {}
        bit_rate_all[scheme] = {}
        buff_all[scheme] = {}
        bw_all[scheme] = {}
    bw_est_all['mpc_sim_mul'] = {}
    bw_est_time_all['mpc_sim_mul'] = {}

    log_files = os.listdir(RESULTS_FOLDER)

    with open('./tracefile') as f:
        for line in f:
            parse = line.split()
            if len(parse) <= 1:
                break
            time_trace_all.append(float(parse[0]))
            bw_trace_all.append(float(parse[1]))

    for log_file in log_files:

        time_ms = []
        bit_rate = []
        buff = []
        bw = []
        reward = []
        bw_est_time = []
        bw_est = []

        print log_file

        with open(RESULTS_FOLDER + log_file, 'rb') as f:
            if 'BW' in log_file:
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
            elif 'BW' in log_file:
                bw_est_all['mpc_sim_mul'][log_file[len('log_mpc_BW_sim_mul_'):]] = bw_est
                bw_est_time_all['mpc_sim_mul'][log_file[len('log_mpc_BW_sim_mul_'):]] = bw_est_time

    def plot_biterate():
        plt.subplot(241)
        plt.plot(np.multiply(bit_rate_all['rl_sim_mul']['0_0'], 0.001), label='client0')
        plt.plot(np.multiply(bit_rate_all['rl_sim_mul']['1_0'], 0.001), label='client1')
        plt.plot(np.multiply(bit_rate_all['rl_sim_mul']['2_0'], 0.001), label='client2')
        plt.legend()
        plt.title('Pensieve')
        plt.ylabel('Bit rate (Mbps)')
        plt.xticks([])

        plt.subplot(242)
        plt.plot(np.multiply(bit_rate_all['mpc_sim_mul']['0_0'], 0.001), label='client0')
        plt.plot(np.multiply(bit_rate_all['mpc_sim_mul']['1_0'], 0.001), label='client1')
        plt.plot(np.multiply(bit_rate_all['mpc_sim_mul']['2_0'], 0.001), label='client2')
        plt.legend()
        plt.title('robustMpc')
        plt.ylabel('Bit rate (Mbps)')
        plt.xticks([])

        plt.subplot(243)
        plt.plot(np.multiply(bit_rate_all['mpcfast_sim_mul']['0_0'], 0.001), label='client0')
        plt.plot(np.multiply(bit_rate_all['mpcfast_sim_mul']['1_0'], 0.001), label='client1')
        plt.plot(np.multiply(bit_rate_all['mpcfast_sim_mul']['2_0'], 0.001), label='client2')
        plt.legend()
        plt.title('fastMpc')
        plt.ylabel('Bit rate (Mbps)')
        plt.xticks([])

        plt.subplot(244)
        plt.plot(np.multiply(bit_rate_all['bb_sim_mul']['0_0'], 0.001), label='client0')
        plt.plot(np.multiply(bit_rate_all['bb_sim_mul']['1_0'], 0.001), label='client1')
        plt.plot(np.multiply(bit_rate_all['bb_sim_mul']['2_0'], 0.001), label='client2')
        plt.legend()
        plt.title('BB')
        plt.ylabel('Bit rate (Mbps)')
        plt.xticks([])

    def plot_buffer():
        plt.subplot(245)
        plt.plot(buff_all['rl_sim_mul']['0_0'], label='client0')
        plt.plot(buff_all['rl_sim_mul']['1_0'], label='client1')
        plt.plot(buff_all['rl_sim_mul']['2_0'], label='client2')
        plt.legend()
        plt.title('Pensieve')
        plt.ylabel('Buffer size (sec)')
        plt.xticks([])

        plt.subplot(246)
        plt.plot(buff_all['mpc_sim_mul']['0_0'], label='client0')
        plt.plot(buff_all['mpc_sim_mul']['1_0'], label='client1')
        plt.plot(buff_all['mpc_sim_mul']['2_0'], label='client2')
        plt.legend()
        plt.title('robustMpc')
        plt.ylabel('Buffer size (sec)')
        plt.xticks([])

        plt.subplot(247)
        plt.plot(buff_all['mpcfast_sim_mul']['0_0'], label='client0')
        plt.plot(buff_all['mpcfast_sim_mul']['1_0'], label='client1')
        plt.plot(buff_all['mpcfast_sim_mul']['2_0'], label='client2')
        plt.legend()
        plt.title('fastMpc')
        plt.ylabel('Buffer size (sec)')
        plt.xticks([])

        plt.subplot(248)
        plt.plot(buff_all['bb_sim_mul']['0_0'], label='client0')
        plt.plot(buff_all['bb_sim_mul']['1_0'], label='client1')
        plt.plot(buff_all['bb_sim_mul']['2_0'], label='client2')
        plt.legend()
        plt.title('BB')
        plt.ylabel('Buffer size (sec)')
        plt.xticks([])

    def plot_bw_est():
        plt.plot(bw_est_time_all['mpc_sim_mul']['0_0'], np.multiply(bw_est_all['mpc_sim_mul']['0_0'], 8),
                 label='client0')
        plt.plot(bw_est_time_all['mpc_sim_mul']['1_0'], np.multiply(bw_est_all['mpc_sim_mul']['1_0'], 8),
                 label='client1')
        plt.plot(bw_est_time_all['mpc_sim_mul']['2_0'], np.multiply(bw_est_all['mpc_sim_mul']['2_0'], 8),
                 label='client2')
        plt.plot(time_trace_all, bw_trace_all, label='True Bandwidth')
        plt.legend()
        plt.title('Bandwidth estimation(robustMpc)')
        plt.ylabel('Throughput (Mbps)')
        plt.xticks([])

    #plot_biterate()
    #plot_buffer()
    plot_bw_est()
    plt.show()


if __name__ == '__main__':
    main()
