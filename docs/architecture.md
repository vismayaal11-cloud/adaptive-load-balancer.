# Adaptive Load Balancer — System Architecture

## 1. Problem Statement

A server can become overloaded when it receives more requests than it can handle efficiently. A traditional static load-balancing strategy may continue sending requests to an overloaded server.

This project aims to distribute client requests across two backend servers using an adaptive load-balancing approach, supported by Software-Defined Networking (SDN).

## 2. Project Objectives

- Accept requests from multiple TCP clients.
- Distribute requests across two backend servers.
- Monitor backend health and load.
- Adapt backend selection based on server conditions.
- Use an SDN controller to update network forwarding rules in response to relevant events.
- Demonstrate the system through testing and network-level evidence.

## 3. System Components

### 3.1 TCP Clients
Generate requests and communicate with the load balancer over TCP.

### 3.2 Load Balancer
Accepts client requests, evaluates backend availability and load, and selects an appropriate backend.

### 3.3 Backend Servers
Two independent TCP servers process requests and return responses.

- Backend 1: Port 9001
- Backend 2: Port 9002

### 3.4 SDN Controller
Receives relevant health or overload events and manages forwarding rules on the OpenFlow switch.

### 3.5 Mininet and OpenFlow Switch
Mininet provides the virtual network topology. The OpenFlow switch forwards network traffic according to rules installed or modified by the SDN controller.

## 4. Communication Flow

1. A client sends a TCP request to the load balancer on port 8000.
2. The load balancer evaluates backend health and estimated load.
3. It selects one of the two backend servers.
4. The selected server processes the request and sends a response.
5. The load balancer returns the response to the client.
6. When a relevant overload or health event occurs, the load balancer communicates that event to the SDN controller.
7. The controller may update the OpenFlow switch's forwarding rules.

## 5. Initial Port Plan

| Component | Port |
|---|---:|
| Load Balancer | 8000 |
| Backend Server 1 | 9001 |
| Backend Server 2 | 9002 |

These values are proposed and must be confirmed by the team.

## 6. Application-Level and Network-Level Decisions

**Application-level decision:** The load balancer selects which backend server receives a request.

**Network-level decision:** The SDN controller modifies forwarding rules on the OpenFlow switch.

Both mechanisms must be demonstrated separately during testing.

## 7. Proposed Technologies

- Python — application and server implementation
- TCP sockets — client-server communication
- Mininet — network emulation
- Open vSwitch — virtual OpenFlow switch
- SDN controller — controller implementation (to be confirmed by the team)

## 8. Implementation Status

Initial architecture documentation. Component interfaces, controller choice, network addressing, and forwarding policy are pending team confirmation.
