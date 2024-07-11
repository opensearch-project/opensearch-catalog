```markdown
# OpenSearch Java Client Documentation

The OpenSearch Java client allows you to interact with your OpenSearch clusters through Java methods and data structures rather than HTTP methods and raw JSON. This guide illustrates how to connect to OpenSearch, index documents, and run queries.

## Installing the Client

### Using Apache HttpClient 5 Transport
Add the following dependencies to your `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.8.1</version>
</dependency>
<dependency>
  <groupId>org.apache.httpcomponents.client5</groupId>
  <artifactId>httpclient5</artifactId>
  <version>5.2.1</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-java:2.8.1'
  implementation 'org.apache.httpcomponents.client5:httpclient5:5.2.1'
}
```

### Using RestClient Transport
Add the following dependencies to your `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-rest-client</artifactId>
  <version>2.15.0</version>
</dependency>
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.6.0</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-rest-client:2.15.0'
  implementation 'org.opensearch.client:opensearch-java:2.6.0'
}
```

## Security
Configure the application's truststore to connect to the Security plugin:
```bash
keytool -import <path-to-cert> -alias <alias-to-call-cert> -keystore <truststore-name>
```

## Sample Data
Define an `IndexData` class:
```java
static class IndexData {
  private String firstName;
  private String lastName;

  public IndexData(String firstName, String lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  public String getFirstName() { return firstName; }
  public void setFirstName(String firstName) { this.firstName = firstName; }
  public String getLastName() { return lastName; }
  public void setLastName(String lastName) { this.lastName = lastName; }

  @Override
  public String toString() {
    return String.format("IndexData{first name='%s', last name='%s'}", firstName, lastName);
  }
}
```

## Initializing the Client with SSL and TLS

### Using Apache HttpClient 5 Transport
```java
import javax.net.ssl.SSLContext;
import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.ssl.SSLContextBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.httpclient5.ApacheHttpClient5TransportBuilder;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final SSLContext sslcontext = SSLContextBuilder.create().loadTrustMaterial(null, (chains, authType) -> true).build();
    final ApacheHttpClient5TransportBuilder builder = ApacheHttpClient5TransportBuilder.builder(host)
      .setHttpClientConfigCallback(httpClientBuilder -> {
        return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
      });

    final OpenSearchClient client = new OpenSearchClient(builder.build());
  }
}
```

### Using RestClient Transport
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.rest_client.RestClientTransport;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final RestClient restClient = RestClient.builder(host).setHttpClientConfigCallback(httpClientBuilder -> {
      return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
    }).build();

    final OpenSearchClient client = new OpenSearchClient(new RestClientTransport(restClient, new JacksonJsonpMapper()));
  }
}
```

## Connecting to Amazon OpenSearch Service
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.es.amazonaws.com", "es", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Connecting to Amazon OpenSearch Serverless
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.aoss.amazonaws.com", "aoss", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Creating an Index
```java
String index = "sample-index";
CreateIndexRequest createIndexRequest = new CreateIndexRequest.Builder().index(index).build();
client.indices().create(createIndexRequest);

IndexSettings indexSettings = new IndexSettings.Builder().autoExpandReplicas("0-all").build();
PutIndicesSettingsRequest putIndicesSettingsRequest = new PutIndicesSettingsRequest.Builder().index(index).value(indexSettings).build();
client.indices().putSettings(putIndicesSettingsRequest);
```

## Indexing Data
```java
IndexData indexData = new IndexData("first_name", "Bruce");
IndexRequest<IndexData> indexRequest = new IndexRequest.Builder<IndexData>().index(index).id("1").document(indexData).build();
client.index(indexRequest);
```

## Searching for Documents
```java
SearchResponse<IndexData> searchResponse = client.search(s -> s.index(index), IndexData.class);
for (int i = 0; i< searchResponse.hits().hits().size(); i++) {
  System.out.println(searchResponse.hits().hits().get(i).source());
}
```

## Deleting a Document
```java
client.delete(b -> b.index(index).id("1"));
```

## Deleting an Index
```java
DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest.Builder().index(index).build();
DeleteIndexResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest);
```

