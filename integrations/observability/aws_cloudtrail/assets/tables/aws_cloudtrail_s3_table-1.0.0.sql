CREATE EXTERNAL TABLE IF NOT EXISTS ${table} (
    Records ARRAY<STRUCT<
        awsRegion: STRING,
        eventCategory: STRING,
        eventID: STRING,
        eventName: STRING,
        eventSource: STRING,
        eventTime: STRING,
        eventType: STRING,
        eventVersion: STRING,
        managementEvent: STRING,
        readOnly: BOOLEAN,
        recipientAccountId: STRING,
        requestID: STRING,
        requestParameters: STRUCT<
            assumeRolePolicyDocument: STRING,
            description: STRING,
            roleName: STRING
        >,
        responseElements: STRUCT<
            role: STRUCT<
                arn: STRING,
                assumeRolePolicyDocument: STRING,
                createDate: STRING,
                path: STRING,
                roleId: STRING,
                roleName: STRING
                >
        >,
        sessionCredentialFromConsole: STRING,
        sourceIPAddress: STRING,
        tlsDetails: STRUCT<
            cipherSuite: STRING,
            clientProvidedHostHeader: STRING,
            tlsVersion: STRING
        >,
        userAgent: STRING,
        userIdentity: STRUCT<
            accessKeyId: STRING,
            accountId: STRING,
            arn: STRING,
            principalId: STRING,
            sessionContext: STRUCT<
                attributes: STRUCT<
                    creationDate: STRING,
                    mfaAuthenticated: STRING
                >
            >,
            type: STRING,
            userName: STRING
        >
    >>
) USING json OPTIONS ('path' ${bucket});