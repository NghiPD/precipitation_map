#!/bin/bash

# load modules for Derecho:
# ===========
source /etc/profile.d/z00_modules.sh
module purge
module load ncarenv/23.06
module load intel-oneapi/2023.0.0
module load cray-mpich/8.1.25
module load parallel-netcdf/1.12.3
module load parallelio/2.5.10
module load ncl/6.6.2
module load hdf5/1.12.2
module load netcdf/4.9.2
module load ncarcompilers/1.0.0
module load nco/5.1.4
module load conda/latest
export PYTHONDONTWRITEBYTECODE=1

cd $PWD

echo "`date` STARTED DATE"
date_in=("2023021818" "2023021900" "2023021906" "2023021912" "2023021918" "2023022000")
date_start=("2023022012")
date_fcst=("2023022112")
exp=("nghido_letkf_OIE60km_WarmStart_aro_noIP4_01.03")
#choice='True'
for i in "${!date_in[@]}"; do
       din=${date_in[$i]}
       python daily_acc_precip.py ${din} ${date_start} ${date_fcst} ${exp}
     
done
echo "`date` ENDED DATE"
exit 0
