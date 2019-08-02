/*
 * pensieve-client.cc
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#include "time-client.h"
#include <ns3/log.h>
#include <ns3/simulator.h>
#include <ns3/dash-client.h>

#include <iostream>

NS_LOG_COMPONENT_DEFINE("TimeClient");

namespace ns3
{
  NS_OBJECT_ENSURE_REGISTERED(TimeClient);

  TypeId
  TimeClient::GetTypeId(void)
  {
    static TypeId tid =
        TypeId("ns3::TimeClient").SetParent<DashClient>().AddConstructor<
            TimeClient>();
    return tid;
  }

  TimeClient::TimeClient()
  {
    // TODO Auto-generated constructor stub

  }

  TimeClient::~TimeClient()
  {
    // TODO Auto-generated destructor stub
  }

  void
  TimeClient::CalcNextSegment(uint32_t currRate, uint32_t & nextRate,
      Time & delay, Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId)
  {

    std::ifstream predict_input;
    
    predict_input.open("./src/dash/model/algorithms/data/predict"+std::to_string(id));
    while(!predict_input.eof())
    {
		//std::cout<<nextRate<<std::endl;
		predict_input>>nextRate;
    }
    predict_input.close();
	//nextRate=1000;


    
    NS_LOG_INFO(
        "currDt: " << currDt);


    NS_LOG_INFO(currRate);

    /*result = result > 100000 ? result : 100000;
     result = result < 400000 ? result : 400000;*/

  }

} /* namespace ns3 */