## Sample Program
The following sample program creates a client, adds an index with non-default settings, inserts a document, searches for the document, deletes the document, and then deletes the index:
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.base.RestClientTransport;
import org.opensearch.client.base.Transport;
import org.opensearch.client.json.jackson.JacksonJsonpMapper;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch._global.IndexRequest;
import org.opensearch.client.opensearch._global.IndexResponse;
import org.opensearch.client.opensearch._global.SearchResponse;
import org.opensearch.client.opensearch.indices.*;
import org.opensearch.client.opensearch.indices.put_settings.IndexSettingsBody;

import java.io.IOException;

public class OpenSearchClientExample {
  public static void main(String[] args) {
    RestClient restClient = null;
    try {
      System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
      System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

      final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
      credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials("admin", "admin"));

      restClient = RestClient.builder(new HttpHost

```markdown
# OpenSearch Java Client Documentation

The OpenSearch Java client allows you to interact with your OpenSearch clusters through Java methods and data structures. This guide illustrates how to connect to OpenSearch, index documents, and run queries.

## Installing the Client

### Using Apache HttpClient 5 Transport
Add the following dependencies to your `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.8.1</version>
</dependency>
<dependency>
  <groupId>org.apache.httpcomponents.client5</groupId>
  <artifactId>httpclient5</artifactId>
  <version>5.2.1</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-java:2.8.1'
  implementation 'org.apache.httpcomponents.client5:httpclient5:5.2.1'
}
```

### Using RestClient Transport
Add the following dependencies to your `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-rest-client</artifactId>
  <version>2.15.0</version>
</dependency>
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.6.0</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-rest-client:2.15.0'
  implementation 'org.opensearch.client:opensearch-java:2.6.0'
}
```

## Security
Configure the application's truststore to connect to the Security plugin:
```bash
keytool -import <path-to-cert> -alias <alias-to-call-cert> -keystore <truststore-name>
```

## Sample Data
Define an `IndexData` class:
```java
static class IndexData {
  private String firstName;
  private String lastName;

  public IndexData(String firstName, String lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  public String getFirstName() { return firstName; }
  public void setFirstName(String firstName) { this.firstName = firstName; }
  public String getLastName() { return lastName; }
  public void setLastName(String lastName) { this.lastName = lastName; }

  @Override
  public String toString() {
    return String.format("IndexData{first name='%s', last name='%s'}", firstName, lastName);
  }
}
```

## Initializing the Client with SSL and TLS

### Using Apache HttpClient 5 Transport
```java
import javax.net.ssl.SSLContext;
import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.ssl.SSLContextBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.httpclient5.ApacheHttpClient5TransportBuilder;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final SSLContext sslcontext = SSLContextBuilder.create().loadTrustMaterial(null, (chains, authType) -> true).build();
    final ApacheHttpClient5TransportBuilder builder = ApacheHttpClient5TransportBuilder.builder(host)
      .setHttpClientConfigCallback(httpClientBuilder -> {
        return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
      });

    final OpenSearchClient client = new OpenSearchClient(builder.build());
  }
}
```

### Using RestClient Transport
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.rest_client.RestClientTransport;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final RestClient restClient = RestClient.builder(host).setHttpClientConfigCallback(httpClientBuilder -> {
      return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
    }).build();

    final OpenSearchClient client = new OpenSearchClient(new RestClientTransport(restClient, new JacksonJsonpMapper()));
  }
}
```

## Connecting to Amazon OpenSearch Service
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.es.amazonaws.com", "es", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Connecting to Amazon OpenSearch Serverless
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.aoss.amazonaws.com", "aoss", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Creating an Index
```java
String index = "sample-index";
CreateIndexRequest createIndexRequest = new CreateIndexRequest.Builder().index(index).build();
client.indices().create(createIndexRequest);

IndexSettings indexSettings = new IndexSettings.Builder().autoExpandReplicas("0-all").build();
PutIndicesSettingsRequest putIndicesSettingsRequest = new PutIndicesSettingsRequest.Builder().index(index).value(indexSettings).build();
client.indices().putSettings(putIndicesSettingsRequest);
```

