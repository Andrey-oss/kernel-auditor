# Kernel Auditor

## Overview
This project is a Flask-based web application designed for system monitoring, optimization, and tweaking on Linux systems. It provides detailed information about system resources, networking, hardware, processes, I/O schedulers, sysctl settings and etc. Users can also modify system settings directly from the web interface

## Features
- **System Information**: View detailed OS and hardware information
- **Network Monitoring**: Display network interfaces, IP addresses, and perform speed tests
- **Process Management**: List and analyze running processes
- **I/O Scheduler Management**: Change and tune I/O schedulers dynamically
- **Sysctl Tweaks**: Modify and apply kernel parameters in real-time
- **API Support**: Expose endpoints for automation and remote management
- **CPU Tuning**: Change governors, frequencies and features
- **Network Settings**: Change and modify some network preferences easily

## Installation
### Prerequisites
- Python 3
- Flask
- Required Python packages (listed in `requirements.txt`)

### Setup Instructions
```bash
# Clone the repository
git clone https://github.com/Andrey-oss/kernel-auditor.git
cd kernel-auditor

# Install dependencies
pip3 install -r requirements.txt

# Run the application
sudo python3 main.py
```

### Install as system-wide service
```bash
# You can install it by running
make make_syswide

# And if you wish to delete it
make del_syswide

# Also you can free some space on your drive:
make clean
```

## Configuration
The application uses a configuration file to manage settings. You can adjust settings in `settings.json`

## Some API Endpoints
### Scheduler Management
- **Set I/O Scheduler**: `POST /api/set_scheduler`
  ```json
  {
      "device": "sda",
      "scheduler": "mq-deadline"
  }
  ```

- **Tune Scheduler Parameters**: `POST /api/set_sched_tunning`
  ```json
  {
      "parameter": "nr_requests",
      "value": "128"
  }
  ```

### Sysctl Management
- **Modify Kernel Parameters**: `POST /api/set_sysctl`
  ```json
  {
      "name": "vm.swappiness",
      "value": "10"
  }
  ```

### CPU Management
- **Set CPU Governor**: `POST /api/set_cpu_governor`
  ```json
  {
      "cpu": 0,
      "governor": "performance"
  }
  ```
- **Set CPU Frequencies**: `POST /api/set_cpu_frequency`
  ```json
  {
      "cpu": 0,
      "min_freq": 2400000,
      "max_freq": 5000000
  }
  ```

- **Set CPU Features**: `POST /api/set_cpu_features`
  ```json
  {
      "cpu": 0,
      "cpb": 1,
      "boost": 1 
  }
  ```

## Usage
- Visit `http://127.0.0.1:5000/` to access the web interface
- Navigate through the sections to view and modify system settings

## Documentation
You can read our documentation, if you don't understand something

## Contributing
Feel free to fork this repository and submit pull requests for improvements

## License
This project is licensed under the MIT License