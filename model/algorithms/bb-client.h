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
      Time m_segmentFetchTime, int id, Time currDt);

  private:
    bool
    BufferInc();

  };

} /* namespace ns3 */

#endif /* BB_CLIENT_H_ */
