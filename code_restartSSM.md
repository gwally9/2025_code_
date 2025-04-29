## Set Up CloudWatch Event for SSM Agent
To set up a CloudWatch event rule to automatically restart the SSM Agent service periodically, you can follow these steps:

Create a CloudWatch event rule that triggers based on a schedule. You can specify the frequency, 
such as every 5 minutes or hourly, using the EventBridge console or AWS CLI.
Configure the target of the event rule to run a Systems Manager (SSM) document that restarts 
the SSM Agent service. This can be done by creating an SSM document with a command to restart 
the service and setting it as the target of the CloudWatch event rule.
For example, you can use the aws events put-rule and aws events put-targets commands to create 
the rule and set the target, respectively. Additionally, you can use the aws ssm send-command 
command to run the SSM document that restarts the SSM Agent service.

Here is an example of an SSM document content that restarts the SSM Agent service:

```
{
    "schemaVersion": "1.2",
    "description": "Restart SSM Agent",
    "parameters": {},
    "runtimeConfig": {
        "aws:runShellScript": {
        "properties": [
            {
            "id": "0.aws:runShellScript",
            "runCommand": [
                "sudo service amazon-ssm-agent restart"
            ]
            }
        ]
        }
    }
}
```
This document can be used as the target of the CloudWatch event rule to automatically restart the SSM Agent service periodically.


aws ssm send-command \
    --document-name "AWS-RunShellScript" \
    --instance-ids  "i-01f06933075dec4ac" \
    --parameters '{"commands":["#!/usr/bin/bash","sudo service amazon-ssm-agent restart""]} ' \
    --output text \
    --query "Command.CommandId"