/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2014 TEI of Western Macedonia, Greece
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 * Author: Dimitrios J. Vergados <djvergad@gmail.com>
 */

// Network topology
//
//       n0 ----------- n1
//            500 Kbps
//             5 ms
//
#include <string>
#include <fstream>
#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/network-module.h"
#include "ns3/dash-module.h"

#include "../model/algorithms/dash-param.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("DashExample");



void BandwidthTrace(float inputBW,uint32_t usersNum){
	//-------------------------------------------------
	//input unit is Mbps
	//I want to user int bandwidth in Kbps;
	//give every user same bandwidth
	//for example,3 user 0.8Mbps BW
	//I will give 3*800Kbps BW
	//-------------------------------------------------
	

	std::string bandUnit="Kbps";
	inputBW=inputBW*1000*usersNum;

	//need to support c++11 standard
	std::string  bandwidth = std::to_string((int)inputBW)+bandUnit;
	//fortunatly



	Config::Set("/NodeList/1/DeviceList/0/$ns3::PointToPointNetDevice/DataRate",StringValue(bandwidth));



	//change the client port bandwidth,but it is not work
	Config::Set("/NodeList/0/DeviceList/0/$ns3::PointToPointNetDevice/DataRate",StringValue(bandwidth));
	//only change the server port bandwidth.it will work
	//server is in the 1th node,client is in 0th node
	//Config::Set("/NodeList/1/DeviceList/0/$ns3::PointToPointNetDevice/DataRate",StringValue("100Kbps"));
}

