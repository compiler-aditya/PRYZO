<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/agent-workflows -->

Agent Workflows walkthrough - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Agent Workflows walkthrough](https://www.youtube.com/watch?v=7gtzXAaA82I)

ElevenLabs

Search

Watch later

Share

Copy link

Info

Shopping

Tap to unmute

If playback doesn't begin shortly, try restarting your device.

Full screen is unavailable. [Learn More](https://support.google.com/youtube/answer/6276924)

More videos

## More videos

You're signed out

Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.

CancelConfirm

Share

Include playlist

An error occurred while retrieving sharing information. Please try again later.

[Watch on](https://www.youtube.com/watch?v=7gtzXAaA82I&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 3:24

•Live

•

## Overview

Agent Workflows provide a powerful visual interface for designing complex conversation flows in ElevenAgents. Instead of relying on linear conversation paths, workflows enable you to create sophisticated, branching conversation graphs that adapt dynamically to user needs.

![Workflow Overview](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/0b5b2cf9754c67ef469c08af5d13786f70ca8e0018d10e92595861abb4ed32cb/assets/images/conversational-ai/workflow-overview.png)

## Node types

Workflows are composed of different node types, each serving a specific purpose in your conversation flow.

![Node Types](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/d638a84e1a6dc584a812be436f5da5e665b103b6cb5b6c53840705723bbb5a8f/assets/images/conversational-ai/workflow-node-types.png)

### Subagent nodes

Subagent nodes allow you to modify agent behavior at specific points in your workflow. These modifications are applied on top of the base agent configuration, or can override the current agent’s config completely, giving you fine-grained control over each conversation phase.
Any of an agent’s configuration, tools available, and attached knowledge base items can be updated/overwitten.

###### General

###### Knowledge Base

###### Tools

![Subagent Extra Agent Config](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/8ca72df8768a03adc0064281c906ab0f5710153249d17f7e7d51f465da7e9e94/assets/images/conversational-ai/workflow-subagent-extra-agent-config.png)

Modify core agent settings for this specific node:

- **System Prompt**: Append or override system instructions to guide agent behavior
- **LLM Selection**: Choose a different language model (e.g., switch from Gemini 2.0 Flash to a more powerful model for complex reasoning tasks)
- **Voice Configuration**: Change voice settings including speed, tone, or even switch to a different voice

**Use Cases:**

- Use a more powerful LLM for complex decision-making nodes
- Apply stricter conversation guidelines during sensitive information gathering
- Change voice characteristics for different conversation phases
- Modify agent personality for specific interaction types

### Dispatch tool node

Tool nodes execute a specific tool call during conversation flow. Unlike tools within subagents, tool nodes are dedicated execution points that guarantee the tool is called.

![Tool Node Result Edges](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/6b60603e56dfb25e89cdfe4223826f635af874e034af8936d74d3b428611e17b/assets/images/conversational-ai/workflow-tool-node-result-edges.png)

**Special Edge Configuration:**
Tool nodes have a unique edge type that allows routing to a new node based on the tool execution result. You can define:

- **Success path**: Where to route when the tool executes successfully
- **Failure path**: Where to route when the tool fails or returns an error

In future, futher branching conditions will be provided.

### Agent transfer node

Agent transfer node facilitate handoffs the conversation between different conversational agents, learn more [here](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/agent-transfer).

### Transfer to number node

Transfer to number nodes transitions from a conversation with an AI agent to a human agent via phone systems, learn more [here](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/transfer-to-number)

### End node

End call nodes terminate the conversation flow gracefully, learn more [here](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/transfer-to-human#:~:text=System%20tools-,End%20call,-Language%20detection)

## Edges and flow control

Edges define how conversations flow between nodes in your workflow. They support sophisticated routing logic that enables dynamic, context-aware conversation paths.

![Workflow Edges](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/02d664c9211bb8cf5452b80ab865f26b8d0b723a6acff75141ea1e9c43f7dbab/assets/images/conversational-ai/workflow-edges.png)

###### Forward Edges

###### Backward Edges

Forward edges move the conversation to subsequent nodes in the workflow. They represent the primary flow of your conversation.

![Forward Edge Configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/2400c66bf6f60b0d4262ecd828dea93847197f7cc00d9c8964e6486419bc90be/assets/images/conversational-ai/workflow-edge-forward.png)

###### LLM Condition

###### Expression

###### None

Use LLM conditions to create dynamic conversation flows based on natural language evaluation. The LLM evaluates conditions in real-time to determine the appropriate path.

![LLM Condition Agent Transfer](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/507885879d781f291ab35b7dda84e760767a5544ffb6bf7b455e7a1cc19b78b7/assets/images/conversational-ai/workflow-agent-transfer-llm-condition.png)

**Configuration Options:**

- **Label**: Human-readable description of the edge condition (not processed by LLM)
- **LLM Condition**: Natural language condition evaluated by the LLM
