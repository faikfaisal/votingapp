# Preparation

This folder contains scripts and configuration files to set up the necessary AWS resources for the votingapp application.

## prepare.sh

The `prepare.sh` script is responsible for creating an Amazon DynamoDB table and an IAM role with a policy to access the table. The script performs the following steps:

1. Retrieves the AWS account ID and region using the AWS CLI.
2. Creates a DynamoDB table with the specified name (`votingapp-restaurants` by default), attribute definitions, key schema, and billing mode (PAY_PER_REQUEST).
3. Waits for a few seconds to ensure the table is available.
4. Adds initial items to the table for each restaurant (ihop, outback, bucadibeppo, chipotle) with a vote count of 0.
5. Creates an IAM role using the `apprunner-trust-policy.json` file, which allows App Runner to assume the role.
6. Creates an IAM policy using the `votingapp-ddb-policy.json` file, after replacing placeholders (ACCOUNT_ID, AWS_REGION, TABLE_NAME) with actual values.
7. Attaches the created policy and the AWSXRayDaemonWriteAccess policy to the IAM role.

The script assigns a DynamoDB table name and IAM role name using variables at the beginning (`TABLE_NAME` and `IAM_ROLE`), which can be changed if desired.

## apprunner-trust-policy.json

This file contains the trust policy for the IAM role created by the `prepare.sh` script. The trust policy allows App Runner to assume the role, granting it the necessary permissions to access the DynamoDB table.

The trust policy is defined in JSON format and specifies the following:
- The version of the policy language (2012-10-17)
- The principal that is allowed to assume the role (in this case, the App Runner service)
- The actions that the principal is allowed to perform (sts:AssumeRole)

## votingapp-ddb-policy.json

This file contains the IAM policy template that grants permissions to access the DynamoDB table. The policy template includes placeholders (ACCOUNT_ID, AWS_REGION, TABLE_NAME) that are replaced with actual values by the `prepare.sh` script when creating the IAM policy.

The policy is defined in JSON format and specifies the following:
- The version of the policy language (2012-10-17)
- The statement that defines the permissions
  - The effect of the statement (Allow)
  - The actions that are allowed (dynamodb:*)
  - The resource that the actions can be performed on (the ARN of the DynamoDB table)

## Usage

To set up the necessary AWS resources for the votingapp application:

1. Ensure you have the AWS CLI installed and configured with the appropriate credentials and region.
2. Run the `prepare.sh` script to create the DynamoDB table and IAM role.
   ```
   ./prepare.sh
   ```
3. After running the script, the DynamoDB table and IAM role will be created. You can now deploy the votingapp application using AWS App Runner, associating the created IAM role with the App Runner service to grant it the necessary permissions to access the DynamoDB table.
