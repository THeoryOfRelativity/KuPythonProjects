#!/bin/bash
while true; do
  tail -Fn4000 $RTPSLOGPATH/ROUTING_SWITCH_"`date +%y%m%d`".log | pytool get_rsw_time_tail.py 0.1 STIP_START
done




