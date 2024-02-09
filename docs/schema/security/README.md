# Security Schems
...
## OCSF Schema
The Open Cybersecurity Schema Framework is an open-source project, delivering an extensible framework for developing schemas, along with a vendor-agnostic core security schema
The [OCSF framework](https://github.com/ocsf) is made up of a set of data types, an attribute dictionary, and the taxonomy.

### Taxonomy Constructs
There are 5 fundamental constructs of the OCSF taxonomy:

- Data Types, Attributes and Arrays
- Event Class
- Category
- Profile
- Extension
  
An attribute is a unique identifier name for a specific validatable data type, either scalar or complex.

Complex data types are termed objects. An object is a collection of contextually related attributes, usually representing an entity, and may include other objects. Each object is also a data type in OCSF. Examples of object data types are Process, Device, User, Malware and File.

**Events** in OCSF are represented by `_event` classes `_which` structure a set of attributes that attempt to describe the semantics of the event in detail. An individual event is an instance of an event class. Event classes have schema-unique IDs.
Individual events may have globally unique IDs. Each event class is grouped by category, and has a unique `category_uid` attribute value which is the category identifier.
**Categories** also have friendly name captions, such as `System Activity`, `Network Activity`, `Findings`, etc.

Event classes are grouped into categories for a number of purposes: a container for a particular event domain, documentation convenience and search, reporting, storage partitioning or access control to name a few.
**Profiles** overlay additional related attributes into event classes and objects** **allowing for cross-category event class augmentation and filtering. Event classes register for profiles that when optionally applied, can be mixed into event classes and objects, by a producer or mapper.
For example, System Activity event classes may also include attributes for malware detection or vulnerability information when an endpoint security product is the data source.
Network Activity event classes from a host computer may carry the `device`, `process` and `user` associated with the activity.
A Security Control profile or Host profile can be applied in these cases, respectively.

For additional details [review](https://github.com/ocsf/ocsf-docs/blob/main/Understanding%20OCSF.pdf).