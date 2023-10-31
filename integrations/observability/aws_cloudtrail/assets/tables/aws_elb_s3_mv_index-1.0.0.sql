CREATE VIEW AS
    SELECT
        exploded_records.eventVersion AS `aws.cloudtrail.eventVersion`,
        exploded_records.userIdentity.type AS `aws.cloudtrail.userIdentity.type`,
        exploded_records.userIdentity.principalId AS `aws.cloudtrail.userIdentity.principalId`,
        exploded_records.userIdentity.arn AS `aws.cloudtrail.userIdentity.arn`,
        exploded_records.userIdentity.accountId AS `aws.cloudtrail.userIdentity.accountId`,
        exploded_records.userIdentity.accessKeyId AS `aws.cloudtrail.userIdentity.accessKeyId`,
        exploded_records.userIdentity.userName AS `aws.cloudtrail.userIdentity.userName`,
        exploded_records.userIdentity.sessionContext.attributes.creationDate AS `aws.cloudtrail.userIdentity.sessionContext.attributes.creationDate`,
        exploded_records.userIdentity.sessionContext.attributes.mfaAuthenticated AS `aws.cloudtrail.userIdentity.sessionContext.attributes.mfaAuthenticated`,
        exploded_records.eventTime AS `aws.cloudtrail.eventTime`,
        exploded_records.eventSource AS `aws.cloudtrail.eventSource`,
        exploded_records.eventName AS `aws.cloudtrail.eventName`,
        exploded_records.awsRegion AS `aws.cloudtrail.awsRegion`,
        exploded_records.sourceIPAddress AS `aws.cloudtrail.sourceIPAddress`,
        exploded_records.userAgent AS `aws.cloudtrail.userAgent`,
        exploded_records.requestParameters.roleName AS `aws.cloudtrail.requestParameters.roleName`,
        exploded_records.requestParameters.description AS `aws.cloudtrail.requestParameters.description`,
        exploded_records.requestParameters.assumeRolePolicyDocument AS `aws.cloudtrail.requestParameters.assumeRolePolicyDocument`,
        exploded_records.responseElements.role.assumeRolePolicyDocument AS `aws.cloudtrail.responseElements.role.assumeRolePolicyDocument`,
        exploded_records.responseElements.role.arn AS `aws.cloudtrail.responseElements.role.arn`,
        exploded_records.responseElements.role.roleId AS `aws.cloudtrail.responseElements.role.roleId`,
        exploded_records.responseElements.role.createDate AS `aws.cloudtrail.responseElements.role.createDate`,
        exploded_records.responseElements.role.roleName AS `aws.cloudtrail.responseElements.role.roleName`,
        exploded_records.responseElements.role.path AS `aws.cloudtrail.responseElements.role.path`,
        exploded_records.requestID AS `aws.cloudtrail.requestID`,
        exploded_records.eventID AS `aws.cloudtrail.eventID`,
        exploded_records.readOnly AS `aws.cloudtrail.readOnly`,
        exploded_records.eventType AS `aws.cloudtrail.eventType`,
        exploded_records.managementEvent AS `aws.cloudtrail.managementEvent`,
        exploded_records.recipientAccountId AS `aws.cloudtrail.recipientAccountId`,
        exploded_records.eventCategory AS `aws.cloudtrail.eventCategory`,
        exploded_records.tlsDetails.tlsVersion AS `aws.cloudtrail.tlsDetails.tlsVersion`,
        exploded_records.tlsDetails.cipherSuite AS `aws.cloudtrail.tlsDetails.cipherSuite`,
        exploded_records.tlsDetails.clientProvidedHostHeader AS `aws.cloudtrail.tlsDetails.clientProvidedHostHeader`,
        exploded_records.sessionCredentialFromConsole AS `aws.cloudtrail.sessionCredentialFromConsole`
    FROM (
             SELECT explode(Records) as exploded_records
             FROM ${table}
         ) t;
WITH (
    auto_refresh = true,
    refresh_interval = '5 Seconds'
)