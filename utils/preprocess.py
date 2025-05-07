import pandas as pd

def preprocess_csv(filepath):
  df = pd.read_csv(filepath) #DataFrame
  result = {}

  #전체 패킷 수 
  result['packet_count'] = len(df)

  if 'ip.len' in df:
    result['mean_ip_len'] = df['ip.len'].mean()
    result['std_ip_len'] = df['ip.len'].std()

  if 'icmp.type' in df:
    result['icmp_type_8_ratio'] = (df['icmp.type'] == 8).mean()
  
  if 'udp.dstport' in df:
    result['udp_port_variety'] = df['udp.dstport'].nunique()
  if 'udp.length' in df:
    result['mean_udp_len'] = df['udp.length'].mean()

  if 'tcp.flags.syn' in df:
    result['syn_count'] = df['tcp.flags.syn'].sum()
  if 'tcp.dstport' in df:
    result['tcp_port_variety'] = df['tcp.dstport'].nunique()
  if 'tcp.seq' in df:
    result['tcp_seq_var'] = df['tcp.seq'].std()

  if 'ttl' in df:
    result['mean_ttl'] = df['ttl'].mean()

  if 'arp.opcode' in df:
    result['arp_reply_ratio'] = (df['arp.opcode']==2).mean()
  if 'arp.src.proto_ipv4' in df:
    result['arp_src_ip_unique'] = df['arp.src.proto_ipv4'].nunique()

  return pd.DataFrame([result])