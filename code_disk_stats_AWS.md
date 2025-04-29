Then you can loop through the attached volumes and gather some statistics  as related to the performance of the volumes attached to the instance. 

for Volume in $(aws ec2 describe-instances --instance-ids  "i-01f06933075dec4ac"|grep VolumeId|awk -F: '{print $2}') 
do 
   echo ${Volume}  
   aws cloudwatch get-metric-statistics \     
     --namespace AWS/EBS --metric-name VolumeReadBytes \     
     --start-time 2025-04-01T00:00:00 \     
     --end-time 2025-04-02T01:00:00 \     
     --period 300 \     
     --statistics Sum \     
     --dimensions Name=VolumeId,Value=${Volume} 
   echo "." 
done  

 NOTE: one would change the date ranges (start/end) for the period under observation and replace the instance ID to match that of the EC2 resource having the issues  
 