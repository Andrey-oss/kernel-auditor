# 📌 I/O Scheduler Settings Documentation  

## 🔹 What is an I/O Scheduler?  
An **I/O (Input/Output) Scheduler** is a Linux kernel mechanism that manages the order of read/write operations to storage devices (HDD, SSD, NVMe). It optimizes disk system performance by organizing requests efficiently, reducing latency, and increasing throughput

## 🔹 Why is an I/O Scheduler important?  
When multiple read/write requests are made simultaneously, the scheduler determines the most efficient execution order to minimize delays

### Common I/O Schedulers:  
- **noop** → Best for SSDs, as it processes requests in a simple FIFO manner
- **deadline** → Reduces I/O request latency, suitable for real-time systems
- **cfq** (deprecated) → Balanced but inefficient for SSDs
- **bfq** → An enhanced CFQ scheduler for HDDs and interactive workloads
- **kyber** → Optimized for NVMe and SSDs, ensures low latency
- **mq-deadline** → A multi-queue version of the deadline scheduler for modern systems

---

## 🔹 What does the I/O Scheduler Settings page do?  
This page provides a user-friendly interface to:  
- ✅ View the current I/O scheduler for each device
- ✅ Dynamically change the I/O scheduler in real-time
- ✅ Tune advanced I/O parameters for better performance
- ✅ Apply changes without requiring a system reboot

---

## 🔹 UI Elements & Functionality  

### 🛠 Selecting an I/O Scheduler  
- A **dropdown menu** allows users to switch between available schedulers for a specific device
- Clicking the **"Apply"** button sends a request to update the scheduler

### ⚙️ Advanced I/O Tuning Parameters  
Users can fine-tune various disk parameters to optimize performance:  

| **Parameter**         | **Description** | **Recommended Values** |
|-----------------------|----------------|------------------------|
| `nr_requests`        | The maximum number of I/O requests in the queue. Higher values can improve performance on high-speed devices | `64 - 1024` |
| `read_ahead_kb`      | Amount of data (in KB) the system pre-reads from storage to improve read efficiency | `128 - 8192` |
| `max_sectors_kb`     | Maximum amount of data (in KB) that can be processed per single I/O request | `128 - 4096` |
| `io_timeout`         | Timeout (in ms) for an I/O request before being considered failed. Lower values improve responsiveness but may cause premature request failures | `100 - 30000` |

### 🎛 Applying the Settings  
- Clicking **"Apply"** for the scheduler sends a `POST` request to `/api/set_scheduler`
- Clicking **"Apply Tuning"** for tuning parameters sends a `POST` request to `/api/set_sched_tunning`

---

## 🔹 API Endpoints Used  

### `POST /api/set_scheduler`  
🔹 Changes the I/O scheduler for a specified device
**Payload Example:**  
```json
{
  "device": "nvme0n1",
  "scheduler": "kyber"
}
```

## `POST /api/set_sched_tunning`  
🔹 Adjusts advanced I/O tuning parameters for a specific storage device
**Payload Example:**
```json
{
  "device": "sda",
  "nr_requests": 256,
  "read_ahead_kb": 1024,
  "max_sectors_kb": 512,
  "io_timeout": 5000
}
```

## 🔹 How It Works  
- 1️⃣ The user selects an I/O scheduler and clicks **"Apply"**
- 2️⃣ The page sends an API request to `/api/set_scheduler`
- 3️⃣ The backend updates the scheduler via sysfs (`/sys/block/{device}/queue/scheduler`)
- 4️⃣ If tuning parameters are changed, a request is sent to `/api/set_sched_tunning`
- 5️⃣ The backend applies the new values to `/sys/block/{device}/queue/`