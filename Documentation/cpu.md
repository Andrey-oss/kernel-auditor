# 🔥 CPU Scaling & Governors Explained  

## 📌 Overview  
CPU scaling is a mechanism that dynamically adjusts the processor's clock speed based on workload demand. This helps conserve energy, reduce heat generation, and improve performance when needed

---

## ⚡ CPU Frequency Scaling  
The processor can operate at different frequencies depending on the load
To check available frequencies, run:
```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_frequencies
```
This will output a list of values (in kHz), for example:
```
800000 1200000 1600000 2000000 2400000
```
- **Check the minimum frequency**:  
  ```bash
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq
  ```
- **Check the maximum frequency**:
  ```bash
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
  ```
- **Check the current frequency**:
  ```bash
  cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
  ```

To manually adjust frequencies:
```bash
echo 1600000 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq
echo 2400000 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
```

---

## 🌛 CPU Frequency Governors
Governors are kernel modules that control how the CPU scales its frequency

### 🔹 Checking available governors
Run the following command:
```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors
```
This will output something like:
```
performance powersave ondemand conservative schedutil
```
### 🔹 Checking the current governor
```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```

### 🔹 Changing the CPU governor for some cores
To change the governor, use:
```bash
echo "performance" | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```
(Replace `"performance"` with your preferred governor)

### 🏆 Available Governors  
| Governor      | Description |
|--------------|-------------|
| `performance` | Always runs the CPU at maximum frequency. Best for high performance |
| `powersave`   | Keeps the CPU at the lowest possible frequency. Best for battery life |
| `ondemand`    | Dynamically adjusts frequency based on CPU load. Default on many systems |
| `conservative` | Similar to `ondemand`, but increases/decreases frequency more gradually |
| `schedutil`   | Uses the CPU scheduler to determine optimal frequency. Best for modern Linux kernels |
- Also you can see more bigger documentation about all available governors. See [here](https://xdaforums.com/t/gpu-governors-detailed.3916728)
---

## 🚀 Core Performance Boost (CPB) and Precision Boost
Some CPUs support additional performance features:

- **AMD Core Performance Boost (CPB)**: Similar to Intel Turbo Boost (currently unsupported)
- **AMD Precision Boost**: Dynamically increases clock speed for improved performance based on workload and thermal conditions

To check if these features are enabled:
```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/boost
```
- `1` = Enabled
- `0` = Disabled

To disable Precusion Boost:
```bash
echo 0 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/boost
```
To enable it again:
```bash
echo 1 | sudo tee /sys/devices/system/cpu/cpu0/cpufreq/boost
```

For AMD CPUs, check Core Performance Boost (CPB)/Precision Boost:
```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/cpb
```
You can enable/disable it the same way

---

## 🔗 Useful Commands
- **Check CPU info**:
  ```bash
  lscpu
  ```
- **Check real-time CPU frequency**:
  ```bash
  watch -n1 "cat /proc/cpuinfo | grep 'MHz'"
  ```
- **List all CPU frequency settings**:
  ```bash
  find /sys/devices/system/cpu/cpu*/cpufreq/ -type f
  ```