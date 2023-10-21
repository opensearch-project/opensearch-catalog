CREATE TABLE ${table}
(
    eventVersion                 STRING,
    userIdentity                 STRUCT<
        type : STRING,
    principalId: STRING,
    arn: STRING,
    accountId: STRING,
    accessKeyId: STRING,
    userName: STRING,
    sessionContext: STRUCT< attributes: STRUCT<
        creationDate: STRING,
    mfaAuthenticated: STRING > >
        >,
    eventTime                    STRING,
    eventSource                  STRING,
    eventName                    STRING,
    awsRegion                    STRING,
    sourceIPAddress              STRING,
    userAgent                    STRING,
    requestParameters            STRUCT<
        name : STRING
        >,
    responseElements             STRING,
    requestID                    STRING,
    eventID                      STRING,
    readOnly                     BOOLEAN,
    eventType                    STRING,
    managementEvent              BOOLEAN,
    recipientAccountId           STRING,
    eventCategory                STRING,
    tlsDetails                   STRUCT< tlsVersion: STRING,
    cipherSuite: STRING,
    clientProvidedHostHeader: STRING >,
    sessionCredentialFromConsole STRING
) USING json OPTIONS (
  'path' ${bucket}
);