## Indexing Data
```java
IndexData indexData = new IndexData("first_name", "Bruce");
IndexRequest<IndexData> indexRequest = new IndexRequest.Builder<IndexData>().index(index).id("1").document(indexData).build();
client.index(indexRequest);
```

## Searching for Documents
```java
SearchResponse<IndexData> searchResponse = client.search(s -> s.index(index), IndexData.class);
for (int i = 0; i< searchResponse.hits().hits().size(); i++) {
  System.out.println(searchResponse.hits().hits().get(i).source());
}
```

## Deleting a Document
```java
client.delete(b -> b.index(index).id("1"));
```

## Deleting an Index
```java
DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest.Builder().index(index).build();
DeleteIndexResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest);
```

## Sample Program
The following sample program creates a client, adds an index with non-default settings, inserts a document, searches for the document, deletes the document, and then deletes the index:
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.base.RestClientTransport;
import org.opensearch.client.base.Transport;
import org.opensearch.client.json.jackson.JacksonJsonpMapper;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch._global.IndexRequest;
import org.opensearch.client.opensearch._global.IndexResponse;
import org.opensearch.client.opensearch._global.SearchResponse;
import org.opensearch.client.opensearch.indices.*;
import org.opensearch.client.opensearch.indices.put_settings.IndexSettingsBody;

import java.io.IOException;

