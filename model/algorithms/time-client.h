/*
 * time-client.h
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#ifndef TIME_CLIENT_H_
#define TIME_CLIENT_H_

#include <ns3/dash-client.h>
namespace ns3
{

  class TimeClient : public DashClient
  {
  public:
    static TypeId
    GetTypeId(void);

    TimeClient();

    virtual
    ~TimeClient();

    virtual void
    CalcNextSegment(uint32_t currRate, uint32_t & nextRate, Time & delay, 
      Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId);

  private:
    bool
    BufferInc();

  };

} /* namespace ns3 */

#endif /* TIME_CLIENT_H_ */
