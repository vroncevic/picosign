#!/bin/bash
#
# @brief   picosign
# @version 1.0.0
# @date    Tue Sep 01 10:45:00 2026
# @company None, free software to use 2026
# @author  Vladimir Roncevic <elektron.ronca@gmail.com>
#

python3 main.py sign --file "microhil-base.uf2" --output "microhil-signed.uf2" --signature "AUTHOR: Vladimir Roncevic | BUILD: 2026-09-01 | VERSION: 1.0.0"
python3 main.py read --file "microhil-signed.uf2"