public class OpenSearchClientExample {
  public static void main(String[] args) {
    RestClient restClient = null;
    try {
      System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
      System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

      final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
      credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials("admin", "admin"));

      restClient = RestClient.builder(new HttpHost("localhost", 9200,

```markdown
# OpenSearch Java Client Documentation

The OpenSearch Java client allows interaction with OpenSearch clusters using Java methods and data structures.

## Installing the Client

### Using Apache HttpClient 5 Transport
Add to `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.8.1</version>
</dependency>
<dependency>
  <groupId>org.apache.httpcomponents.client5</groupId>
  <artifactId>httpclient5</artifactId>
  <version>5.2.1</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-java:2.8.1'
  implementation 'org.apache.httpcomponents.client5:httpclient5:5.2.1'
}
```

### Using RestClient Transport
Add to `pom.xml`:
```xml
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-rest-client</artifactId>
  <version>2.15.0</version>
</dependency>
<dependency>
  <groupId>org.opensearch.client</groupId>
  <artifactId>opensearch-java</artifactId>
  <version>2.6.0</version>
</dependency>
```
For Gradle:
```gradle
dependencies {
  implementation 'org.opensearch.client:opensearch-rest-client:2.15.0'
  implementation 'org.opensearch.client:opensearch-java:2.6.0'
}
```

## Security
Configure the application's truststore to connect to the Security plugin:
```bash
keytool -import <path-to-cert> -alias <alias-to-call-cert> -keystore <truststore-name>
```

## Sample Data
Define an `IndexData` class:
```java
static class IndexData {
  private String firstName;
  private String lastName;

  public IndexData(String firstName, String lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }

  public String getFirstName() { return firstName; }
  public void setFirstName(String firstName) { this.firstName = firstName; }
  public String getLastName() { return lastName; }
  public void setLastName(String lastName) { this.lastName = lastName; }

  @Override
  public String toString() {
    return String.format("IndexData{first name='%s', last name='%s'}", firstName, lastName);
  }
}
```

## Initializing the Client with SSL and TLS

### Using Apache HttpClient 5 Transport
```java
import javax.net.ssl.SSLContext;
import org.apache.hc.client5.http.auth.AuthScope;
import org.apache.hc.client5.http.auth.UsernamePasswordCredentials;
import org.apache.hc.client5.http.impl.auth.BasicCredentialsProvider;
import org.apache.hc.core5.http.HttpHost;
import org.apache.hc.core5.ssl.SSLContextBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.httpclient5.ApacheHttpClient5TransportBuilder;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final SSLContext sslcontext = SSLContextBuilder.create().loadTrustMaterial(null, (chains, authType) -> true).build();
    final ApacheHttpClient5TransportBuilder builder = ApacheHttpClient5TransportBuilder.builder(host)
      .setHttpClientConfigCallback(httpClientBuilder -> {
        return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
      });

    final OpenSearchClient client = new OpenSearchClient(builder.build());
  }
}
```

### Using RestClient Transport
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.transport.rest_client.RestClientTransport;

public class OpenSearchClientExample {
  public static void main(String[] args) throws Exception {
    System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
    System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

    final HttpHost host = new HttpHost("https", "localhost", 9200);
    final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(new AuthScope(host), new UsernamePasswordCredentials("admin", "admin".toCharArray()));

    final RestClient restClient = RestClient.builder(host).setHttpClientConfigCallback(httpClientBuilder -> {
      return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
    }).build();

    final OpenSearchClient client = new OpenSearchClient(new RestClientTransport(restClient, new JacksonJsonpMapper()));
  }
}
```

## Connecting to Amazon OpenSearch Service
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.es.amazonaws.com", "es", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Connecting to Amazon OpenSearch Serverless
```java
SdkHttpClient httpClient = ApacheHttpClient.builder().build();
OpenSearchClient client = new OpenSearchClient(new AwsSdk2Transport(httpClient, "search-...us-west-2.aoss.amazonaws.com", "aoss", Region.US_WEST_2, AwsSdk2TransportOptions.builder().build()));
InfoResponse info = client.info();
System.out.println(info.version().distribution() + ": " + info.version().number());
httpClient.close();
```

## Creating an Index
```java
String index = "sample-index";
CreateIndexRequest createIndexRequest = new CreateIndexRequest.Builder().index(index).build();
client.indices().create(createIndexRequest);

IndexSettings indexSettings = new IndexSettings.Builder().autoExpandReplicas("0-all").build();
PutIndicesSettingsRequest putIndicesSettingsRequest = new PutIndicesSettingsRequest.Builder().index(index).value(indexSettings).build();
client.indices().putSettings(putIndicesSettingsRequest);
```

## Indexing Data
```java
IndexData indexData = new IndexData("first_name", "Bruce");
IndexRequest<IndexData> indexRequest = new IndexRequest.Builder<IndexData>().index(index).id("1").document(indexData).build();
client.index(indexRequest);
```

## Searching for Documents
```java
SearchResponse<IndexData> searchResponse = client.search(s -> s.index(index), IndexData.class);
for (int i = 0; i< searchResponse.hits().hits().size(); i++) {
  System.out.println(searchResponse.hits().hits().get(i).source());
}
```

## Deleting a Document
```java
client.delete(b -> b.index(index).id("1"));
```

## Deleting an Index
```java
DeleteIndexRequest deleteIndexRequest = new DeleteIndexRequest.Builder().index(index).build();
DeleteIndexResponse deleteIndexResponse = client.indices().delete(deleteIndexRequest);
```

## Sample Program
The following sample program creates a client, adds an index with non-default settings, inserts a document, searches for the document, deletes the document, and then deletes the index:
```java
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.opensearch.client.RestClient;
import org.opensearch.client.RestClientBuilder;
import org.opensearch.client.base.RestClientTransport;
import org.opensearch.client.base.Transport;
import org.opensearch.client.json.jackson.JacksonJsonpMapper;
import org.opensearch.client.opensearch.OpenSearchClient;
import org.opensearch.client.opensearch._global.IndexRequest;
import org.opensearch.client.opensearch._global.IndexResponse;
import org.opensearch.client.opensearch._global.SearchResponse;
import org.opensearch.client.opensearch.indices.*;
import org.opensearch.client.opensearch.indices.put_settings.IndexSettingsBody;

import java.io.IOException;

public class OpenSearchClientExample {
  public static void main(String[] args) {
    RestClient restClient = null;
    try {
      System.setProperty("javax.net.ssl.trustStore", "/full/path/to/keystore");
      System.setProperty("javax.net.ssl.trustStorePassword", "password-to-keystore");

      final BasicCredentialsProvider credentialsProvider = new BasicCredentialsProvider();
      credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials("admin", "admin"));

      restClient = RestClient.builder(new HttpHost("localhost", 9200,
```