int
main(int argc, char *argv[])
{
  bool tracing = false;
  uint32_t maxBytes = 100;
  uint32_t users = 1;
  double target_dt = 35.0;


  double stopTime = 1024.0;
  double startTime = 0.0;

  uint32_t seed=1;
  std::string traceName = "None";


  std::string linkRate = "500Kbps";
  std::string delay = "5ms";
  std::string protocol = "ns3::DashClient";
  std::string window = "10s";

  uint32_t numChunk=48;


  double intervalStep=0.0;

  /*  LogComponentEnable("MpegPlayer", LOG_LEVEL_ALL);*/
  /*LogComponentEnable ("DashServer", LOG_LEVEL_ALL);
   LogComponentEnable ("DashClient", LOG_LEVEL_ALL);*/

//
// Allow the user to override any of the defaults at
// run-time, via command-line arguments
//
  CommandLine cmd;
  cmd.AddValue("tracing", "Flag to enable/disable tracing", tracing);
  cmd.AddValue("maxBytes", "Total number of bytes for application to send",
      maxBytes);
  cmd.AddValue("users", "The number of concurrent videos", users);
  cmd.AddValue("targetDt",
      "The target time difference between receiving and playing a frame.",
      target_dt);
  cmd.AddValue("stopTime",
      "The time when the clients will stop requesting segments", stopTime);
  cmd.AddValue("linkRate",
      "The bitrate of the link connecting the clients to the server (e.g. 500kbps)",
      linkRate);
  cmd.AddValue("delay",
      "The delay of the link connecting the clients to the server (e.g. 5ms)",
      delay);
  cmd.AddValue("protocol",
      "The adaptation protocol. It can be 'ns3::DashClient' or 'ns3::OsmpClient (for now).",
      protocol);
  cmd.AddValue("window",
      "The window for measuring the average throughput (Time).", window);

  cmd.AddValue("intervalStep",
	  "The step of interval for each user",intervalStep);
  cmd.AddValue("traceName",
	  "The trace file name,it will load until the stopTime",traceName);
  cmd.AddValue("randomSeed",
	  "The seed of global random",seed);
  cmd.AddValue("startTime",
	  "The time of client start",startTime);
  cmd.AddValue("numChunk",
	  "The number of chunk in video",numChunk);


  cmd.Parse(argc, argv);

  RngSeedManager::SetSeed(seed);

//
// Explicitly create the nodes required by the topology (shown above).
//
  NS_LOG_INFO("Create nodes.");
  NodeContainer nodes;
  nodes.Create(2);

  NS_LOG_INFO("Create channels.");

//
// Explicitly create the point-to-point link required by the topology (shown above).
//
  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute("DataRate", StringValue(linkRate));
  pointToPoint.SetChannelAttribute("Delay", StringValue(delay));
  NetDeviceContainer devices;
  devices = pointToPoint.Install(nodes);

//
// Install the internet stack on the nodes
//
  InternetStackHelper internet;
  internet.Install(nodes);

//
// We've got the "hardware" in place.  Now we need to add IP addresses.
//
  NS_LOG_INFO("Assign IP Addresses.");
  Ipv4AddressHelper ipv4;
  ipv4.SetBase("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i = ipv4.Assign(devices);

  NS_LOG_INFO("Create Applications.");

  std::vector<std::string> protocols;
  std::stringstream ss(protocol);
  std::string proto;
  uint32_t protoNum = 0; // The number of protocols (algorithms)
  while (std::getline(ss, proto, ',') && protoNum++ < users)
    {
      protocols.push_back(proto);
    }

  uint16_t port = 80;  // well-known echo port number
  std::vector<DashClientHelper> clients;
  std::vector<ApplicationContainer> clientApps;

  //---------------------------------set the dynamic bandwidth----------------------------------------------------------
  //
  //user traceName to set the location where the trace read from
  //
  //also,it will read the trace until the trace time greater then stop time
  //
  //Author:huang lin <oliverHLin@163.com>
  //sent email if any problem
  //
  //--------------------------------------------------------------------------------------------------------------------
  

  USERS_BB=users;
  USERS_MPC=users;
  USERS_MPCFAST=users;
  
  if(traceName!="None"){
    TRACE_NAME_BB=traceName;
    TRACE_NAME_MPC=traceName;
    TRACE_NAME_MPCFAST=traceName;

  	std::string tracePATH = "./src/dash/model/algorithms/test_sim_traces/";
  	tracePATH = tracePATH + traceName;
  	std::ifstream traceFile(tracePATH);
  	std::string traceTime,traceBandWidth;
	float timeToSet,bandToSet,cycleTime=0.0;
	if(traceFile){
		traceFile >> traceTime;
		traceFile >> traceBandWidth;
		do{
			//atof may need stdlib.h
			timeToSet=atof(traceTime.c_str());
			bandToSet=atof(traceBandWidth.c_str());
			Simulator::Schedule(Seconds(timeToSet+cycleTime),BandwidthTrace,bandToSet,users);
			traceFile >> traceTime;
			traceFile >> traceBandWidth;
			if(traceFile.eof()){
				cycleTime+=timeToSet;
				traceFile.clear();
				traceFile.seekg(0,std::ios::beg);
				traceFile >> traceTime;
				traceFile >> traceBandWidth;
			}

		}while(atof(traceTime.c_str())+cycleTime<stopTime);
  	}
	traceFile.close();
  }
  else{
    TRACE_NAME_BB="norway_none";
    TRACE_NAME_MPC="norway_none";
    TRACE_NAME_MPCFAST="norway_none";


  }


  //in 120sec call BandwidthTrace,and use 10 to the function BWT input
  //Simulator::Schedule(Seconds(120.0),BandwidthTrace,10);



  //
  //--------------------setSupplement----
  
/*
  for(double stime=0.5;stime<stopTime;stime+=1){
	  Simulator::Schedule(Seconds(stime),setSupplement,stime,m_player.GetRealPlayTime(mpegHeader.GetPlaybackTime()));
  }

*/




  //--------------------------------------------------------------------------------------------------------------------
  double startInerval=0.0;
  for (uint32_t user = 0; user < users; user++,startInerval+=intervalStep)
    {
      DashClientHelper client("ns3::TcpSocketFactory",
          InetSocketAddress(i.GetAddress(1), port), protocols[user % protoNum]);
      //client.SetAttribute ("MaxBytes", UintegerValue (maxBytes));
      client.SetAttribute("VideoId", UintegerValue(user + 1)); // VideoId should positive
      client.SetAttribute("TargetDt", TimeValue(Seconds(target_dt)));
      client.SetAttribute("window", TimeValue(Time(window)));
	  client.SetAttribute("NumberChunk",UintegerValue(numChunk));
      ApplicationContainer clientApp = client.Install(nodes.Get(0));
      clientApp.Start(Seconds(startTime+0.25+startInerval));
      clientApp.Stop(Seconds(stopTime));

      clients.push_back(client);
      clientApps.push_back(clientApp);

    }

  DashServerHelper server("ns3::TcpSocketFactory",
      InetSocketAddress(Ipv4Address::GetAny(), port));
  ApplicationContainer serverApps = server.Install(nodes.Get(1));
  serverApps.Start(Seconds(0.0));
  serverApps.Stop(Seconds(stopTime + 5.0));

//
// Set up tracing if enabled
//
  if (tracing)
    {
      AsciiTraceHelper ascii;
      pointToPoint.EnableAsciiAll(ascii.CreateFileStream("dash-send.tr"));
      pointToPoint.EnablePcapAll("dash-send", false);
    }

//
// Now, do the actual simulation.
//
  NS_LOG_INFO("Run Simulation.");
  /*Simulator::Stop(Seconds(100.0));*/
  Simulator::Run();
  Simulator::Destroy();
  NS_LOG_INFO("Done.");

  uint32_t k;
  for (k = 0; k < users; k++)
    {
      Ptr<DashClient> app = DynamicCast<DashClient>(clientApps[k].Get(0));
      std::cout << protocols[k % protoNum] << "-Node: " << k;
      app->GetStats();
    }

  return 0;

}
