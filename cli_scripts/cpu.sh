# Simple bash script to change the processor governor on all cores

available_governors=$(cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_available_governors \
  | head -1 | sed -e 's/ \([a-zA-Z0-9]\)/|\1/g' -e 's/ $//')
if [ $# -ne 1 ]
then
  echo "Usage: $0 [$available_governors]"
fi

function current_cpu_governor ()
{
  echo -n "CPU scaling governor is currently set to: "
  cpu_scaling_governor="NOT SET"
  for governor in $(ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor)
  do
    cpu_scaling_governor=$(cat $governor)
  done
  echo "$cpu_scaling_governor"
}

current_cpu_governor;

new_governor=""
if [ $# -eq 0 ]
then
  exit 0
else
  new_governor="$1"
fi

user_id=`whoami`
if [[ "$user_id" != "root" ]]
then
  echo "$0: please run this script as root user."
  exit
fi

if [ -z $(echo $available_governors | sed -e 's/^/|/' -e 's/$/|/' | grep "|$new_governor|") ]
then
  echo "Mode '$new_governor' is not supported"
  exit 1
else
  echo "Setting CPU into '$new_governor' mode..."
fi
for governor in $(ls /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor)
do
  echo "$new_governor" > $governor
done
current_cpu_governor;
exit 0
