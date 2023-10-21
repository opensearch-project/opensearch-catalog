CREATE EXTERNAL TABLE IF NOT EXISTS ${table} (
    Records ARRAY<STRUCT<
        eventVersion: STRING,
        userIdentity: STRUCT<
            type: STRING,
            principalId: STRING,
            arn: STRING,
            accountId: STRING,
            accessKeyId: STRING,
            userName: STRING,
            sessionContext: STRUCT<
                sessionIssuer: STRUCT<>,
                webIdFederationData: STRUCT<>,
                attributes: STRUCT<
                    creationDate: STRING,
                    mfaAuthenticated: STRING
                >
            >
        >,
        eventTime: STRING,
        eventSource: STRING,
        eventName: STRING,
        awsRegion: STRING,
        sourceIPAddress: STRING,
        userAgent: STRING,
        requestParameters: STRUCT<
            roleName: STRING,
            description: STRING,
            assumeRolePolicyDocument: STRING
        >,
        responseElements: STRUCT<
            role: STRUCT<
                assumeRolePolicyDocument: STRING,
                arn: STRING,
                roleId: STRING,
                createDate: STRING,
                roleName: STRING,
                path: STRING
            >
        >,
        requestID: STRING,
        eventID: STRING,
        readOnly: BOOLEAN,
        eventType: STRING,
        managementEvent: BOOLEAN,
        recipientAccountId: STRING,
        eventCategory: STRING,
        tlsDetails: STRUCT<
            tlsVersion: STRING,
            cipherSuite: STRING,
            clientProvidedHostHeader: STRING
        >,
        sessionCredentialFromConsole: STRING
    >>
) USING json OPTIONS ('path' ${bucket});