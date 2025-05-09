import subprocess #터미널 명령어 실행할 수 있는 모듈

def run_tshark(pcap_path, csv_path):
  cmd = [ "tshark", "-r", pcap_path, "-T", "fields",
        "-e", "frame.time_epoch", "-e", "ip.src", "-e", "ip.dst", "-e", "ip.len",
        "-e", "icmp.type", "-e", "udp.dstport", "-e", "udp.length",
        "-e", "tcp.flags.syn", "-e", "tcp.flags.ack", "-e", "tcp.dstport",
        "-e", "tcp.seq", "-e", "tcp.ack", "-e", "ip.ttl",
        "-e", "arp.src.proto_ipv4", "-e", "arp.dst.proto_ipv4", "-e", "arp.opcode",
        "-E", "header=y", "-E", "separator=,", "-E", "quote=d", "-E", "occurrence=f"]

  with open(csv_path, 'w') as f:
    subprocess.run(cmd, stdout=f, check=True) 
    #명령어 결과를 새 파일에 저장하고 오류 생기면 알려줌