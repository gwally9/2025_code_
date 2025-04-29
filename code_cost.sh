#!/bin/bash

regions=$(aws ec2 describe-regions --query "Regions[].RegionName" --output text)
#regions="eu-west-1  eu-west-2  eu-west-3  us-east-1 us-east-2  us-west-1 us-west-2 "

for region in $regions; do
    echo "Checking region: $region"
 
    aws ec2 describe-instances \
        --filters Name=instance-state-name,Values=stopped,running \
        --query "Reservations[*].Instances[*].{Region:'$region', Name:Tags[?Key==\`Name\`]|[0].Value, Instance:InstanceId, Type:InstanceType, State:State.Name}" \
        --output text \
        --region $region >> inventory.csv

    echo "Finished checking region: $region"
done

