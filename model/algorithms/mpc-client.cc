/*
 * mpc-client.cc
 *
 *  Created on: Jun 16, 2014
 *      Author: dimitriv
 */

#include "mpc-client.h"
#include <ns3/log.h>
#include <ns3/simulator.h>
#include <ns3/dash-client.h>
#include <string>
std::string TRACE_NAME_MPC="null";
int USERS_MPC=0;



NS_LOG_COMPONENT_DEFINE("MpcClient");

namespace ns3
{
  NS_OBJECT_ENSURE_REGISTERED(MpcClient);

  TypeId
  MpcClient::GetTypeId(void)
  {
    static TypeId tid =
        TypeId("ns3::MpcClient").SetParent<DashClient>().AddConstructor<
            MpcClient>();
    return tid;
  }

  MpcClient::MpcClient()
  {
    // TODO Auto-generated constructor stub

  }

  MpcClient::~MpcClient()
  {
    // TODO Auto-generated destructor stub
  }

  void
  MpcClient::CalcNextSegment(uint32_t currRate, uint32_t & nextRate,
      Time & delay, Time m_segmentFetchTime, int id, Time currDt,uint32_t m_segmentId)
  {
	  double bufferLevel=currDt.GetSeconds();
	  double nowtime=Simulator::Now().GetSeconds();
	  double lastdownloadtime=m_segmentFetchTime.GetSeconds();
	  double rebuf=std::max(lastdownloadtime-lastbuffer,0.0);
	  uint32_t chunk_size=(currRate/8)*4;
	  lastbuffer=bufferLevel;

	  if(mpcPBlen>=5){
		  mpcPBfront++;
		  mpcPastBandwidth[(mpcPBfront+mpcPBlen-1)%5]=currRate/(2000000*lastdownloadtime);
	  }
	  else{
		  mpcPBlen++;
		  mpcPastBandwidth[(mpcPBfront+mpcPBlen-1)%5]=currRate/(2000000*lastdownloadtime);
	  }
	double currError=0.0;
	if(mpcPBElen>0){
		currError = std::abs(mpcPastBandwidthEsts[(mpcPBEfront+mpcPBElen-1)%5]-mpcPastBandwidth[(mpcPBfront+mpcPBlen-1)%5])/mpcPastBandwidth[(mpcPBfront+mpcPBlen-1)%5];
	}
	if(mpcPBERlen>=5){
		mpcPBERfront++;
		mpcPastBandwidthEstsError[(mpcPBERfront+mpcPBERlen-1)%5]=currError;
	}
	else{
		mpcPBERlen++;
		mpcPastBandwidthEstsError[(mpcPBERfront+mpcPBERlen-1)%5]=currError;

	}
	double bandwidthSum=0.0;
	for(int i=0;i<mpcPBlen;i++)
		bandwidthSum += (1.0 / mpcPastBandwidth[(mpcPBfront+i)%5]);
	double harmonicBandwidth = (mpcPBlen/bandwidthSum);
	double maxError=0;
	for(int i=0;i<mpcPBERlen;i++)
		if(maxError<mpcPastBandwidthEstsError[(mpcPBERfront+i)%5])
			maxError=mpcPastBandwidthEstsError[(mpcPBERfront+i)%5];
	double futureBandwidth = harmonicBandwidth/(1.0+maxError);
	if(mpcPBElen>=5){
		mpcPBEfront++;
		mpcPastBandwidthEsts[(mpcPBEfront+mpcPBElen-1)%5]=harmonicBandwidth;
	}
	else{
		mpcPBElen++;
		mpcPastBandwidthEsts[(mpcPBEfront+mpcPBElen-1)%5]=harmonicBandwidth;
	}

	//in last few chunk,we also ests 5 chunk;
	double maxQoe=-100000.0;
	int bestRateIndex=0;
	int futureList[5]={0,0,0,0,0};
	for(int b1=0;b1<6;b1++){
		futureList[0]=b1;
		for(int b2=0;b2<6;b2++){
			futureList[1]=b2;
			for(int b3=0;b3<6;b3++){
				futureList[2]=b2;
				for(int b4=0;b4<6;b4++){
					futureList[3]=b4;
					for(int b5=0;b5<6;b5++){
						futureList[4]=b5;
						double currRebufferTime=0.0;
						double bitRateSum=0.0;
						double smoothnessDiff=0.0;
						double currBuffer=bufferLevel;
						double QOE;
						int lastBitRate=currRate;
						for(int i=0;i<5;i++){
							double downloadTime=(bitRate[futureList[i]]/2000000.0)/futureBandwidth;
							if(currBuffer<downloadTime){
								currRebufferTime+=(downloadTime-currBuffer);
								currBuffer=0.0;
							}
							else
								currBuffer-=downloadTime;
							currBuffer+=4;
							bitRateSum+=bitRate[futureList[i]]/1000000.0;//unit is Mbps;
							smoothnessDiff+=std::abs(bitRate[futureList[i]]-lastBitRate)/1000000.0;
							lastBitRate=bitRate[futureList[i]];
						}
						QOE=bitRateSum-REBUF_PENALTY*currRebufferTime-smoothnessDiff;
						if(QOE>maxQoe){
							maxQoe=QOE;
							bestRateIndex=b1;

						}
					}
				}
			}
		}
	}
	nextRate=bitRate[bestRateIndex];
	double rateDiff=currRate>=lastRate?currRate-lastRate:lastRate-currRate;
	lastRate=currRate;
	double reward=currRate/1000000.0-rebufPenalty*rebuf-smoothPenalty*rateDiff/1000000.0;
	if(log_output.is_open()){
		//log_output<<Simulator::Now().GetSeconds()<<" "<<bufferLevel<<" "<<currRate<<" "<<m_segmentFetchTime.GetSeconds()<<std::endl;
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<std::endl;
	  }
	  else{
		log_output.open("./src/dash/model/algorithms/results/log_"+TRACE_NAME_MPC.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_MPC)+"_"+std::to_string(id));
		s_real_buffer_output.open("./src/dash/model/algorithms/results/realbuffer_"+TRACE_NAME_MPC.substr(7)+"_"+GetTypeId().GetName().substr(5,GetTypeId().GetName().length()-11)+"_"+std::to_string(USERS_MPC)+"_"+std::to_string(id));
		//log_output<<Simulator::Now().GetSeconds()<<" "<<bufferLevel<<" "<<currRate<<" "<<m_segmentFetchTime.GetSeconds()<<std::endl;
		log_output<<nowtime<<" "<<currRate<<" "<<bufferLevel<<" "<<rebuf<<" "<<chunk_size<<" "<<lastdownloadtime<<" "<<reward<<std::endl;

	  }
  }

} /* namespace ns3 */
