
aws ssm send-command \
    --document-name "AWS-RunShellScript" \
    --instance-ids  "i-01f06933075dec4ac" \
    --parameters '{"commands":["#!/usr/bin/bash","sudo service amazon-ssm-agent restart"]} ' \
    --output text \
    --query "Command.CommandId"