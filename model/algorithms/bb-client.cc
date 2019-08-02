/*
 * bb-client.cc
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#include "bb-client.h"
#include <ns3/log.h>
#include <ns3/simulator.h>
#include <ns3/dash-client.h>


NS_LOG_COMPONENT_DEFINE("BbClient");

namespace ns3
{
  NS_OBJECT_ENSURE_REGISTERED(BbClient);

  TypeId
  BbClient::GetTypeId(void)
  {
    static TypeId tid =
        TypeId("ns3::BbClient").SetParent<DashClient>().AddConstructor<
            BbClient>();
    return tid;
  }

  BbClient::BbClient()
  {
    // TODO Auto-generated constructor stub

  }

  BbClient::~BbClient()
  {
    // TODO Auto-generated destructor stub
  }

  void
  BbClient::CalcNextSegment(uint32_t currRate, uint32_t & nextRate,
      Time & delay, Time m_segmentFetchTime, int id, Time currDt)
  {

    //double rebufftime = std::max(m_segmentFetchTime.GetSeconds() - 4.0, 0.0);
	//this rebufftime is error?
	

	double rebufftime = std::max(m_segmentFetchTime.GetSeconds()-currDt.GetSeconds(),0.0);
    //double currDt = GetBufferEstimate();//bufferlevel is estimated
    std::ifstream predict_input;
    std::ifstream contiornot;
    char flag[4];
	
    rebufftime_output<<rebufftime<<std::endl;
    buffer_output<<currDt.GetSeconds()<<std::endl;
    lastdownloadtime<<m_segmentFetchTime.GetSeconds()<<std::endl;
    currRate_output<<currRate<<std::endl;
    chunk_size<<currRate/8*4<<std::endl;
	time_output<<Simulator::Now().GetSeconds()<<std::endl;
    
    permission.open("./src/dash/model/algorithms/data/permission"+std::to_string(id));
    permission<<1;
    permission.close();

    
    while(1)
      {
        contiornot.open("./src/dash/model/algorithms/data/permission"+std::to_string(id));
        contiornot >> flag;
        if (flag[1]=='0')
        {
          break;
        }
        contiornot.close();
      }
    

    predict_input.open("./src/dash/model/algorithms/data/predict"+std::to_string(id));
    while(!predict_input.eof())
    {
      predict_input >> nextRate;
    }
    predict_input.close();


    
    NS_LOG_INFO(
        "currDt: " << currDt);


    NS_LOG_INFO(currRate);

    /*result = result > 100000 ? result : 100000;
     result = result < 400000 ? result : 400000;*/

  }

} /* namespace ns3 */
