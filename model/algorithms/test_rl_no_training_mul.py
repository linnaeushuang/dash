import os
os.environ['CUDA_VISIBLE_DEVICES']=''
import numpy as np
import tensorflow as tf
import a3ctest as a3c
#import matplotlib.pyplot as plt
import sys
import multiprocessing as mp


S_INFO = 7  # bit_rate, buffer_size, next_chunk_size, bandwidth_measurement(throughput and time), chunk_til_video_end
S_LEN = 8  # take how many frames in the past
A_DIM = 6
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
VIDEO_BIT_RATE = [300,750,1200,1850,2850,4300]  # Kbps
BUFFER_NORM_FACTOR = 10.0
CHUNK_TIL_VIDEO_END_CAP = 48
M_IN_K = 1000.0
REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
SMOOTH_PENALTY = 1
DEFAULT_QUALITY = 0  # default video quality without agent
RANDOM_SEED = 42
RAND_RANGE = 1000
SUMMARY_DIR = './results'
LOG_FILE = './results/log'
# log in format of time_stamp bit_rate buffer_size rebuffer_time chunk_size download_time reward
NN_MODEL = './testmodels/nn_model_ep_20000.ckpt'

DATA_PATH = './data'

NUM_AGENT=7

def main( m_id ,shareData,tracename='none',allvideochunk=64):

    np.random.seed(RANDOM_SEED)

    assert len(VIDEO_BIT_RATE) == A_DIM

    if not os.path.exists(SUMMARY_DIR):
        os.makedirs(SUMMARY_DIR)

    # log_path need to fix

    log_path = LOG_FILE + '_'+tracename+'_Pensieve_'+str(NUM_AGENT)+'_' + str(m_id)
    log_file = open(log_path, 'wb')

    with tf.Session() as sess:

        actor = a3c.ActorNetwork(sess,
                                 state_dim=[S_INFO, NUM_AGENT*2], action_dim=A_DIM,
                                 learning_rate=ACTOR_LR_RATE,s_len=S_LEN)

        critic = a3c.CriticNetwork(sess,
                                   state_dim=[S_INFO, NUM_AGENT*2],
                                   learning_rate=CRITIC_LR_RATE,s_len=S_LEN)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()  # save neural net parameters

        # restore neural net parameters
        nn_model = NN_MODEL
        if nn_model is not None:  # nn_model is the path to file
            saver.restore(sess, nn_model)
            print("Model restored.")

        time_stamp = 0

        last_bit_rate = DEFAULT_QUALITY
        bit_rate = DEFAULT_QUALITY

        action_vec = np.zeros(A_DIM)
        action_vec[bit_rate] = 1

        s_batch = [np.zeros((S_INFO, NUM_AGENT*2))]
        a_batch = [action_vec]
        r_batch = []
        entropy_record = []

        video_count = 0

        delay_file = open(DATA_PATH + '/lastdownloadtime' + str(m_id))
        #sleep_file = open(DATA_PATH + '/rebufftime0')
        buffer_size_file = open(DATA_PATH + '/buffer' + str(m_id))
        rebuf_file = open(DATA_PATH + '/rebufftime' + str(m_id))
        video_chunk_size_file = open(DATA_PATH + '/chunk_size' + str(m_id))
        video_chunk_remain_file = open(DATA_PATH + '/m_segmentleft' + str(m_id))
        time_file = open(DATA_PATH + '/time' + str(m_id))

        currChunk=0
        
        while currChunk!=allvideochunk:  # serve video forever
            # the action is from the last decision
            # this is to make the framework similar to the real
            with open(DATA_PATH + '/permission' + str(m_id)) as enable:
                key = enable.read()
                if key == '1':

                    currChunk+=1


                    output_file = open(DATA_PATH + '/predict' + str(m_id),'a')
                    file_permission = open(DATA_PATH + '/permission' + str(m_id),'a')
                    
                    delay = delay_file.readline().split('\n')[0]
                    delay = float(delay)*1000#in ms
                    
                    sleep_time = 0.0#float(sleep_file.readline().split('\n')[0])
                    
                    buffer_size = float(buffer_size_file.readline().split('\n')[0])
                    buffer_size = max(buffer_size,0)
                    

                    rebuf = float(rebuf_file.readline().split('\n')[0])
                    
                    video_chunk_size = float(video_chunk_size_file.readline().split('\n')[0])
                    
                    next_video_chunk_sizes = np.multiply(VIDEO_BIT_RATE, 500)
                    
                    video_chunk_remain = float(video_chunk_remain_file.readline().split('\n')[0])
                    currTime = time_file.readline().split('\n')[0]
                    
                    if video_chunk_remain == 0:
                        end_of_video = 1
                    else:
                        end_of_video = 0

                    time_stamp += delay  # in ms
                    time_stamp += sleep_time  # in ms

                    # reward is video quality - rebuffer penalty - smoothness
                    # reward = VIDEO_BIT_RATE[bit_rate] / M_IN_K \
                    #          - REBUF_PENALTY * rebuf \
                    #          - SMOOTH_PENALTY * np.abs(VIDEO_BIT_RATE[bit_rate] -
                    #                                    VIDEO_BIT_RATE[last_bit_rate]) / M_IN_K



                    reward = VIDEO_BIT_RATE[bit_rate] / M_IN_K \
                            - REBUF_PENALTY * rebuf \
                            - SMOOTH_PENALTY * np.abs(VIDEO_BIT_RATE[bit_rate] -
                                               VIDEO_BIT_RATE[last_bit_rate]) / M_IN_K \
                            - 13*np.std([shareData[i*2+1]*4.3 for i in range(len(shareData)/2)]) \
                            - np.mean([shareData[i*2]*10 for i in range(len(shareData)/2) if i != m_id])


                    r_batch.append(reward)

                    last_bit_rate = bit_rate

                    # log time_stamp, bit_rate, buffer_size, reward
                    #log_file.write(str(time_stamp / M_IN_K) + '\t' +
                    #               str(VIDEO_BIT_RATE[bit_rate]) + '\t' +
                    #               str(buffer_size) + '\t' +
                    #               str(rebuf) + '\t' +
                    #               str(video_chunk_size) + '\t' +
                    #               str(delay) + '\t' +
                    #               str(reward) + '\n')
                    #log_file.flush()
                    # log time_stamp, bit_rate, buffer_size, reward
                    log_file.write(str(currTime) + '\t' +
                                   str(VIDEO_BIT_RATE[bit_rate]*1000) + '\t' +
                                   str(buffer_size) + '\t' +
                                   str(rebuf) + '\t' +
                                   str(int(video_chunk_size)) + '\t' +
                                   str(delay) + '\t' +
                                   str(reward) + '\n')
                    log_file.flush()


                    # retrieve previous state
                    if len(s_batch) == 0:
                        state = [np.zeros((S_INFO, NUM_AGENT*2))]
                    else:
                        state = np.array(s_batch[-1], copy=True)

                    # dequeue history record
                    state = np.roll(state, -1, axis=1)

                    # this should be S_INFO number of terms
                    state[0, -1] = VIDEO_BIT_RATE[bit_rate] / float(np.max(VIDEO_BIT_RATE))  # last quality
                    state[1, -1] = buffer_size / BUFFER_NORM_FACTOR  # 10 sec
                    state[2, -1] = float(video_chunk_size) / float(delay) / M_IN_K  # kilo byte / ms
                    state[3, -1] = float(delay) / M_IN_K / BUFFER_NORM_FACTOR  # 10 sec
                    state[4, :A_DIM] = np.array(next_video_chunk_sizes) / M_IN_K / M_IN_K  # mega byte
                    state[5, -1] = np.minimum(video_chunk_remain, CHUNK_TIL_VIDEO_END_CAP) / float(CHUNK_TIL_VIDEO_END_CAP)

                    shareData[m_id*2] = rebuf /BUFFER_NORM_FACTOR
                    shareData[m_id*2+1] = VIDEO_BIT_RATE[bit_rate] / float(np.max(VIDEO_BIT_RATE))
                    state[6, :] = shareData[:]

                    action_prob = actor.predict(np.reshape(state, (1, S_INFO, NUM_AGENT*2)))
                    action_cumsum = np.cumsum(action_prob)
                    bit_rate = (action_cumsum > np.random.randint(1, RAND_RANGE) / float(RAND_RANGE)).argmax()
                    
                    output_file.write(str(VIDEO_BIT_RATE[int(bit_rate)]*1000)+'\n')
                    file_permission.write('0\n')
                    output_file.close()
                    file_permission.close()
                    # Note: we need to discretize the probability into 1/RAND_RANGE steps,
                    # because there is an intrinsic discrepancy in passing single state and batch states

                    s_batch.append(state)

                    entropy_record.append(a3c.compute_entropy(action_prob[0]))

                    

                    if end_of_video:
                        #log_file.write('\n')

                        #log_file.close()

                        last_bit_rate = DEFAULT_QUALITY
                        bit_rate = DEFAULT_QUALITY  # use the default action here

                        del s_batch[:]
                        del a_batch[:]
                        del r_batch[:]

                        action_vec = np.zeros(A_DIM)
                        action_vec[bit_rate] = 1

                        s_batch.append(np.zeros((S_INFO, NUM_AGENT*2)))
                        a_batch.append(action_vec)
                        entropy_record = []

                        print "video count", video_count
                        video_count += 1

                        '''
                        log_path = LOG_FILE + '_sim_mul_' + str(m_id) + '_' + str(video_count)
                        log_file = open(log_path, 'wb')
                        '''

if __name__ == '__main__':
    users=NUM_AGENT
    tracename=sys.argv[1]
    allvideochunk=int(sys.argv[2])
    clients = []
    shareMemory=mp.Array('f',NUM_AGENT*2)
    for t in xrange(users):
        clients.append(mp.Process(target=main,args = (t,shareMemory,tracename,allvideochunk,)))
    for t in xrange(users):
        clients[t].start()
    for t in xrange(users):
        clients[t].join()

    
