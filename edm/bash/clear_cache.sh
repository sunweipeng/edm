#!/bin/bash
# -*- coding: utf-8 -*-
used=`free -m | awk 'NR==2' | awk '{print $3}'`
free=`free -m | awk 'NR==2' | awk '{print $4}'`
echo "===========================" >> yl_dropcaches.log
date >> yl_dropcaches.log
echo "Memory usage | [Use：${used}MB][Free：${free}MB]" >>  yl_dropcaches.log
if [ $free -le 400 ] ; then
 #sync && echo 1 > /proc/sys/vm/drop_caches
 #sync && echo 2 > /proc/sys/vm/drop_caches
	sync && echo 3 > /proc/sys/vm/drop_caches
	echo "OK" >>  yl_dropcaches.log
else
	echo "Not required" >> yl_dropcaches.log
fi
