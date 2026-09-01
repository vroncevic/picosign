#!/bin/bash
#
# @brief   picosign
# @version 1.0.0
# @date    Tue Sep 01 10:50:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 coverage/ats_coverage.py picosign
pylint picosign > picosign.report
echo "Done"
