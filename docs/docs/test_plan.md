# Adaptive Load Balancer — Test Plan

## 1. Objective

Verify that the adaptive load balancer distributes requests correctly, responds to backend health and load conditions, and integrates with the SDN controller and OpenFlow switch.

## 2. Test Environment

- Python-based TCP clients and servers
- Two backend servers
- TCP load balancer
- Mininet network topology
- OpenFlow switch
- SDN controller

Exact software versions and network addresses will be documented after environment setup.

## 3. Test Cases

| ID | Test | Expected Result |
|---|---|---|
| T1 | Network connectivity | Clients and backend hosts can communicate through the Mininet topology. |
| T2 | Basic TCP request | A client sends a request and receives a valid backend response. |
| T3 | Multiple clients | Concurrent client requests are handled successfully. |
| T4 | Backend distribution | Requests are distributed across the available backend servers. |
| T5 | Backend overload | The load balancer avoids or reduces requests to an overloaded backend. |
| T6 | Backend failure | Requests are redirected to a healthy backend when another backend becomes unavailable. |
| T7 | SDN event handling | The controller receives a health or overload event. |
| T8 | Flow-rule update | The controller changes the relevant OpenFlow switch rule in response to an event. |
| T9 | End-to-end integration | Application-level adaptation and network-level rule changes are demonstrated together. |

## 4. Evidence to Collect

- Client request and response logs.
- Backend server logs.
- Load-balancer backend-selection logs.
- Controller event logs.
- OpenFlow switch flow-table output before and after an event.
- Mininet connectivity test output.
- Test results and screenshots.

## 5. Pass Criteria

A test is marked PASS only when its expected behavior is observed and evidence is collected.

A feature that has not yet been implemented or tested must be marked NOT TESTED, not PASS.

## 6. Known Integration Considerations

- Application-level backend selection and network-level forwarding changes must be verified separately.
- Existing TCP connections do not automatically migrate when an OpenFlow rule changes.
- The controller event format and network forwarding policy must be agreed upon by the team.

## 7. Test Results

Results will be recorded after implementation and integration.

| Test ID | Status | Evidence / Notes |
|---|---|---|
| T1–T9 | NOT TESTED | Pending implementation |
