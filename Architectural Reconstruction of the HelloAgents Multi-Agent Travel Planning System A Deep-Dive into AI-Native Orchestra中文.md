Architectural Reconstruction of the HelloAgents Multi-Agent Travel Planning System: A Deep-Dive into AI-Native Orchestration, Model Context Protocols, and Geospatial Integration

The global landscape of artificial intelligence underwent a fundamental phase shift in 2025, transitioning from the "Battle of a Hundred Models" to the "Year of Agents".[1] While the previous era focused on the scaling of foundation models, the current paradigm prioritizes the construction of autonomous, goal-oriented systems capable of interacting with the physical and digital worlds through specialized tools and multi-agent collaboration.[1, 2] At the forefront of this shift is the HelloAgents framework, a project initiated by the Datawhale community to provide a systematic, practice-oriented approach to building AI-native agents from the ground up.[1] Unlike software-engineering-oriented agents which treat large language models as mere data processing backends within rigid flowcharts, AI-native agents leverage the reasoning capabilities of the model to navigate non-linear tasks dynamically.[1] The "Intelligent Travel Planning System" serves as the primary pedagogical vehicle for this framework, illustrating the complexities of task decomposition, tool invocation via the Model Context Protocol (MCP), and real-time frontend visualization.[3]

Theoretical Foundations of Agentic Orchestration

The architectural core of a sophisticated travel planning system rests on the Orchestrator-Workers pattern, a design philosophy that mirrors human organizational structures.[4, 5] In this model, a central planning agent—often referred to as the "Brain" or "Manager"—receives a high-level user request, such as "Plan a three-day historical tour of Beijing with a moderate budget".[3, 4] This request is inherently "fuzzy" and multi-dimensional, requiring the agent to extract latent intentions and decompose them into discrete, executable sub-tasks.[3, 6]

Classification of Agent Frameworks and Workflow Patterns

Developing a multi-agent system requires a deliberate choice between high-level abstraction and low-level control. The following table provides a comparative analysis of the leading frameworks utilized in the 2025 agentic ecosystem, including the self-developed HelloAgents framework and its common alternatives used for rapid prototyping.[1, 5, 7, 8]

| Framework       | Orchestration Pattern            | Primary Advantage                           | Typical Use Case                         |
| --------------- | -------------------------------- | ------------------------------------------- | ---------------------------------------- |
| **HelloAgents** | Orchestrator-Workers (Custom)    | Systematic transparency and modularity [1]  | Educational and custom enterprise builds |
| **LangGraph**   | Cyclical Graphs / State Machines | Persistence and complex branching logic [5] | High-reliability, iterative workflows    |
| **CrewAI**      | Role-Based Collaboration         | Rich, detailed output through role-play [7] | Content generation and research          |
| **Dify / n8n**  | Process-Driven Flowcharts        | Low-code accessibility [1, 6]               | Simple automation and linear tasks       |

While HelloAgents emphasizes the "building of wheels" rather than merely using them, frameworks like LangGraph offer robust persistence and the ability to revisit nodes—a critical feature for travel planning where initial search results might necessitate a complete re-evaluation of the schedule.[1, 5] CrewAI, conversely, focuses on a sequential or hierarchical process where specialized agents like a "Researcher" or "Local Guide" contribute to a final synthesis, often resulting in more comprehensive itineraries due to the nature of role-based prompting.[5, 7, 9]

The AI-Native Shift: Beyond the Flowchart

The distinction between AI-native and process-driven systems is best observed in how the system handles environmental uncertainty.[1] A process-driven system might fail if a weather API returns an error or if a specific landmark is closed.[10] An AI-native agent, empowered by the HelloAgents architecture, utilizes its reasoning loops to diagnose the failure and pivot to an alternative plan—such as suggesting an indoor museum if rain is forecasted.[3, 10] This requires the agent to have access to a shared context and memory, allowing state information to flow between specialized sub-agents.[1, 6]

The Model Context Protocol: Standardizing the Tool Ecosystem

A primary challenge in agentic development is the "integration tax"—the repetitive effort of writing custom code to connect specific models to specific APIs.[11, 12] The Model Context Protocol (MCP) emerged as an open standard to solve this fragmentation, functioning as a universal interface for tool discovery and invocation.[11, 12] MCP allows an agent to see a catalog of available tools, understand their input schemas, and receive structured responses without the developer needing to write bespoke integration logic for every pairing.[12, 13]

