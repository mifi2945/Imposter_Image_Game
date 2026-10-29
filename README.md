# Imposter_Image_Game
## CSC4201 — Project Requirements
For this project, you are again part of a 2-4 person team building a microservice application. This time, you have some additional freedom, in choosing your team, and in designing your application. You are allowed/encouraged to choose your own application—subject to time constraints and the minimal require- ments later in this document. A suggested project is described later in this document as a fallback.
### Timeline
Below is a list of dates and milestones for the project.
- October 29, 2026 Please have decided what teams you are on, an record it in Canvas. And, please provide a 1 to 3 paragraph description of the application you intend to implement when possible.
- November 12, 2026 Preliminary Planning. Here you should have:
  - A diagram showing what services comprise your application, and how they depend on one an- other. For example, the miniproject could perhaps be diagrammed as:
  - What communication style and protocol each service will use, and which (if any) tools or brokers will be used for the communication. N.B. I recommend that you restrict the project to at most one synchronous and at most one asynchronous protocol.
  - Brief descriptions of the public API for each service (methods, endpoints, schema).
  - At least one saga tracing a multiservice “transaction.” These need not be final, but should be well-enough developed to plausibly describe your final result.
- November 19, 2026 Have the infrastructure and pipeline set up to automatically deploy each microservice to the same Kubernetes cluster. It is easier, but more expensive, to use a managed cluster. (You may also consider additional tooling for gateways, service meshes, Knative, etc.)  
At this point the services themselves can be skeletal—they don’t need full functionality, but should exist as services. Independent build/deploy is preferred.  
Here, you should also have added me to any/all repositories.
- December 3, 2026 Begin demos of working projects. This is not a deadline, but I would not expect the demo of a working project before this.
- December 10, 2026 Be ready to submit the results of performance tests. How many requests/s can your application manage? When under load, are there pointsin the design which are more/less stressed?
- December 11, 2026 Last day of classes. This is a deadline. What isn’t in by now, isn’t in.
### Requirements and Recommendations
Your application should:
- Allow “external” users. This can be through an exposed API, a dedicated frontend, or both.
- Require authorization. That is, there should be operations that certain users can perform and other users cannot. Users should have some authentication mechanism to get the required authorizations.
- Distribute responsibilities meaningfully to the services. Each service should encapsulate a design decision (and you should know what those decisions are). A central orchestrator (e.g. the frontend) telling all other services what to do) is a warning indicator in this regard.
- Be scaled appropriately. I would expect 1-3 services per team member.
- Be deployed as a single project in a single Kubernetes cluster.
- Be built and deployed independently.
### Default Application
Create a blogging platform. Some useful features:
- Role-based Access Control. Users can be one of poster Can add new posts to the blog. A post has a title, formatted text, and a selection of categories. commenter Can comment on posts. user No login required. Can read posts, but cannot add or edit admin Full control over site, including formatting defaults, policies, etc.
- Posts can be listed by category, by poster, by date, or searched by keyword.
- Users can be notified of new posts (or even of replies to their comments).
- Each post has a list of recommended “related” posts. This list is neither exclusive nor exhaustive. Feel free to omit some of the functionality and/or add ad- ditional (e.g. subscriber-only posts, RSS feeds, comment feed, external links to other blogs, human–or ai–moderation of comments, etc.).
