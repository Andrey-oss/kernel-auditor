# Network Settings – Technical Documentation

This module provides a unified interface for managing and tuning various Linux networking parameters. It is designed for administrators and power users seeking fine-grained control over TCP/IP behavior, interface configuration, and DNS resolution

---

## 1. TCP Congestion Control Algorithms

### 📌 What is it?

TCP Congestion Control Algorithms determine how TCP reacts to network congestion. Choosing the right algorithm can improve throughput, latency, and reliability based on workload

### 🛠 Available Parameters

- `net.ipv4.tcp_congestion_control`: Current congestion control algorithm
- `/proc/sys/net/ipv4/tcp_available_congestion_control`: Lists all available algorithms

### 🔧 Example:

```bash
sysctl net.ipv4.tcp_congestion_control=bbr
```

---

## 2. MAC Address Changer

### 📌 What is it?

Temporarily or permanently changes the MAC address of a network interface. Useful for privacy, spoofing, or network testing

### 🛠 Tools/Interfaces

- `ip link set dev <iface> address <new_mac>`
- `macchanger` (utility)

### ⚠ Note:

Changing MAC may cause DHCP lease invalidation or network instability

---

## 3. DNS Resolver Configuration (`resolv.conf`)

### 📌 What is it?

Controls name resolution by specifying DNS servers in `/etc/resolv.conf`

### 🛠 Example:

```bash
echo "nameserver 8.8.8.8" > /etc/resolv.conf
```

Can be overwritten by:
- `systemd-resolved`
- `NetworkManager`
- `dhclient`

### 💡 Persistent Configuration

Disable overwrite by setting immutable bit:

```bash
chattr +i /etc/resolv.conf
```

---

## 4. Socket Buffer/Queue Settings

### 📌 What is it?

Controls kernel-level buffers for sending and receiving packets

### 🛠 Common Parameters

- `net.core.rmem_max` – max receive buffer
- `net.core.wmem_max` – max send buffer
- `net.ipv4.tcp_rmem` – min/default/max receive buffer for TCP
- `net.ipv4.tcp_wmem` – min/default/max send buffer for TCP
- `net.core.netdev_max_backlog` – max number of packets in input queue

### 🔧 Example:

```bash
sysctl -w net.core.rmem_max=16777216
sysctl -w net.core.wmem_max=16777216
```

---

## API Integration

This page interfaces with backend APIs using POST requests:

- `/api/change_mac`: Temporarily sets MAC address
- `/api/set_resolv_conf`: Updates DNS settings in `resolv.conf`
- `/api/set_congestion_algorithm`: Applies new TCP congestion algorithm
- `/api/set_socket_buffers`: Changes socket settings (currently for buffers)

---

## Summary

This page offers advanced control over Linux networking internals. It is ideal for scenarios where:

- Custom latency/throughput tuning is required
- System is acting as a router/firewall
- High-performance server workloads are deployed
- Privacy and MAC spoofing are desired