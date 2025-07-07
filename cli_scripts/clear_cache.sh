# Simple bash scripts which cleans cached RAM

user_id=`whoami`
if [[ "$user_id" != "root" ]]
then
  echo "$0: Run this script with root access"
  exit 126
fi

function clear_cache ()
{
  sudo echo 1 > /proc/sys/vm/drop_caches
}

clear_cache()
exit 0