Mechanics of Tool Invocation and Transport

MCP operates through a client-server architecture. The agent acts as the client, while the external service (such as the Amap/Gaode Maps API) is wrapped in an MCP server.[12] Communication typically occurs over standard input/output (stdio) for local processes or via HTTP/SSE for remote services.[14, 15]

| MCP Server Type     | Transport Mechanism | Implementation Detail                  | Deployment Scenario               |
| ------------------- | ------------------- | -------------------------------------- | --------------------------------- |
| **Standard I/O**    | `stdio`             | Subprocess persistence [14]            | Local development and CLI tools   |
| **Streamable HTTP** | `http` / `sse`      | Stateless/Persistent sessions [14, 16] | Scalable web applications         |
| **FastAPI Mount**   | `asgi`              | FastMCP integration [17]               | High-performance backend services |

The FastMCP library significantly accelerates the development of these servers by using Python decorators to register tools.[15, 18] For example, a travel agent's "Weather Tool" can be registered with a simple `@mcp.tool` decorator, where the function's docstring automatically becomes the tool's description for the LLM to understand when to invoke it.[13, 19]

Token Optimization and Context Window Management

A sophisticated travel planner may interact with dozens of tools, each with complex schemas. If all tool definitions are loaded into the LLM's context window upfront, it can lead to massive token consumption and increased latency.[11] MCP addresses this by allowing for dynamic tool loading or "meta-tools" that help the agent discover more specific tools only when needed.[16] Furthermore, by tokenizing sensitive data and filtering intermediate tool results—such as a long list of POIs where only the top five are relevant—the system maintains context efficiency.[3, 11]

The token cost *T* for a given turn in the agentic workflow can be represented by the sum of the system instructions *I*, the tool definitions *D*, and the conversation history *H*, all relative to the model's capacity:

*T*=*I*+∑*D*+*H*

In scenarios where *D* grows too large, the system must utilize "Code Execution" agents, which write scripts to process large datasets internally rather than passing every data row through the LLM's expensive attention mechanism.[7, 11]

Engineering the Seven-Day Reproduction Sprint

Reproducing the HelloAgents travel planning system in a single week requires a focused methodology that isolates core logic from peripheral features. The following sections detail the daily technical requirements and objectives for such a sprint.

Day 1: Infrastructure and API Harmonization

The initial phase is dedicated to establishing the technical baseline. This involves setting up a Python virtual environment and securing access to the necessary API keys.[1, 20] The choice of LLM is critical; for Chinese-language travel planning, models like DeepSeek are often preferred for their high cost-efficiency and strong understanding of local cultural nuances.[10] Simultaneously, the Gaode (Amap) Web Service API must be configured, with a particular focus on the "Keyword Search" and "Weather" endpoints.[21, 22]

The technical objective for Day 1 is to establish a successful "Hand-and-Brain" connection. This is verified by writing a simple Python function that queries a POI and ensuring that the LLM can correctly identify when to call that function based on a user prompt.[19, 23]

Day 2: The Orchestrator and Intention Extraction

Day 2 focuses on the "Brain" of the system. The primary task is Prompt Engineering for the Planner Agent.[3] This agent must not generate a final itinerary immediately; instead, it must output a structured JSON object representing a task decomposition.[6] This JSON serves as the internal protocol for the rest of the sprint.

| Intent Field     | Purpose                | Technical Requirement    |
| ---------------- | ---------------------- | ------------------------ |
| `destination`    | Geographical grounding | String validation        |
| `days`           | Temporal constraint    | Integer type-safety      |
| `preferences`    | Personalization weight | List of categorical tags |
| `needed_actions` | Task routing           | Mapping to MCP tools     |

A failure at this stage—such as the agent "hallucinating" an itinerary without querying the tools—will propagate through the entire system, leading to inaccurate plans.[10] Therefore, strict JSON schema enforcement via Pydantic is implemented to validate the orchestrator's output.[24]

Day 3: Function-Level Agents and MCP Encapsulation

The third day is dedicated to building the "Specialists." Following the HelloAgents pattern, the system is divided into functional agents: the Scout (POI search), the Meteorologist (weather), and the Concierge (hotel and dining).[3, 10] Each specialist is encapsulated as an MCP tool using the FastMCP framework.[13, 18]

