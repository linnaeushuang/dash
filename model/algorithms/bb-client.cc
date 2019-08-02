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
	  double rebuf=std::max(lastdownloadtime-4.0,0.0);
	  uint32_t chunk_size=(currRate/8)*4;
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
	  int rateDiff=currRate>=nextRate?currRate-nextRate:nextRate-currRate;
	  double reward=nextRate/1000000.0-rebufPenalty*rebuf-smoothPenalty*rateDiff/1000000.0;
	if(log_output.is_open()){
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<" "<<std::endl;
	  }
	  else{
		log_output.open("./src/dash/model/algorithms/results/log_"+TRACE_NAME_BB.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_BB)+"_"+std::to_string(id));
		s_real_buffer_output.open("./src/dash/model/algorithms/results/realbuffer_"+TRACE_NAME_BB.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_BB)+"_"+std::to_string(id));
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<" "<<std::endl;
	  }
  }


  /*
// Application Methods
  void
  BbClient::StartApplication(void) // Called at time specified by Start
  {
    NS_LOG_FUNCTION(this);
	std::cout<<"node"<<std::to_string(m_id)<<": "<<GetTypeId()<<std::endl;
    

	s_real_buffer_output.open("./src/dash/model/algorithms/data/realBuffer"+std::to_string(m_id));



    if (!m_socket)
      {

        m_socket = Socket::CreateSocket(GetNode(), m_tid);

        // Fatal error if socket type is not NS3_SOCK_STREAM or NS3_SOCK_SEQPACKET
        if (m_socket->GetSocketType() != Socket::NS3_SOCK_STREAM
            && m_socket->GetSocketType() != Socket::NS3_SOCK_SEQPACKET)
          {
            NS_FATAL_ERROR("Using HTTP with an incompatible socket type. "
                "HTTP requires SOCK_STREAM or SOCK_SEQPACKET. "
                "In other words, use TCP instead of UDP.");
          }

        if (Inet6SocketAddress::IsMatchingType(m_peer))
          {
            m_socket->Bind6();
          }
        else if (InetSocketAddress::IsMatchingType(m_peer))
          {
            m_socket->Bind();
          }

        m_socket->Connect(m_peer);
        m_socket->SetRecvCallback(MakeCallback(&DashClient::HandleRead, this));
        m_socket->SetConnectCallback(
            MakeCallback(&DashClient::ConnectionSucceeded, this),
            MakeCallback(&DashClient::ConnectionFailed, this));
        m_socket->SetSendCallback(MakeCallback(&DashClient::DataSend, this));
      }
  }

  void
  BbClient::StopApplication(void) // Called at time specified by Stop
  {
	  std::cout<<"dash stop"<<Simulator::Now().GetSeconds()<<std::endl;
    NS_LOG_FUNCTION(this);

	log_output.close();

    
	s_real_buffer_output<<s_lastTime + s_lastBuffer*0.02<<" "<<0.0<<std::endl;
	s_real_buffer_output.close();

    if (m_socket != 0)
      {
        m_socket->Close();
        m_connected = false;
        m_player.m_state = MPEG_PLAYER_DONE;
      }
    else
      {
        NS_LOG_WARN("DashClient found null socket to close in StopApplication");
      }
  }

  */


} /* namespace ns3 */
