#!/bin/sh
#sdsort for sorting the results according to their score
sdsort -n -f'SCORE' 1sj0_docking_out.sd > 1sj0_docking_out_sorted.sd
cat 1sj0_docking_out_sorted.sd
