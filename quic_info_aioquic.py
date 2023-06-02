import json
from numpy import mean, var

def is_parameters_set(event):
    return event['name'] == "transport:parameters_set"

def is_packet_lost(event):
    return event['name'] == "recovery:packet_lost"

def is_packet_sent(event):
    return event['name'] == "transport:packet_sent"

def is_packet_received(event):
    return event['name'] == "transport:packet_received"

def is_metrics_updated(event):
    return event['name'] == "recovery:metrics_updated"

def is_datagrams_sent(event):
    return event['name'] == "transport:datagrams_sent"

def is_datagrams_received(event):
    return event['name'] == "transport:datagrams_received"

class Quic_info:
    def __init__(self, qlog_file, host_type=None):

        self.qlogs = None
        with open(qlog_file) as f:
            self.qlogs = json.load(f)

        self.host_type = host_type

    def _get_events(self):
        return self.qlogs["traces"][0]["events"]

    def get_RTO(self):
        for event in self._get_events():
            if is_parameters_set(event):
                if event['data']['owner'] == self.host_type and "idle_timeout" in event["data"]:
                    return event['data']['idle_timeout']

    def get_ATO(self):
        for event in self._get_events():
            if is_parameters_set(event):
                if event['data']['owner'] == self.host_type and "max_ack_delay" in event["data"]:
                    return event['data']['max_ack_delay']

    def get_snd_MSS(self):
        for event in self._get_events():
            if is_parameters_set(event):
                if event['data']['owner'] == "local":
                    return event['data']['initial_max_data']

    def get_rcv_MSS(self):
        for event in self._get_events():
            if is_parameters_set(event):
                if event['data']['owner'] == "remote":
                    return event['data']['initial_max_data']

    def get_lost(self):
        lost = 0
        for event in self._get_events():
            if is_packet_lost(event):
                lost += 1
        return lost
    
    def get_last_data_sent(self):
        for event in reversed(self._get_events()):
            if is_packet_sent(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        return event['time']

    def get_last_ack_sent(self):
        for event in reversed(self._get_events()):
            if is_packet_sent(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "ack":
                        return event['time']

    def get_last_data_recv(self):
        for event in reversed(self._get_events()):
            if is_packet_received(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        return event['time']

    def get_last_ack_recv(self):
        for event in reversed(self._get_events()):
            if is_packet_received(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "ack":
                        return event['time']

    def get_minrtt(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "min_rtt" in event["data"]:
                    return event["data"]["min_rtt"]

    def get_srtt(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "smoothed_rtt" in event["data"]:
                    return event["data"]["smoothed_rtt"]

    def get_varrtt(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "rtt_variance" in event["data"]:
                    return event["data"]["rtt_variance"]

    def get_latest_rtt(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "latest_rtt" in event["data"]:
                    return event["data"]["latest_rtt"]

    def get_pacing_rate(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "pacing_rate" in event["data"]:
                    return event["data"]["pacing_rate"]
    
    def get_max_pacing_rate(self):
        max_pacing_rate = 0
        for event in self._get_events():
            if is_metrics_updated(event) and "pacing_rate" in event["data"]:
                if event["data"]["pacing_rate"] > max_pacing_rate: 
                    max_pacing_rate = event["data"]["pacing_rate"]
        return max_pacing_rate

    def get_ssthresh(self):
        for event in reversed(self._get_events()):
            if is_metrics_updated(event):
                if "ssthresh" in event["data"]:
                    return event["data"]["ssthresh"]

    def get_delivery_rate(self):
        return self.get_bytes_sent()/self.get_connexion_duration()

    def get_bytes_sent(self):
        bytes_sent = 0
        for event in self._get_events():
            if is_datagrams_sent(event):
                for row in event["data"]["raw"]:
                    bytes_sent += row["length"]
        return bytes_sent

    def get_bytes_received(self):
        bytes_reveived = 0
        for event in self._get_events():
            if is_datagrams_received(event):
                for row in event["data"]["raw"]:
                    bytes_reveived += row["length"]
        return bytes_reveived

    def get_data_frames_sent(self):
        frames_sent = 0
        for event in self._get_events():
            if is_packet_sent(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        frames_sent += 1
        return frames_sent

    def get_data_frames_received(self):
        frames_received = 0
        for event in self._get_events():
            if is_packet_received(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        frames_received += 1
        return frames_received

    def get_cwnd(self):
        for event in self._get_events():
            if is_metrics_updated(event):
                if "congestion_window" in event["data"]:
                    return event["data"]["congestion_window"]

    def get_maxcwnd(self):
        max_cwnd = 0
        for event in self._get_events():
            if is_metrics_updated(event) and "congestion_window" in event["data"]:
                if event["data"]["congestion_window"] > max_cwnd:
                    max_cwnd = event["data"]["congestion_window"]
        return max_cwnd

    def get_datagram_sent(self):
        datagram_sent = 0
        for event in self._get_events():
            if is_datagrams_sent(event):
                datagram_sent += event["data"]["count"]
        return datagram_sent

    def get_data_datagram_sent(self):
        data_datagram_sent = 0
        for event in self._get_events():
            if is_datagrams_sent(event):
                for row in event["data"]["raw"]:
                    if row["length"] > 0:
                        data_datagram_sent += 1
        return data_datagram_sent

    def get_data_sent(self):
        sent = {}  # pkt_numbet -> data_carried
        for event in self._get_events():
            if is_packet_sent(event):
                data_carried = 0
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        data_carried += frame["length"]
                sent[event["data"]["header"]["packet_number"]] = data_carried
            if is_packet_lost(event):
                del sent[event["data"]["packet_number"]]
        data_sent = sum(sent.values())
        return data_sent

    def get_datagram_received(self):
        datagram_received = 0
        for event in self._get_events():
            if is_datagrams_received(event):
                datagram_received += event["data"]["count"]
        return datagram_received

    def get_data_datagram_received(self):
        data_datagram_received = 0
        for event in self._get_events():
            if is_datagrams_received(event):
                for row in event["data"]["raw"]:
                    if row["length"] > 0:
                        data_datagram_received += 1
        return data_datagram_received

    def get_data_received(self):
        data_received = 0
        for event in self._get_events():
            if is_packet_received(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "stream":
                        data_received += frame["length"]
        return data_received

    def get_next_send_packet_number(self):
        for event in reversed(self._get_events()):
            if is_packet_sent(event):
                return event["data"]["header"]["packet_number"] + 1

    def get_next_receive_packet_number(self):
        for event in reversed(self._get_events()):
            if is_packet_received(event):
                return event["data"]["header"]["packet_number"] + 1
        
    def get_connexion_duration(self):
        events = self._get_events()
        return events[-1]["time"] - events[0]["time"]

    def get_upload_estimated_overhead(self):
        # udp header = 8 bytes
        udp_headers = self.get_datagram_sent() * 8
        # total bytes sent
        total_bytes_sent = udp_headers + self.get_bytes_sent()
        
        if total_bytes_sent == 0: return 0

        return 1 - (self.get_data_sent() / total_bytes_sent)

    def get_spurious(self):
        acked = set()
        losts = set()
        for event in self._get_events():
            if is_packet_received(event):
                for frame in event["data"]["frames"]:
                    if frame["frame_type"] == "ack":
                        for start, end in frame["acked_ranges"]:
                            acked |= set(range(start, end+1))
            if is_packet_lost(event):
                losts.add(event["data"]["packet_number"])
        return len(acked.intersection(losts))



    def to_json(self):
        methodes = [methode for methode in dir(
            self) if methode.startswith('get_')]
        return {meth[4:]: getattr(self, meth)() for meth in methodes}
