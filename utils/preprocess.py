import pandas as pd

def preprocess_csv(filepath):
  df = pd.read_csv(filepath)  # DataFrame
  result = {}

  # 전체 패킷 수
  result['packet_count'] = len(df)

  if 'ip.len' in df.columns:
    result['mean_ip_len'] = df['ip.len'].mean()  # 평균 길이
    result['std_ip_len'] = df['ip.len'].std()    # 표준 편차

  if 'icmp.type' in df.columns:
    # ICMP 타입이 8인 평균 비율
    result['icmp_type_8_ratio'] = (df['icmp.type'] == 8).mean()
  
  if 'udp.dstport' in df.columns:
    # 목적지 포트 종류 개수
    result['udp_port_variety'] = df['udp.dstport'].nunique()
  
  if 'udp.length' in df.columns:
    # UDP 패킷 길이의 평균
    result['mean_udp_len'] = df['udp.length'].mean()

  if 'tcp.flags.syn' in df.columns:
    # SYN 플래그가 켜진 패킷 수 (TCP 연결 시작 신호)
    result['syn_count'] = df['tcp.flags.syn'].sum()
  
  if 'tcp.dstport' in df.columns:
    # TCP 목적지 포트의 다양성
    result['tcp_port_variety'] = df['tcp.dstport'].nunique()
  
  if 'tcp.seq' in df.columns:
    # TCP 시퀀스 번호의 표준편차 (패킷 흐름 분석용)
    result['tcp_seq_var'] = df['tcp.seq'].std()

  if 'ip.ttl' in df.columns:
    # time-to-live 평균 (네트워크 거리 추정에 사용)
    result['mean_ttl'] = df['ip.ttl'].mean()

  if 'arp.opcode' in df.columns:
    # ARP 응답 패킷의 비율 (2는 Reply)
    result['arp_reply_ratio'] = (df['arp.opcode'] == 2).mean()
  
  if 'arp.src.proto_ipv4' in df.columns:
    # ARP 요청을 보낸 고유한 IP 개수
    result['arp_src_ip_unique'] = df['arp.src.proto_ipv4'].nunique()

  return pd.DataFrame([result])
