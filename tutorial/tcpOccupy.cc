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


using namespace ns3;

NS_LOG_COMPONENT_DEFINE("TCPoccupy");


void throghPutPerSec(Ptr<Application> sinkapp,uint32_t nodeid,uint32_t lastTP){
	Ptr<PacketSink> sink = DynamicCast<PacketSink> (sinkapp);
	double throghPut = sink->GetTotalRx()-lastTP;
	std::cout<<Simulator::Now().GetSeconds()<<" "<<nodeid<<" "<<throghPut<<std::endl;


	//(3)test output,output is ok,but multiple user is error
	//std::cout<<"node"<<nodeid<<std::endl;

	
	Simulator::Schedule(Seconds(1.0),&throghPutPerSec,sinkapp,nodeid,sink->GetTotalRx());
}

int main(int argc,char *argv[]){

	// users=7,same time setup ,will no work
	// but different time setup.will work
	uint32_t maxBytes = 100;
	uint32_t users = 1;
	double stopTime = 128.0;
	uint32_t seed=3;
	std::string traceName = "None";
	std::string linkRate = "500Kbps";
	std::string delay = "5ms";
	double intervalStep=0.0;

	CommandLine cmd;
	cmd.AddValue("maxBytes", "Total number of bytes for application to send",
	    maxBytes);
	cmd.AddValue("users", "The number of concurrent videos", users);
	cmd.AddValue("stopTime",
	    "The time when the clients will stop requesting segments", stopTime);
	cmd.AddValue("linkRate",
	    "The bitrate of the link connecting the clients to the server (e.g. 500kbps)",
	    linkRate);
	cmd.AddValue("delay",
	    "The delay of the link connecting the clients to the server (e.g. 5ms)",
	    delay);
	cmd.AddValue("intervalStep",
	    "The step of interval for each user",intervalStep);
	cmd.AddValue("traceName",
	    "The trace file name,it will load until the stopTime",traceName);
	cmd.AddValue("randomSeed",
	    "The seed of global random",seed);
	
	
	cmd.Parse(argc, argv);

	//RngSeedManager::SetSeed(seed);

	NodeContainer nodes;
	nodes.Create(2);

	PointToPointHelper pointToPoint;
	pointToPoint.SetDeviceAttribute("DataRate", StringValue(linkRate));
	pointToPoint.SetChannelAttribute("Delay", StringValue(delay));
	NetDeviceContainer devices;
	devices = pointToPoint.Install(nodes);

	InternetStackHelper internet;
	internet.Install(nodes);


	NS_LOG_INFO("Assign IP Addresses.");
	Ipv4AddressHelper ipv4;
	ipv4.SetBase("10.1.1.0", "255.255.255.0");
	Ipv4InterfaceContainer i = ipv4.Assign(devices);


	double startInterval=0.0;
	uint16_t port=800;

	for(uint32_t n=0;n<users;n++,startInterval+=intervalStep){
		BulkSendHelper source("ns3::TcpSocketFactory",InetSocketAddress(i.GetAddress(1),port+n));
		source.SetAttribute("MaxBytes",UintegerValue(0));
		ApplicationContainer sourceApp=source.Install(nodes.Get(0));

		sourceApp.Start(Seconds(0.25+startInterval));
		sourceApp.Stop(Seconds(stopTime));


		PacketSinkHelper sink("ns3::TcpSocketFactory",InetSocketAddress(Ipv4Address::GetAny(),port+n));
		ApplicationContainer sinkApp=sink.Install(nodes.Get(1));

		//Ptr<PacketSink> paramSink=DynamicCast<PacketSink> (sinkApp.Get(1))
		sinkApp.Start(Seconds(0.0));
		sinkApp.Stop(Seconds(stopTime+5.0));

		//(1)here , this call function is error
		//(2)function is error,call is ok
		//(4)multiple user,no call this function is ok
		//(5)change sinkApp.Get(1) to sinkApp.Get(0) will work,multiple users also work
		Simulator::Schedule(Seconds(1.0),&throghPutPerSec,sinkApp.Get(0),n,0);
	}
	Simulator::Stop(Seconds(stopTime+5.0));
	Simulator::Run();
	Simulator::Destroy();
	return 0;

}
