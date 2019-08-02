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
#include <string>
std::string TRACE_NAME_BB="null";
int USERS_BB=0;


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
      Time & delay, Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId)
  {



	  double bufferLevel = currDt.GetSeconds();
	  double nowtime=Simulator::Now().GetSeconds();
	  double lastdownloadtime=m_segmentFetchTime.GetSeconds();
	  double rebuf=std::max(lastdownloadtime-lastbuffer,0.0);
	  uint32_t chunk_size=(currRate/8)*4;
	  lastbuffer=bufferLevel;
	  if(bufferLevel < RESEVOIR){
		  nextRate=bitRate[0];
	  }
	  else if(bufferLevel >= RESEVOIR + CUSHION){
		  nextRate=bitRate[5];
	  }
	  else{
		  int index=(int)(5*(bufferLevel-RESEVOIR)/CUSHION);
		  nextRate=bitRate[std::max(index,0)];
	  }
	  //}
	  double rateDiff=currRate>=lastRate?currRate-lastRate:lastRate-currRate;
	  lastRate=currRate;
	  double reward=currRate/1000000.0-rebufPenalty*rebuf-smoothPenalty*rateDiff/1000000.0;
	if(log_output.is_open()){
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<" "<<std::endl;
	  }
	  else{
		log_output.open("./src/dash/model/algorithms/results/log_"+TRACE_NAME_BB.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_BB)+"_"+std::to_string(id));
		s_real_buffer_output.open("./src/dash/model/algorithms/results/realbuffer_"+TRACE_NAME_BB.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_BB)+"_"+std::to_string(id));
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<" "<<std::endl;
	  }
  }


} /* namespace ns3 */
