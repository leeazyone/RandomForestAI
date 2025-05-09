import subprocess


def run_tshark(pcap_path, csv_path):
    #tshark_path = "C:\\Program Files\\Wireshark\\tshark.exe"  # 직접 경로 지정

    cmd = [
        "tshark", "-r", pcap_path, "-T", "fields",
        "-e", "frame.time_epoch", "-e", "ip.src", "-e", "ip.dst", "-e", "ip.len",
        "-e", "icmp.type", "-e", "udp.dstport", "-e", "udp.length",
        "-e", "tcp.flags.syn", "-e", "tcp.flags.ack", "-e", "tcp.dstport",
        "-e", "tcp.seq", "-e", "tcp.ack", "-e", "ip.ttl",
        "-e", "arp.src.proto_ipv4", "-e", "arp.dst.proto_ipv4", "-e", "arp.opcode",
        "-E", "header=y", "-E", "separator=,", "-E", "quote=d", "-E", "occurrence=f"
    ]

    with open(csv_path, 'w') as f:
        subprocess.run(cmd, stdout=f, check=True)