The challenge here is "Responsibility Decoupling." The Scout agent should only worry about finding highly-rated attractions, while the Meteorologist only provides environmental data.[3] The separation of these concerns allows the orchestrator to call them in parallel or sequence, depending on the need for efficiency or accuracy.[5]

Day 4: Semantic Integration and JSON Synthesis

On Day 4, the碎片化 (fragmented) data from the various specialists is synthesized into a coherent narrative. Raw API data from Gaode Maps is often verbose and contains noise that is irrelevant to the user.[3, 22] A data cleaning layer must extract only the essential fields: name, coordinates, rating, and description.[3]

The Planner Agent then receives this cleaned data and is tasked with generating the final `Daily Itinerary JSON`. This JSON must contain the latitude and longitude for every stop to enable map visualization on the frontend.[3, 25] The logic must handle the "Traveling Salesman Problem" (TSP) heuristically, ensuring that the suggested attractions are geographically clustered to minimize travel time.[21]

Day 5: Backend Service and SSE Streaming Implementation

The fifth day transitions the system from a CLI tool to a web service. FastAPI is utilized to create an asynchronous endpoint.[18, 20] Because agentic reasoning can take substantial time, the system must use Server-Sent Events (SSE) to stream the "thought process" to the user.[26, 27]

The `StreamingResponse` in FastAPI allows the server to yield updates like "Agent is searching for historical landmarks..." or "Analyzing weather for Day 2...".[28, 29] This approach drastically improves the perceived performance and keeps the user engaged during the 30-60 second generation window.[24, 26]

| Protocol Detail | Implementation               | Purpose                               |
| --------------- | ---------------------------- | ------------------------------------- |
| **Media Type**  | `text/event-stream` [28, 30] | Informs browser of streaming data     |
| **Data Format** | `data: {json}\n\n` [28, 29]  | Standard SSE message structure        |
| **Async Loop**  | `async for / yield` [28, 31] | Non-blocking execution of agent steps |

Day 6: Frontend Development and Map Visualization

The sixth day focuses on the user interface, built with Vue3 and Vite.[3] The frontend has two primary responsibilities: form input for user preferences and the visualization of the generated itinerary.[3] The integration of the Gaode Maps JS API is the most complex task of this phase.[32]

The frontend logic must iterate through the itinerary JSON to place markers on the map and draw polylines connecting the stops for each day.[25, 33, 34] For multi-stop itineraries, marker clustering is employed to maintain visual clarity at high zoom levels.[32] Advanced markers are used to display rich content like ratings or stop numbers directly on the map.[33, 35]

Day 7: End-to-End Debugging and Prompt Tuning

The final day is reserved for integration testing and the resolution of "Hallucination" issues. A common failure in agentic systems is the agent inventing a fictional landmark if the POI tool returns no results.[10] Prompt optimization is required to instruct the agent to admit ignorance or suggest alternative cities rather than fabricating data.[10] Technical polish, such as adjusting CSS for the itinerary cards and ensuring responsive design for mobile users, completes the sprint.[3]

Geospatial Data Processing and API Integration

The success of the HelloAgents travel planner is contingent on the high-fidelity integration of the Amap (Gaode Maps) Web Service API.[21, 22] This integration is not a simple passthrough; it requires a deep understanding of geospatial data structures and API limitations.

POI Search and Path Planning Logic

The POI (Point of Interest) Search API requires parameters such as `keywords`, `city`, and `extensions`.[22] The `extensions=all` parameter is particularly useful as it returns detailed information like business hours and ratings, which the agent uses to determine the feasibility of a stop.[22]

When planning the route between these POIs, the system utilizes the Path Planning API, which supports walking, driving, and transit.[21] The response provides not only the geometry of the route but also the estimated duration, allowing the agent to calculate whether a 3-day itinerary is realistically achievable.[21, 36]

Geographic Coordinate Systems and Normalization

A frequent technical hurdle is the coordinate system mismatch. While most international APIs use WGS-84 (the global standard for GPS), Chinese mapping services like Amap utilize the GCJ-02 (Mars Coordinate) system.[3] If the coordinates are not handled consistently, markers on the map may appear shifted. The HelloAgents framework ensures data normalization by treating location data as a strictly typed object within the Pydantic models, converting strings like `"116.397, 39.916"` into individual `float` values for longitude and latitude.[3, 24]

Comparative Analysis of Multi-Agent Orchestration Frameworks

While the HelloAgents system provides a baseline, professional systems often iterate toward more complex frameworks like LangGraph or CrewAI. This section explores why one framework might be chosen over another for specific travel planning use cases.[5, 7]

