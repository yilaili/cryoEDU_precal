#!/bin/bash

# diam=120,180,250,350
# K=3,10,25,50,100
# tau2_fudge=1,2,8,24

# ctf=0
# ctf_intact_first_peak=0
# zero_mask=0

#### no ctf, no ctf_intact_first_peak, no zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --nodes 8 &
    wait
  done
done

#### do ctf, no ctf_intact_first_peak, no zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --nodes 8 &
    wait
  done
done

#### do ctf, do ctf_intact_first_peak, no zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --nodes 8 &
    wait
  done
done

#########################
#### no ctf, no ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --zero_mask --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --zero_mask --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --zero_mask --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --zero_mask --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --zero_mask --nodes 8 &
    wait
  done
done

#### do ctf, no ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --zero_mask --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --zero_mask --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --zero_mask --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --zero_mask --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --zero_mask --nodes 8 &
    wait
  done
done

#### do ctf, do ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --nodes 1 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --nodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --nodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --nodes 5 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_2D/submit_2DClass.py -i job014/particle_1.star -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --nodes 8 &
    wait
  done
done
