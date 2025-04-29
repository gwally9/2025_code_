Monitoring & ObservabilityTooling Assessment

OVERVIEW
- Questionnaires were distributed into the organization with the aim of ascertaining the instrumentation methods deployed for application monitoring.  An additional series of questions, which solicited refinement for some of the initial questions was also distributed.
- Several interactive session were facilitated which demonstrated the various operational tools utilized during the reported incidents time periods, along with a generalized walk-throughs of the tools’ configuration and capabilities that provide a holistic overview of the operational resources.
- Lastly, topological discussion were held that permitted us to gather a fundamental overview of the compute platforms deployed in support of the applications.

Resources

- The team guided us through the plethora of parameters, patterns, and visuals within Dynatrace. A vast majority of the inherent capabilities of the APM, Dynatrace were enabled and leveraged within the organization, in order to facilitate a robust diagnostic and operational stance of the applications.
- Conversely, a tightly coupled integration into the Dynatrace was not deployed and reliance upon other tools and techniques are utilized to aid in understanding a holistic overview of the entire.
- Specifically, the engineering team had to relied upon:
    - vCenter, for management of ESXi cluster resources; Hosts, Guests, Metric data, etc.
    - Qpasa - for observation of Messaging resources - performant data, etc.
    - Splunk - collator of service, server log data

Findings

- Reliance upon disparent monitoring platforms, can induces operational overhead and potentially elongated analysis of a situation. The causal effect can be that one can not correlate the underlying problem, and is open to interpretation.
- Dynatrace has a finite retention of the aggregated data collected thereby forcing one to derive conclusions or corrective actions within a time box.  Any attempt to investigate deviations from an operational norm has to be investigated using other resources and doesn’t encompass data similar to that ingested by Dynatrace.
- Log aggregation, from servers hosting the application, to my understanding are not collected into Dynatrace, thereby forcing the engineers to examine potential event data within another application stack (Splunk)
- There’s a backlog of features ear-marked for enablement within Dynatrace that may provide additional robustness to the capabilities of the APM resources.  Leveraging these capabilities may solidify a comprehensive solution.

Conclusion

- Examine the features of Dynatrace that are back logged for enablement and derive a timeline for enablement
- Consider a cohesive, say single pane of glass observability platform that provides a cohesive set of resource for issue/event analysis
- If possible, consider adding additional data collection and visualization within Dynatrace that displays workload characteristics of the messaging infrastructure from a near realtime perspective
- Possibly adjusting KPI thresholds on critical resources to be slightly more sensitive to abnormal or saturation conditions. 