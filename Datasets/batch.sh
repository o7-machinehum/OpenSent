#!/bin/bash

#Batch run below
#Make some files with the listings in them
ls Oct > batchOutput/OctListing
ls Sept > batchOutput/SeptListing

#Lets first read in out october listing
readarray arry < batchOutput/OctListing

for i in "${arry[@]}";
do
	./BatchLagFinder.m Oct/$i
done
