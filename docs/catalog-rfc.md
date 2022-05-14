
# OpenSearch Catalog RFC

## Introduction

The OpenSearch Catalog is designed to make it easier for developers and community to contribute, search and install artifacts like plugins, visualization dashboards, ingestion to visualization content packs (data pipeline configurations, normalization, ingestion, dashboards). The OpenSearch Catalog does this by providing a searchable catalog of community contributed OpenSearch artifacts and [projects](https://opensearch.org/community_projects) that users can browse, rate and download from the project website, OpenSearch CLI, and OpenSearch Dashboards. Users can install and update artifacts with a single click from OpenSearch Dashboards or by running an install/update command from OpenSearch CLI. When the artifacts have updates, they are highlighted in OpenSearch Dashboards to help users discover the latest versions of artifacts.

## Problem

OpenSearch and OpenSearch Dashboards can be overwhelming to get started with as the depth of features and functionality requires expertise that takes time to understand and master. It is also difficult to discover additional functionality that is contained in plugins that are spread out through the ecosystem and find good examples to be reused for different parts of OpenSearch and OpenSearch Dashboards. The growing number of features in various plugins like Alerting, Index Management, Anomaly Detection, Observability among others makes OpenSearch a powerful search and log analytics platform. While these features add a lot of value to users and admins, they require a level of understanding of OpenSearch fundamental components like Data Ingestion pipelines, Data Normalization, Mappers,Indices, Shards, , Dashboards.

## Solution

We are proposing to build an OpenSearch Catalog for OpenSearch and OpenSearch Dashboards to help users with sharing their artifacts like plugins, visualization dashboards, content packs, alerting monitors, index management policies, anomaly detection detectors, mappers among others for the benefit for the community along with helping users discover artifacts that can be installed with 1-click . The OpenSearch Catalog will provide contributors a place to publish their artifacts to see wide adoption from all users of OpenSearch and OpenSearch Dashboards and provide end users with a place to search, review, rate, and comment on artifacts.

**OpenSearch Catalog**

1. Developers should be able to publish their artifacts to OpenSearch catalog.
2. Multiple versions of a single artifact (plugin/dashboard) should be available to download in the event a user is using an older OpenSearch distribution.
3. Users should be able to install artifacts from OpenSearch Dashboards, CLI, and OpenSearch website.
4. Users should be able to rate and browse artifacts from OpenSearch Dashboards and OpenSearch website.
5. Artifact updates should be highlighted to cluster administrators via OpenSearch Dashboards and the CLI.

The goal is to reduce the friction from spinning up a new cluster to immediately deriving business value from being able to easily install multiple artifacts that have been created by the community.

## OpenSearch Catalog components

The OpenSearch catalog will consist of the following components to support authentication, install, validation, search, and curation (ratings, reviews).

**OpenSearch catalog website**: The website will be the central place for developers to contribute and upload artifacts. It will support different functions of login, upload, browse, search, install, rate, review, comment, validate and curate the content.

**OpenSearch Dashboards plugin**: The OpenSearch Dashboards will have a UI plugin for users and admins of OpenSearch clusters to search and install a plugin or define an alerting monitor or index management policy.

**Catalog plugin:** The catalog plugin will be a back end plugin to maintain the metadata around installed artifacts (create/install, update, remove).

**CLI**: The OpenSearch CLI lets users to package and upload artifacts into the catalog.

 **Validation Framework**: The validation framework will ensure the uploaded artifact is tested and compatible with different versions of OpenSearch.

**Curation:** The curation will support the workflow of content approval before being available in the catalog.

### Artifacts

Artifacts are components of OpenSearch and OpenSearch Dashboards that allow users to immediately derive value without having to the understand complexity of installing and operating specific features on their clusters They also provide extra functionality (plugins) for the user to enhance the base OpenSearch and OpenSearch Dashboard distributions. The OpenSearch Catalog provides a searchable catalog of community contributed OpenSearch artifacts that users can browse, rate, and download from the project website, the OpenSearch CLI, and OpenSearch Dashboards.

Catalog allow users to:

* Install new plugins that provide additional functionality
* Add pre-built Dashboards with Visualizations for common data formats
* Implement pre-defined complex queries and scripts with multiple log sources for common and advanced workloads
* Add common index mappings and templates without having to build your own
* Add common resources (e.g., monitors, policies) for installed plugins such as Alerting monitors and Index State Management policies.
* And more!


For example authors can share their common Index State Management policies that can be useful for all users of OpenSearch. Such as a policy that sets replicas to 5 before rolling over the index once it reaches 7 days of age, transitioning to a warm state where it reduces replicas, sets the index to read-only, force merges the segments to improve search, and then deleting the index after 30 days of age. For a new user this would originally take a while to learn and setup on their own, but now they can quickly view examples and install them directly on their cluster to get started with.

```
{
  "policy": {
    "description": "ingesting logs",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [
          { "replica_count": { "number_of_replicas": 5 } },
          {
            "retry": { "count": 3, "backoff": "exponential", "delay": "1h" },
            "rollover": { "min_index_age": "7d" }
          }
        ],
        "transitions": [{ "state_name": "warm" }]
      },
      {
        "name": "warm",
        "actions": [
          { "read_only": {} },
          { "replica_count": { "number_of_replicas": 1 } },
          { "force_merge": { "max_num_segments": 1 } }
        ],
        "transitions": [{
            "state_name": "delete",
            "conditions": { "min_index_age": "30d" }
		}]
      },
      {
        "name": "delete",
        "actions": [{
	        "notification": {
		        "destination": { "slack": { "url": "<url>" } },
		        "message_template": { "source": "Deleting index {{ctx.index}}" }
	        }
        }, {
            "retry": { "count": 3, "backoff": "exponential", "delay": "1h" },
            "delete": {}
		}]
      }
    ]
  }
}
```


The artifacts require a Manifest.json file which is bundled together with the artifact data and media in a zip that is then published to the OpenSearch Catalog where it will go through the publishing lifecycle before being available for public use.

### Manifest.json

The Manifest.json file is required in all artifacts zips. It contains all information required for an artifact to be published, validated, installed, and meta information to show on the catalog.

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|author	|Object	|No	|The artifact's author	|"author": { name": "Jane Smith" }	|
|dependencies	|Object	|Yes	|The dependencies of the artifact	|"dependencies": { "opensearchDependency": "^1.2.0" }	|
|description	|String	|Yes	|The artifact's description	|This is a description of my artifact	|
|icons	|Object	|No	|An object with keys to provided image names that will be used when showing an icon of the artifact	|"icons": { "48": "icon.png", "96": "icon@2x.png" }	|
|id	|String	|Yes	|The unique id/name of the artifact that will be used in the catalog URI	|my-awesome-artifact	|
|keywords	|String[]	|Yes	|List of keywords used for searching on the catalog to help find the artifact	|["awesome", "plugin", "business analytics"]	|
|license	|String	|Yes	|The license of the artifact	|Apache 2.0	|
|links	|Object[]	|No	|List of links to be displayed on the artifacts page	|[{ "name": "Project website", "url": "..." }, ...]	|
|manifest_version	|Number	|Yes	|The version of the manifest.json used	|1	|
|media	|Object[]	|No	|Images and GIFs that are displayed on the catalog for the artifact	|[{ "name" "Homepage", "description": "...", "path": "img/homepage.png" }, ...]	|
|name	|String	|Yes	|The artifacts name	|My awesome artifact	|
|path	|String	|Yes	|The path to the artifact file	|my-awesome-plugin.zip	|
|type	|String	|Yes	|The artifact's type	|Index Mapping	|
|variables	|Object	|No	|Variable substitutions for the artifact which will look for <%variable%> in the supported artifact to replace with the users input.	|"variables": { "index": { "type": "String" } }	|
|version	|String	|Yes	|The version of the artifact	|1.2.0	|

**author**

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|email	|String	|No	|Author's email	|foo@amazon.com	|
|name	|String	|No	|Author's name	|John Smith	|
|url	|String	|No	|Author's website	|https://www.amazon.com	|

**dependencies**

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|opensearchDependency	|String	|Yes	|The versions of OpenSearch this artifact supports and depends on	|^1.2.0	|
|artifact	|Object[]	|No	|Other artifacts this artifact depends on	|[{ "id": "artifact-id", "version": "1.3.0" }, ...]	|

**artifacts**

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|id	|String	|Yes	|The id of the artifact	|awesome-plugin	|
|version	|String	|Yes	|The version of the artifact	|5.2.3	|

**links**

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|name	|String	|Yes	|The name of the link	|Project website	|
|url	|String	|Yes	|The url for the link	|https://www.amazon.com	|

**media**

|Property	|Type	|Mandatory	|Description	|Example	|
|---	|---	|---	|---	|---	|
|name	|String	|Yes	|The name of the image	|Homepage	|
|description	|String	|Yes	|The description of the image used for alt text for accessibility	|Homepage view of awesome-plugin showing graph of business analytics	|
|path	|String	|Yes	|The path to the image	|img/homepage.png	|

### Artifact Types

This is not an exhaustive list of artifact types we plan to support, but some we see immediate benefit for the community.

|Extension Type	|Notes	|
|---	|---	|
|Plugins	|A plugin is a developed piece of software that is enhancing OpenSearch or OpenSearch Dashboards with specific functionality. It lives in a code repository and creates an artifact that can be shared.	|
|Dashboards	|A dashboard is a collection of Visualizations.	|
|Visualizations	|Single Visualizations of different types.	|
|Queries	|Queries can be time consuming to put together and are infact reusable when the data is formatted the same which is common.	|
|Scripts (e.g. painless)	|In spite of the name, painless scripts are incredibly painful for users to write. Having a place where users could share common patterns for scripts would benefit everyone.	|
|Index Templates-Component Templates	|The index template APIs follow a composable component template pattern where you create can different sub templates (component templates) and compose them together into a larger index template. These could be shared by providing common settings and mappings to be used for indices.	|
|Index Mappings	|When the data being ingested is of the same type/format then a common index mapping could be used for most users.	|
|Index State Management Policies	|ISM Policies are shareable for different use cases	|
|Anomaly Detection Detectors	|Anomaly detectors can be reused across clusters if the underlying data is in the same format	|
|Alerting Monitors-Triggers	|If users have the same format of data ingested and they want to alarm on it then a lot of them will want the same type of monitors and alarms/triggers.	|
|Custom	|We might not capture every type of artifact users want to be able to share. Instead of waiting for us to add support the custom type allows people to publish a custom type artifact that can still be shared with users	|

### Tooling

We plan to provide tooling to support authors with building and publishing their artifacts and for users to download and manage their installed artifacts. To start with we will enhance the [opensearch-cli](https://github.com/opensearch-project/opensearch-cli) with new APIs and commands that help bundle artifacts into the required format to be published. It will also provide functionality for helping the author get the artifact through the publishing lifecycle until it is officially published to the public.

```
// Create a new artifact locally called my-awesome-query
opensearch-cli artifacts create my-awesome-query --type query --profile prod
```

We plan to provide built-in support into OpenSearch Dashboards to easily export your built artifact types so they can be published such as visualizations and dashboards.

Lastly we will add support for a new Gradle plugin that plugin developers can add to their plugin for easily building the artifacts zip and publishing directly using Gradle to the catalog.

```
// Command will bundle the plugin, Manifest.json, and any required media files
// into an artifact zip to then be published to the catalog
./gradlew assemble artifact
...
./gradlew publishToOpenSearchCatalog
```

### Publishing

For publishing we require users to create an account using one of the common social logins such as GitHub, Google, or Facebook. Once an account is created there will be an author portal on the OpenSearch Catalog to manage artifacts that are in the publishing process or already published.

The publishing process helps ensure the quality of artifacts on the catalog stay high and helps the author follow best practices. Authors can view and work through the publishing process directly from the OpenSearch Catalog or use the CLI.

When an artifact is first published it will be in the DRAFT stage where it will go through validations, security checks, and allow the author to make edits and review.

The validations of an artifact will verify that the artifact actually works for the supported versions listed by the author. This ensures that you don’t accidentally install an artifact that is broken for your version of OpenSearch.

We will also do security scans of all published artifacts periodically to help protect clusters from security exploits. This will happen during the publishing process and periodically after.

Once the author feels it is ready it will be submitted for review and enter the REVIEW stage where it will be officially reviewed.

If there are any comments from the review board that they feel are required then the author will be notified and the artifact will enter into a REVISION stage.

Once the comments are addressed and the review board signs off the artifact will enter the final PUBLISHED stage where it will become available to the public on the OpenSearch Catalog.

### Discovering

The OpenSearch Catalog will be hosted as a web application that can be independently browsed through to discover new artifacts. Users can directly download artifacts from the OpenSearch Catalog and use the CLI tooling to install.

We also plan to provide an OpenSearch Dashboards plugin that will allow users to browse the OpenSearch Catalog directly from OpenSearch Dashboards. The eventual goal is to have this plugin provide a simplified installation process by introducing one-click installs directly from the UI. Users will be able to browse artifacts and click install to have it immediately installed in their cluster.

We plan to not require users to have an account to browse and download artifacts from the catalog. But, if users want to be able to review, rate, and comment on artifacts they must be logged in.

### Installing and uninstalling

We are going to provide two mechanisms for users to install artifacts on to their OpenSearch clusters. 
Outside the cluster environment and inside the cluster environment. 

We will have a opensearch-cli tool which can interact with the OpenSearch catalog and the cluster on behalf of the user to list the artifacts available and install artifact on behalf of the user. This tool can be used as an ad hoc installer of artifacts. 

```
// This will go and fetch the my-awesome-artifact from the catalog
// and start the installation process for it
opensearch-cli artifacts install my-awesome-artifact --profile prod`
```

Alternatively we will also provide an OpenSearch dashboard plugin that is part of the OpenSearch cluster which can provide users with ability to interact with the OpenSearch catalog to list down the artifacts. Along with this we will have a OpenSearch plugin that can install any applicable extension that the user desires on to the cluster . These two combined will provide a more streamlined user experience where users can see the list of artifacts installed on the cluster at a given moment, browse the catalog artifacts and install plugins from the artifact catalog by clicking a button.

For initial phase users won’t be able to install plugins through either of the channels, but just download the plugin from catalog.

### Distributions

One challenge we want to tackle is providing support for companies and users that have their clusters deployed in such a way where they cannot directly connect to the OpenSearch Catalog over the internet. To do this we plan to provide distributions of the OpenSearch Catalog such that end users can directly host their own catalog that is essentially a mirror of the official OpenSearch Catalog. We plan to provide daily dumps of all artifacts split by type so they can be downloaded and hosted internally for their mirrored catalog to pull from.

The mirrored catalogs will have trimmed down functionally as we do not want to bifurcate ratings, reviews, comments, and accounts. It will provide the ability to browse, download, and install artifacts.

## Providing Feedback

We seek comments and feedback on the proposed design for OpenSearch Catalog. Some specific questions we're seeking feedback on include:

* What other types of artifacts would you like to see in the catalog?
* Opt-in vs Opt-out? Would you prefer the OpenSearch Dashboards Catalog plugin to be turned on by default allowing users to browse artifacts from the online catalog or would you prefer to have it disabled by default and require an admin of the cluster to enable it before it can be used?
* Would you expect OpenSearch, and in the future, elected community leaders to curate and approve artifacts before they are allowed to show up in the catalog? 
* Should we require all artifact's sources to be public so builds can be traced or built by the OpenSearch catalog itself? Such as requiring a GitHub repository that can be used to build the artifact.