LangGraph: Stateful Resilience

LangGraph is built for systems that require high levels of state management.[5] For a travel planner, this means that if a user decides to change their destination halfway through a 5-day plan, the system can "backtrack" to the planning node, clear only the relevant state variables, and re-generate the itinerary without losing other preferences.[5] LangGraph’s support for cyclical workflows—where an agent can output a "Self-Correction" node—is vital for ensuring that the generated travel plan is logically consistent.[5, 7]

CrewAI: Narrative Richness and Specialized Roles

CrewAI excels in the "Human-Like" quality of the output.[7] By assigning a "Local Expert" role to a sub-agent, the framework encourages the LLM to provide insider tips and local dining recommendations that a more generic planner might miss.[7, 9] CrewAI's hierarchical process allows a "Manager Agent" to review the work of "Researcher Agents," providing a layer of quality control that is beneficial for luxury or complex travel planning.[5, 7]

| Feature               | LangGraph                    | CrewAI                      | n8n / Dify               |
| --------------------- | ---------------------------- | --------------------------- | ------------------------ |
| **Cycle Support**     | Native (Looping graphs) [5]  | Limited (Sequential) [5, 7] | Prohibited (DAG only)    |
| **State Persistence** | Checkpoint-based [5]         | Task-based context          | External DB required     |
| **Logic Type**        | Low-level Python control [5] | YAML/Role-based [5]         | No-code / Node-based [1] |
| **Speed**             | Medium (Complex setup)       | Fast (High-level) [5]       | Very Fast (Drag-drop)    |

Implementation of Real-Time Streaming and SSE

The user experience of the HelloAgents system is anchored in its streaming capability. This section examines the technical implementation of SSE in a FastAPI environment.[26, 27, 28]

Chunked Transfer Encoding and Async Generators

FastAPI’s `StreamingResponse` utilizes HTTP chunked transfer encoding, allowing data to be sent without a pre-defined `Content-Length` header.[28, 30] The backend uses an async generator to yield JSON chunks as the agents progress through their tasks.[28, 31]

This is mathematically beneficial for system stability, as it avoids long-running, blocking connections that could time out in standard proxy environments like Nginx. By sending periodic "heartbeat" pings or progress updates, the system keeps the connection alive even during intensive LLM reasoning cycles.[26, 27]

Frontend Consumption of Streaming Data

On the client side, the standard `EventSource` API (or more advanced libraries like `@microsoft/fetch-event-source` for POST requests) is used to listen to the stream.[24, 27, 30] Each incoming event triggers a state update in Vue3, allowing the UI to show a growing list of "Agent Thoughts" or progressively building the itinerary on the map.[3, 24]

Challenges and Failure Modes in Agentic Travel Planning

The transition from a prototype to a production-ready travel assistant reveals several systemic challenges. These failure modes must be addressed through a combination of architecture and prompt engineering.[10]

Handling API Unreliability and Latency

External services like weather APIs or POI searches are inherently latent and occasionally unreliable.[10, 26] A multi-agent system must be resilient to "Cascading Failures," where a failure in the weather agent causes the entire itinerary to crash.[10] The implementation of circuit breakers and fallback values—such as using historical averages for weather when real-time data is unavailable—is a hallmark of professional-grade systems.[10]

The Hallucination and Over-Generalization Problem

Agents often struggle with "Spatial Hallucinations," such as placing a landmark in the wrong city or suggesting an impossible travel route.[10] This is mitigated by strictly anchoring the agent's reasoning in the tool results. The prompt must explicitly state: "Only use landmarks returned by the POI tool. If no landmarks are found, inform the user rather than creating your own".[10]

Dependency and Environment Management

In the HelloAgents repository, issues have been documented regarding missing dependencies such as `huggingface_hub` in the `requirements.txt` file.[37] This highlights the importance of robust environment management using tools like `uv` or `pip-compile` to ensure that the agentic stack is reproducible across different machines.[12, 15, 18]

The Future of Agentic Travel Assistants

As we move deeper into the "Year of Agents," systems like HelloAgents will likely integrate more "Durable Task" capabilities, allowing for long-running workflows that can span days or weeks.[4] For example, an agent could monitor flight prices over a month and only finalize the itinerary when a specific budget threshold is reached.[4]

