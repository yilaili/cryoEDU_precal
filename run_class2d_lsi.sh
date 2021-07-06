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
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --mpinodes 5 &
    wait
  done
done

#### do ctf, no ctf_intact_first_peak, no zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --mpinodes 5 &
    wait
  done
done

#### do ctf, do ctf_intact_first_peak, no zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --mpinodes 5 &
    wait
  done
done

#########################
#### no ctf, no ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --zero_mask --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --zero_mask --mpinodes 5 &
    wait
  done
done

#### do ctf, no ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --zero_mask --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --zero_mask --mpinodes 5 &
    wait
  done
done

#### do ctf, do ctf_intact_first_peak, do zero_mask
for diam in 120 180 250 350
do
  for tau2_fudge in 1 2 8 24
  do
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 3 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 10 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 25 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --mpinodes 2 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 50 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --mpinodes 4 &
    python /lsi/groups/mcianfroccolab/yilai/codes/cryoEDU_precal/submit_class2d.py -i Extract/job014/particles.star --projdir /lsi/groups/mcianfroccolab/yilai/cryoEDU_precal_results/T20S -d $diam -K 100 --tau2_fudge $tau2_fudge --ctf --ctf_intact_first_peak --zero_mask --mpinodes 5 &
    wait
  done
done
