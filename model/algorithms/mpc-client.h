/*
 * mpc-client.h
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#ifndef MPC_CLIENT_H_
#define MPC_CLIENT_H_

#include <ns3/dash-client.h>
namespace ns3
{

  class MpcClient : public DashClient
  {
  public:
    static TypeId
    GetTypeId(void);

    MpcClient();

    virtual
    ~MpcClient();

    virtual void
    CalcNextSegment(uint32_t currRate, uint32_t & nextRate, Time & delay, 
      Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId);

  private:
    bool
    BufferInc();


	int bitRate[6]={300000,750000,1200000,1850000,2850000,4300000};
	double mpcPastBandwidth[5]={0.0,0.0,0.0,0.0,0.0};
	double mpcPastBandwidthEsts[5]={0.0,0.0,0.0,0.0,0.0};
	double mpcPastBandwidthEstsError[5]={0.0,0.0,0.0,0.0,0.0};

	int mpcPBfront=0,mpcPBlen=0;
	int mpcPBEfront=0,mpcPBElen=0;
	int mpcPBERfront=0,mpcPBERlen=0;



	//front point to first non-empty value;
	//front+len point to after end non-empty value;

	double REBUF_PENALTY=4.3;
	double rebufPenalty=4.3;
	double smoothPenalty=1.0;
	double lastbuffer=4.0;
	double lastRate=300000;


  };

} /* namespace ns3 */

#endif /* MPC_CLIENT_H_ */
