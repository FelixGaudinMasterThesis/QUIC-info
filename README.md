# QUIC-info

## Fixed Parameters

- **RTO** The Retransmission Time-Out is the time in milliseconds before sending a packet again. 
- **ATO** The Acknowledgement Time-Out is the time in milliseconds before sending an acknowledgement again.
- **Snd-MSS** The Sender Maximum-Segment-Size is the maximum size in bytes used by the sender.
- **Rcv-MSS** The Receiver Maximum-Segment-Size is the maximum size in bytes used by the receiver.

## Timing

- **Last-data-sent** This is the timestamp (in ms) of the last packet sent that contains a data frame.
- **Last-ack-sent** This is the timestamp (in ms) of the last packet sent that contains an acknowledgement frame.
- **Last-data-recv** This is the timestamp (in ms) of the last packet received that contains a data frame.
- **Last-ack-recv** This is the timestamp (in ms) of the last packet received that contains an acknowledgement frame.
- **Min-rtt** This is the lowest time in milliseconds taken to perform a Round-Trip.
- **Smooth-rtt** This is the smoothed time in milliseconds taken to perform a Round-Trip.
- **Var-rtt** This is the variance of all Round-Trip Times.
- **Max-rtt** This is the highest time in milliseconds taken to perform a Round-Trip.

## Data exchanged

- **Bytes-sent** This is the total number of bytes sent on top of the UDP layer. This includes retransmission.
- **Bytes-recv** This is the total number of bytes received on top of the UDP layer.
- **Frames-sent** This is the total number of QUIC frames sent. 
- **Frames-recv** This is the total number of QUIC frames received. 
- **Data-frames-sent** This is the total number of QUIC data frames sent. 
- **Data-frames-recv** This is the total number of QUIC data frames received. 
- **Dgrams-sent** This is the number of UDP datagrams sent. 
- **Dgrams-recv** This is the number of UDP datagrams received. 
- **Data-dgrams-sent** This is the number of UDP datagrams sent that contain a data frame. 
- **Data-dgrams-recv** This is the number of UDP datagrams received that contain a data frame. 
- **Data-sent** This is the number of bytes sent in the QUIC frames without including retransmissions.
- **Data-recv**  This is the number of bytes received in the QUIC frames without including retransmissions.

## Others

- **Lost** This is the number of lost events.
- **Retrans** This is the number of frames retransmitted. 
- **Pacing-rate** This is the current Pacing Rate seen (in bytes per second).
- **Max-pacing-rate** This is the highest Pacing Rate used during the transfer (in bytes per second).
- **Delivery-rate** This is the global estimation of sending rate (in bytes per second).
- **Cwnd** This is the current size of the congestion window in bytes.
- **Next-send-pkt-nbr** This is the number of the next packet that will be sent. 
- **Next-recv-pkt-nbr** This is the number of the next packet that will be received.
- **Duration** This is the total time elapsed.
- **Spurious** This is the number of spurious retransmission.  