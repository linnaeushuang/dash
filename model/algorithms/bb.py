import numpy as np



S_INFO = 5  # bit_rate, buffer_size, rebuffering_time, bandwidth_measurement, chunk_til_video_end
S_LEN = 8  # take how many frames in the past
A_DIM = 6
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
BITRATE_REWARD = [1, 2, 3, 12, 15, 20]
BUFFER_NORM_FACTOR = 10.0
CHUNK_TIL_VIDEO_END_CAP = 48.0
TOTAL_VIDEO_CHUNKS = 48
M_IN_K = 1000.0
REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
SMOOTH_PENALTY = 1
DEFAULT_QUALITY = 0  # default video quality without agent
RANDOM_SEED = 42
RAND_RANGE = 1000000
# total buffer is 35(sec)
#RESEVOIR and CUSHION will be changed to .4total~.6total ?
RESEVOIR = 5  # BB
CUSHION = 10  # BB
SUMMARY_DIR = './results'
LOG_FILE = './results/log_bb'
# log in format of time_stamp bit_rate buffer_size rebuffer_time chunk_size download_time reward
# NN_MODEL = './models/nn_model_ep_5900.ckpt'

DATA_PATH = './data'


def main():

    np.random.seed(RANDOM_SEED)

    assert len(VIDEO_BIT_RATE) == A_DIM


    log_path = LOG_FILE + '_sim_0'
    log_file = open(log_path, 'wb')

    epoch = 0
    time_stamp = 0

    last_bit_rate = DEFAULT_QUALITY
    bit_rate = DEFAULT_QUALITY

    r_batch = []

    video_count = 0

    delay_file = open(DATA_PATH + '/lastdownloadtime0')
    #sleep_file = open(DATA_PATH + '/rebufftime0')
    buffer_size_file = open(DATA_PATH + '/buffer0')
    rebuf_file = open(DATA_PATH + '/rebufftime0')
    video_chunk_size_file = open(DATA_PATH + '/chunk_size0')
    video_chunk_remain_file = open(DATA_PATH + '/m_segmentleft0')

    while True:  # serve video forever
        # the action is from the last decision
        # this is to make the framework similar to the real
        with open(DATA_PATH + '/permission0') as enable:
            key = enable.read()
            if key == '1':
                output_file = open(DATA_PATH + '/predict0','a')
                file_permission = open(DATA_PATH + '/permission0','a')
                
                delay = delay_file.readline().split('\n')[0]
                delay = float(delay)*1000
                
                sleep_time = 0.0#float(sleep_file.readline().split('\n')[0])
                
                buffer_size = float(buffer_size_file.readline().split('\n')[0])
                buffer_size = max(buffer_size,0)
                
                rebuf = float(rebuf_file.readline().split('\n')[0])
                
                video_chunk_size = float(video_chunk_size_file.readline().split('\n')[0])
                
                next_video_chunk_sizes = np.multiply(VIDEO_BIT_RATE, 500)
                
                video_chunk_remain = float(video_chunk_remain_file.readline().split('\n')[0])
                
                if video_chunk_remain == 0:
                    end_of_video = 1
                else:
                    end_of_video = 0

                time_stamp += delay  # in ms
                time_stamp += sleep_time  # in ms

                # reward is video quality - rebuffer penalty
                reward = VIDEO_BIT_RATE[bit_rate] / M_IN_K \
                         - REBUF_PENALTY * rebuf \
                         - SMOOTH_PENALTY * np.abs(VIDEO_BIT_RATE[bit_rate] -
                                                   VIDEO_BIT_RATE[last_bit_rate]) / M_IN_K

                # log scale reward
                # log_bit_rate = np.log(VIDEO_BIT_RATE[bit_rate] / float(VIDEO_BIT_RATE[0]))
                # log_last_bit_rate = np.log(VIDEO_BIT_RATE[last_bit_rate] / float(VIDEO_BIT_RATE[0]))

                # reward = log_bit_rate \
                #          - REBUF_PENALTY * rebuf \
                #          - SMOOTH_PENALTY * np.abs(log_bit_rate - log_last_bit_rate)

                # reward = BITRATE_REWARD[bit_rate] \
                #          - 8 * rebuf - np.abs(BITRATE_REWARD[bit_rate] - BITRATE_REWARD[last_bit_rate])


                r_batch.append(reward)

                last_bit_rate = bit_rate

                # log time_stamp, bit_rate, buffer_size, reward
                log_file.write(str(time_stamp / M_IN_K) + '\t' +
                               str(VIDEO_BIT_RATE[bit_rate]) + '\t' +
                               str(buffer_size) + '\t' +
                               str(rebuf) + '\t' +
                               str(video_chunk_size) + '\t' +
                               str(delay) + '\t' +
                               str(reward) + '\n')
                log_file.flush()

                if buffer_size < RESEVOIR:
                    bit_rate = 0
                elif buffer_size >= RESEVOIR + CUSHION:
                    bit_rate = A_DIM - 1
                else:
                    bit_rate = (A_DIM - 1) * (buffer_size - RESEVOIR) / float(CUSHION)
                
                bit_rate = int(bit_rate)

                output_file.write(str(VIDEO_BIT_RATE[int(bit_rate)] * 1000) + '\n')
                file_permission.write('0\n')
                output_file.close()
                file_permission.close()

                if end_of_video:
                    log_file.write('\n')
                    log_file.close()

                    last_bit_rate = DEFAULT_QUALITY
                    bit_rate = DEFAULT_QUALITY  # use the default action here
                    r_batch = []

                    print "video count", video_count
                    video_count += 1


                    log_path = LOG_FILE + '_sim_' + str(video_count)
                    log_file = open(log_path, 'wb')


if __name__ == '__main__':
    main()

