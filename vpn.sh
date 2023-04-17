#!/bin/bash

sudo openconnect --config /etc/vpnc/default.conf --non-inter  c2sext.comfama.com.co --passwd-on-stdin <<< A1b1c1d1.. &
