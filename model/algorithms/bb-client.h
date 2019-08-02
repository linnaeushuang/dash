/*
 * bb-client.h
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#ifndef BB_CLIENT_H_
#define BB_CLIENT_H_

#include <ns3/dash-client.h>
namespace ns3
{

  class BbClient : public DashClient
  {
  public:
    static TypeId
    GetTypeId(void);

    BbClient();

    virtual
    ~BbClient();

    virtual void
    CalcNextSegment(uint32_t currRate, uint32_t & nextRate, Time & delay, 
      Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId);


	/*
    virtual void
    StartApplication(void);    // Called at time specified by Start
    virtual void
    StopApplication(void);     // Called at time specified by Stop
	*/

  private:
    bool
    BufferInc();

	double RESEVOIR = 7.0;
	double CUSHION = 21.0;
	int bitRate[6]={300000,750000,1200000,1850000,2850000,4300000};
	int fetchIndex=0;
	double rebufPenalty=4.3;
	double smoothPenalty=1.0;

  };

} /* namespace ns3 */

#endif /* BB_CLIENT_H_ */