The maturation of the Model Context Protocol will further lower the barrier to entry, allowing travel assistants to connect to thousands of local services—ranging from real-time bus transit data in Nagoya to high-speed rail bookings in China—without custom code.[12] The ultimate goal is a "Human-in-the-loop" (HITL) system where the agent acts as a highly capable executive assistant, managing the complex logistics of travel while the user provides only high-level guidance.[4, 5]

Conclusion: Synthesizing the Agentic Workflow

The "HelloAgents Multi-Agent Travel Planning System" represents a pivotal shift in how we approach software development in the age of generative AI. By leveraging the Orchestrator-Workers pattern and the standardized Model Context Protocol, the system achieves a level of flexibility and autonomy that traditional procedural programming cannot match. The seven-day sprint methodology demonstrates that with a focused approach on core agent logic, tool encapsulation, and asynchronous communication, developers can rapidly prototype sophisticated systems that interact meaningfully with the real world. As frameworks like LangGraph and CrewAI continue to refine the boundaries of state management and role-based collaboration, the future of travel planning lies in these resilient, AI-native ecosystems that prioritize the reasoning of the model over the rigidity of the code. The integration of real-time streaming, geospatial precision, and multi-agent synergy creates an experience that is more than the sum of its parts—a truly intelligent assistant for the modern explorer.

\--------------------------------------------------------------------------------

