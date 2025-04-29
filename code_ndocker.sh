#!/bin/sh
home="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

instance=${LIMA_INSTANCE:-default}
case "$1" in
begin) 
 cd $home 
 PATH=$PATH:"$home" ./limactl start ${2:-$instance}
 cd - >/dev/null ;;
end) $home/limactl stop $${2:-$instance} ;;
shell) $home/limactl shell ${2:-$instance} ;;
ls|list) $home/limactl ls ;;
*) $home/limactl shell $instance nerdctl "$@"
esac

