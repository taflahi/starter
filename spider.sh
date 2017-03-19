#!/bin/bash

cp -a '/Users/tirmidzi/Cores/Codes/RECO/Py/SpiderDecoder/.' '/Users/tirmidzi/Cores/Codes/RECO/Outputs/'$1'/'
sed -i '.bak' 's/_business_id/'$2'/g' '/Users/tirmidzi/Cores/Codes/RECO/Outputs/'$1'/spider.sh'