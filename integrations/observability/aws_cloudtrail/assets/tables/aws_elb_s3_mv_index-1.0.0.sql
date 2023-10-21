CREATE VIEW AS
    SELECT
        eventVersion AS "aws.cloudtrail.eventVersion",
        userIdentity.type AS "aws.cloudtrail.userIdentity.type",
        userIdentity.principalId AS "aws.cloudtrail.userIdentity.principalId",
        userIdentity.arn AS "aws.cloudtrail.userIdentity.arn",
        userIdentity.accountId AS "aws.cloudtrail.userIdentity.accountId",
        userIdentity.accessKeyId AS "aws.cloudtrail.userIdentity.accessKeyId",
        userIdentity.userName AS "aws.cloudtrail.userIdentity.userName",
        userIdentity.sessionContext.attributes.creationDate AS "aws.cloudtrail.userIdentity.sessionContext.attributes.creationDate",
        userIdentity.sessionContext.attributes.mfaAuthenticated AS "aws.cloudtrail.userIdentity.sessionContext.attributes.mfaAuthenticated",
        eventTime AS "aws.cloudtrail.eventTime",
        eventSource AS "aws.cloudtrail.eventSource",
        eventName AS "aws.cloudtrail.eventName",
        awsRegion AS "aws.cloudtrail.awsRegion",
        sourceIPAddress AS "aws.cloudtrail.sourceIPAddress",
        userAgent AS "aws.cloudtrail.userAgent",
        requestParameters.name AS "aws.cloudtrail.requestParameters.name",
        responseElements AS "aws.cloudtrail.responseElements",
        requestID AS "aws.cloudtrail.requestID",
        eventID AS "aws.cloudtrail.eventID",
        readOnly AS "aws.cloudtrail.readOnly",
        eventType AS "aws.cloudtrail.eventType",
        managementEvent AS "aws.cloudtrail.managementEvent",
        recipientAccountId AS "aws.cloudtrail.recipientAccountId",
        eventCategory AS "aws.cloudtrail.eventCategory",
        tlsDetails.tlsVersion AS "aws.cloudtrail.tlsDetails.tlsVersion",
        tlsDetails.cipherSuite AS "aws.cloudtrail.tlsDetails.cipherSuite",
        tlsDetails.clientProvidedHostHeader AS "aws.cloudtrail.tlsDetails.clientProvidedHostHeader",
        sessionCredentialFromConsole AS "aws.cloudtrail.sessionCredentialFromConsole"
    FROM ${table};
WITH (
    auto_refresh = true,
    refresh_interval = '5 Seconds'
)