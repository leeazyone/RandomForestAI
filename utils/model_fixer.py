import pandas as pd

def fix_prediction(prediction: str, summary: pd.DataFrame) -> str:
    icmp_ratio = summary.get("icmp_type_8_ratio", pd.Series([0])).iloc[0]
    std_ip_len = summary.get("std_ip_len", pd.Series([0])).iloc[0]
    udp_variety = summary.get("udp_port_variety", pd.Series([0])).iloc[0]
    mean_udp_len = summary.get("mean_udp_len", pd.Series([0])).iloc[0]
    arp_reply_ratio = summary.get("arp_reply_ratio", pd.Series([0])).iloc[0]
    mac_per_ip = summary.get("mac_per_ip", pd.Series([0])).iloc[0]

    if prediction == "Ping of Death" and icmp_ratio > 0.4 and std_ip_len < 10:
        return "ICMP Flood"

    if prediction == "UDP Flood":
        if arp_reply_ratio > 0.05 and mac_per_ip > 1.0 and udp_variety <= 5 and mean_udp_len > 30:
            return "ARP Spoofing"

    return prediction