1. hello-agents/README_EN.md at main · datawhalechina/hello-agents - GitHub, [https://github.com/datawhalechina/hello-agents/blob/main/README_EN.md](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fdatawhalechina%2Fhello-agents%2Fblob%2Fmain%2FREADME_EN.md)
2. agentic-ai-development · GitHub Topics, [https://github.com/topics/agentic-ai-development?o=asc&s=stars](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Ftopics%2Fagentic-ai-development%3Fo%3Dasc%26s%3Dstars)
3. hello-agents/docs/chapter13/第十三章智能旅行助手.md at main - GitHub, [https://github.com/datawhalechina/hello-agents/blob/main/docs/chapter13/%E7%AC%AC%E5%8D%81%E4%B8%89%E7%AB%A0%20%E6%99%BA%E8%83%BD%E6%97%85%E8%A1%8C%E5%8A%A9%E6%89%8B.md](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fdatawhalechina%2Fhello-agents%2Fblob%2Fmain%2Fdocs%2Fchapter13%2F%E7%AC%AC%E5%8D%81%E4%B8%89%E7%AB%A0%20%E6%99%BA%E8%83%BD%E6%97%85%E8%A1%8C%E5%8A%A9%E6%89%8B.md)
4. Azure-Samples/durable-agents-travel-planner - GitHub, [https://github.com/Azure-Samples/durable-agents-travel-planner](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2FAzure-Samples%2Fdurable-agents-travel-planner)
5. LangGraph vs CrewAI: Let's Learn About the Differences - ZenML Blog, [https://www.zenml.io/blog/langgraph-vs-crewai](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.zenml.io%2Fblog%2Flanggraph-vs-crewai)
6. peterzat/n8n-travel-planner-agentic-workflow: Intelligent travel planning with multi-agent AI orchestration using n8n - GitHub, [https://github.com/peterzat/n8n-travel-planner-agentic-workflow](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fpeterzat%2Fn8n-travel-planner-agentic-workflow)
7. Multiagent Orchestration Showdown: Comparing CrewAI, SmolAgents, and LangGraph | by Saeed Hajebi | Medium, [https://medium.com/@saeedhajebi/multiagent-orchestration-showdown-comparing-crewai-smolagents-and-langgraph-0e169b6a293d](https://www.google.com/url?sa=E&q=https%3A%2F%2Fmedium.com%2F@saeedhajebi%2Fmultiagent-orchestration-showdown-comparing-crewai-smolagents-and-langgraph-0e169b6a293d)
8. The Leading Multi-Agent Platform, [https://www.crewai.com/](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.crewai.com%2F)
9. mlbrilliance/TripPlanner_Agentic_AI: Using Crew AI Agentic Framework, this is a trip planner code in python - GitHub, [https://github.com/mlbrilliance/TripPlanner_Agentic_AI](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fmlbrilliance%2FTripPlanner_Agentic_AI)
10. [问题/Issue] 章节13：无法调用mcp · Issue #216 · datawhalechina/hello-agents - GitHub, [https://github.com/datawhalechina/hello-agents/issues/216](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fdatawhalechina%2Fhello-agents%2Fissues%2F216)
11. Code execution with MCP: building more efficient AI agents - Anthropic, [https://www.anthropic.com/engineering/code-execution-with-mcp](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.anthropic.com%2Fengineering%2Fcode-execution-with-mcp)
12. Bridging AI and Transit: A Deep Dive into the Nagoya Bus MCP Server, [https://skywork.ai/skypage/en/ai-transit-nagoya-bus/1981560357265707008](https://www.google.com/url?sa=E&q=https%3A%2F%2Fskywork.ai%2Fskypage%2Fen%2Fai-transit-nagoya-bus%2F1981560357265707008)
13. Tools - FastMCP, [https://gofastmcp.com/servers/tools](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgofastmcp.com%2Fservers%2Ftools)
14. Model Context Protocol (MCP) - Docs by LangChain, [https://docs.langchain.com/oss/python/langchain/mcp](https://www.google.com/url?sa=E&q=https%3A%2F%2Fdocs.langchain.com%2Foss%2Fpython%2Flangchain%2Fmcp)
15. A Beginner's Guide to Use FastMCP - Apidog, [https://apidog.com/blog/fastmcp/](https://www.google.com/url?sa=E&q=https%3A%2F%2Fapidog.com%2Fblog%2Ffastmcp%2F)
16. From REST API to MCP Server - Stainless, [https://www.stainless.com/mcp/from-rest-api-to-mcp-server](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.stainless.com%2Fmcp%2Ffrom-rest-api-to-mcp-server)
17. FastAPI FastMCP, [https://gofastmcp.com/integrations/fastapi](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgofastmcp.com%2Fintegrations%2Ffastapi)
18. Building an MCP Server with FastAPI and FastMCP - Speakeasy, [https://www.speakeasy.com/mcp/framework-guides/building-fastapi-server](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.speakeasy.com%2Fmcp%2Fframework-guides%2Fbuilding-fastapi-server)
19. Build Your First MCP Server in 15 Minutes (Complete Code) - Medium, [https://medium.com/data-science-collective/build-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79](https://www.google.com/url?sa=E&q=https%3A%2F%2Fmedium.com%2Fdata-science-collective%2Fbuild-your-first-mcp-server-in-15-minutes-complete-code-d63f85c0ce79)
20. Learn How MCP Works: Build a Simple Server with FastAPI (Beginner Friendly), [https://www.youtube.com/watch?v=Ywy9x8gM410](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DYwy9x8gM410)
21. 高德地图_Web服务API - 开放平台, [https://open.alitrip.com/docs/doc.htm?treeId=143&articleId=104661&docType=1](https://www.google.com/url?sa=E&q=https%3A%2F%2Fopen.alitrip.com%2Fdocs%2Fdoc.htm%3FtreeId%3D143%26articleId%3D104661%26docType%3D1)
22. 关键字搜索 - 高德地图API, [https://amap.apifox.cn/api-14633570](https://www.google.com/url?sa=E&q=https%3A%2F%2Famap.apifox.cn%2Fapi-14633570)
23. A Quick Introduction to Model Context Protocol (MCP) in Python - Medium, [https://medium.com/@adev94/a-quick-introduction-to-model-context-protocol-mcp-in-python-bee6d36334ec](https://www.google.com/url?sa=E&q=https%3A%2F%2Fmedium.com%2F@adev94%2Fa-quick-introduction-to-model-context-protocol-mcp-in-python-bee6d36334ec)
24. How to Stream Structured JSON Output from LLMs Using FastAPI and PydanticAI, [https://python.plainenglish.io/how-to-stream-structured-json-output-from-llms-using-fastapi-and-pydanticai-c1dacae66ca6](https://www.google.com/url?sa=E&q=https%3A%2F%2Fpython.plainenglish.io%2Fhow-to-stream-structured-json-output-from-llms-using-fastapi-and-pydanticai-c1dacae66ca6)
25. adding multiple markers to a map using json - vuejs - Reddit, [https://www.reddit.com/r/vuejs/comments/vm13wb/adding_multiple_markers_to_a_map_using_json/](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.reddit.com%2Fr%2Fvuejs%2Fcomments%2Fvm13wb%2Fadding_multiple_markers_to_a_map_using_json%2F)
26. Streaming AI Agents Responses with Server-Sent Events (SSE): A Technical Case Study, [https://akanuragkumar.medium.com/streaming-ai-agents-responses-with-server-sent-events-sse-a-technical-case-study-f3ac855d0755](https://www.google.com/url?sa=E&q=https%3A%2F%2Fakanuragkumar.medium.com%2Fstreaming-ai-agents-responses-with-server-sent-events-sse-a-technical-case-study-f3ac855d0755)
27. How to Stream LLM Responses in Real-Time Using FastAPI and SSE - GoPenAI, [https://blog.gopenai.com/how-to-stream-llm-responses-in-real-time-using-fastapi-and-sse-d2a5a30f2928](https://www.google.com/url?sa=E&q=https%3A%2F%2Fblog.gopenai.com%2Fhow-to-stream-llm-responses-in-real-time-using-fastapi-and-sse-d2a5a30f2928)
28. Streaming APIs for Beginners: Python, FastAPI, and Async Generators | by Okan Yenigün, [https://python.plainenglish.io/streaming-apis-for-beginners-python-fastapi-and-async-generators-848b73a8fc06](https://www.google.com/url?sa=E&q=https%3A%2F%2Fpython.plainenglish.io%2Fstreaming-apis-for-beginners-python-fastapi-and-async-generators-848b73a8fc06)
29. How to forward OpenAI's stream response using FastAPI in python? - API, [https://community.openai.com/t/how-to-forward-openais-stream-response-using-fastapi-in-python/963242](https://www.google.com/url?sa=E&q=https%3A%2F%2Fcommunity.openai.com%2Ft%2Fhow-to-forward-openais-stream-response-using-fastapi-in-python%2F963242)
30. Streaming Responses In FastAPI - Medium, [https://medium.com/@ab.hassanein/streaming-responses-in-fastapi-d6a3397a4b7b](https://www.google.com/url?sa=E&q=https%3A%2F%2Fmedium.com%2F@ab.hassanein%2Fstreaming-responses-in-fastapi-d6a3397a4b7b)
31. Custom Response - HTML, Stream, File, others - FastAPI, [https://fastapi.tiangolo.com/advanced/custom-response/](https://www.google.com/url?sa=E&q=https%3A%2F%2Ffastapi.tiangolo.com%2Fadvanced%2Fcustom-response%2F)
32. Guide to Implementing Marker Clustering and Automatic Zoom Levels in Vue-Amap With Amap - Oreate AI Blog, [https://www.oreateai.com/blog/guide-to-implementing-marker-clustering-and-automatic-zoom-levels-in-vueamap-with-amap/5b68e7354be4af7b59e66851113b6d9d](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.oreateai.com%2Fblog%2Fguide-to-implementing-marker-clustering-and-automatic-zoom-levels-in-vueamap-with-amap%2F5b68e7354be4af7b59e66851113b6d9d)
33. vue3-google-map/README.md at develop - GitHub, [https://github.com/inocan-group/vue3-google-map/blob/develop/README.md](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Finocan-group%2Fvue3-google-map%2Fblob%2Fdevelop%2FREADME.md)
34. Simple Polylines | Maps JavaScript API - Google for Developers, [https://developers.google.com/maps/documentation/javascript/examples/polyline-simple](https://www.google.com/url?sa=E&q=https%3A%2F%2Fdevelopers.google.com%2Fmaps%2Fdocumentation%2Fjavascript%2Fexamples%2Fpolyline-simple)
35. Migrate to advanced markers | Maps JavaScript API - Google for Developers, [https://developers.google.com/maps/documentation/javascript/advanced-markers/migration](https://www.google.com/url?sa=E&q=https%3A%2F%2Fdevelopers.google.com%2Fmaps%2Fdocumentation%2Fjavascript%2Fadvanced-markers%2Fmigration)
36. Display routing information on a map image - HERE Technologies, [https://www.here.com/docs/bundle/map-image-developer-guide-v3/page/topics/routing-tutorial.html](https://www.google.com/url?sa=E&q=https%3A%2F%2Fwww.here.com%2Fdocs%2Fbundle%2Fmap-image-developer-guide-v3%2Fpage%2Ftopics%2Frouting-tutorial.html)
37. [问题/Issue] 章节13：code/chapter13/helloagents-trip-planner/backend/requirements.txt文件中缺少huggingface_hub模块依赖#223 - GitHub, [https://github.com/datawhalechina/hello-agents/issues/223](https://www.google.com/url?sa=E&q=https%3A%2F%2Fgithub.com%2Fdatawhalechina%2Fhello-agents%2Fissues%2F223)