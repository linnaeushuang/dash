/*
 * mpcfast-client.h
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#ifndef MPCfast_CLIENT_H_
#define MPCfast_CLIENT_H_

#include <ns3/dash-client.h>
namespace ns3
{

  class MpcfastClient : public DashClient
  {
  public:
    static TypeId
    GetTypeId(void);

    MpcfastClient();

    virtual
    ~MpcfastClient();

    virtual void
    CalcNextSegment(uint32_t currRate, uint32_t & nextRate, Time & delay, 
      Time m_segmentFetchTime, int id, Time currDt);

  private:
    bool
    BufferInc();

  };

} /* namespace ns3 */

#endif /* MPCFAST_CLIENT_H_ */
