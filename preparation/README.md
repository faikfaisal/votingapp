# Preparation

This folder contains scripts and configuration files to set up the necessary AWS resources for the votingapp application.

## prepare.sh

The `prepare.sh` script is a bash script that automates the process of creating an Amazon DynamoDB table and an IAM role with the required permissions to access the table.

The script performs the following steps:

1. Sets the table name in the `$TABLE_NAME` variable and the IAM role name in the `$IAM_ROLE` variable. These values can be modified if desired.

2. Retrieves the AWS account ID using the `aws sts get-caller-identity` command and stores it in the `$ACCOUNT_ID` variable.

3. Retrieves the AWS region from the AWS CLI configuration using the `aws configure get region` command and stores it in the `$AWS_REGION` variable. If the region is not set, an error message is displayed and the script exits.

4. Creates the DynamoDB table using the `aws dynamodb create-table` command with the following parameters:
   - The table name is set to the value of `$TABLE_NAME`.
   - The table has a single key attribute named "name" of type String.
   - The billing mode is set to PAY_PER_REQUEST.
   - The AWS region is set to the value of `$AWS_REGION`.

5. Waits for 10 seconds to ensure the table is available before proceeding.

6. Inserts initial items into the DynamoDB table using the `aws dynamodb put-item` command. Four items are added, one for each restaurant: ihop, outback, bucadibeppo, and chipotle. Each item has a "name" attribute with the restaurant name and a "restaurantcount" attribute initialized to 0.

7. Creates the IAM role using the `aws iam create-role` command with the following parameters:
   - The role name is set to the value of `$IAM_ROLE`.
   - The assume role policy document is read from the `apprunner-trust-policy.json` file.

8. Creates the IAM policy for the role:
   - The `votingapp-ddb-policy.json` file serves as a template for the IAM policy. It contains placeholders for the account ID, AWS region, and table name.
   - The `sed` command is used to substitute the placeholders with the actual values and write the result to a temporary file named `filled-votingapp-ddb-policy.json`.
   - The `aws iam create-policy` command creates the IAM policy using the `filled-votingapp-ddb-policy.json` file.
   - The temporary `filled-votingapp-ddb-policy.json` file is deleted.

9. Attaches the created IAM policy and the AWS managed `AWSXRayDaemonWriteAccess` policy to the IAM role using the `aws iam attach-role-policy` command. The `AWSXRayDaemonWriteAccess` policy allows the application to perform X-Ray tracing.

## File Roles

- `apprunner-trust-policy.json`: This file contains the assume role policy document that allows the AWS App Runner service to assume the IAM role created by the script.

- `prepare.sh`: This is the main bash script that automates the creation of the DynamoDB table, IAM role, and associated policies.

- `votingapp-ddb-policy.json`: This file serves as a template for the IAM policy that grants the necessary permissions to access the DynamoDB table. It contains placeholders for the account ID, AWS region, and table name, which are replaced with the actual values during the script execution.

These files work together to set up the required AWS resources for the votingapp application, ensuring that the application has the necessary permissions to interact with the DynamoDB table and perform X-Ray tracing.
