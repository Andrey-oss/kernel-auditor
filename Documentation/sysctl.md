# 📝 Sysctl Settings Documentation

## 🔧 What is Sysctl?

**Sysctl** is an interface for managing kernel parameters and various aspects of the operating system in real-time. These parameters control critical aspects such as system performance, security, and networking. In Linux, sysctl-controlled parameters are stored in the virtual file system `/proc/sys` With sysctl commands, you can both view and modify these values

Changing a sysctl parameter can directly affect system behavior, performance, and other core aspects of your machine

## 🔍 What Can Be Done on This Page?

This web interface allows you to:

- **Search for Settings**: Use the search field to find specific sysctl parameters quickly
- **Modify Values**: Change the value of any parameter directly in the table. After editing the value, click the **"Apply"** button to save your changes
- **Apply Settings**: Clicking the **"Apply"** button sends the updated value to the system, and it will take effect immediately

## 🏷️ Example Default Values for Common Parameters

Here are some default values for common sysctl parameters:

| **Parameter**            | **Description**                                           | **Default Value** |
|--------------------------|-----------------------------------------------------------|-------------------|
| **`vm.swappiness`**       | Controls how often the system uses swap space            | `60`              |
| **`fs.file-max`**         | Limits the number of open file descriptors in the system | `8192`            |
| **`net.ipv4.ip_forward`** | Controls IPv4 packet forwarding (routing)               | `0` (disabled)    |
| **`net.core.somaxconn`**  | The maximum number of connections in the listening queue | `128`             |
| **`kernel.pid_max`**      | The maximum Process ID (PID) number for system processes | `32768`           |

## ⚙️ How to Change a Parameter?

Follow these steps to change sysctl parameter values:

1. **Search** for the parameter you want to modify by typing its name in the search bar
2. **Edit** the value in the "Value" column by typing a new value
3. **Apply** the new setting by clicking the **"Apply"** button next to the parameter

Once applied, the changes will take effect immediately in your system’s kernel

> **⚠️ Important!** Be cautious when modifying these values, as incorrect configurations could lead to system instability, performance issues, or even crashes

## 🗨️ Notes

- After clicking **"Apply"**, the modified values are sent to the kernel and will be immediately reflected in the system
- This tool provides an easy-to-use interface for managing critical system parameters without needing to interact directly with the terminal