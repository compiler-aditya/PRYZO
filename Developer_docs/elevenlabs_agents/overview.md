<!-- Source: https://elevenlabs.io/docs/eleven-agents/overview -->

Agents accomplish tasks through natural dialogue - from quick requests to complex, open-ended workflows. ElevenLabs provides voice-rich, expressive models, developer tools for building multimodal agents, and tools to monitor and evaluate agent performance at scale.

[![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/b01da89ad7994300673d0932d321cd0f53fe727b6210e6c1f00e765e498f8722/assets/images/agents/agents-overview-build.png)\\
\\
**Configure** \\
\\
Configure multimodal agents with our developer toolkit, dashboard, or visual workflow\\
builder](https://elevenlabs.io/docs/agents-platform/build/overview) [![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/17a81505a62493491ead763b307b1e854825a0da67ab1a1d86b41b57ad87bc73/assets/images/agents/agents-overview-integrate.png)\\
\\
**Deploy** \\
\\
Integrate multimodal agents across telephony systems, web, and mobile](https://elevenlabs.io/docs/agents-platform/integrate/overview) [![](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/3790a000d203429c852cd4be74f2635ea41222f31b0edb53ae760c61e4a0f07d/assets/images/agents/agents-overview-operate.png)\\
\\
**Monitor** \\
\\
Evaluate agent performance with built-in testing, evals, and analytics](https://elevenlabs.io/docs/agents-platform/operate/overview)

## Platform capabilities

From design to deployment to optimization, ElevenLabs provides everything you need to build agents at scale.

### Design and configure

| Goal | Guide | Description |
| --- | --- | --- |
| Create conversation workflows | [Workflows](https://elevenlabs.io/docs/agents-platform/customization/agent-workflows) | Build multi-step workflows with visual workflow builder |
| Write system prompts | [System prompt](https://elevenlabs.io/docs/agents-platform/best-practices/prompting-guide) | Learn best practices for crafting effective agent prompts |
| Select language model | [Models](https://elevenlabs.io/docs/agents-platform/customization/llm) | Choose from supported LLMs or bring your own custom model |
| Control conversation flow | [Conversation flow](https://elevenlabs.io/docs/agents-platform/customization/conversation-flow) | Configure turn-taking, interruptions, and timeout settings |
| Configure voice & language | [Voice & language](https://elevenlabs.io/docs/agents-platform/customization/voice) | Select from 5k+ voices across 31 languages with customization options |
| Add knowledge to agent | [Knowledge base](https://elevenlabs.io/docs/agents-platform/customization/knowledge-base) | Upload documents and enable RAG for grounded responses |
| Connect tools | [Tools](https://elevenlabs.io/docs/agents-platform/customization/tools) | Enable agents to call clients & APIs to perform actions |
| Personalize each conversation | [Personalization](https://elevenlabs.io/docs/agents-platform/customization/personalization) | Use dynamic variables and overrides for per-conversation customization |
| Secure agent access | [Authentication](https://elevenlabs.io/docs/agents-platform/customization/authentication) | Implement custom authentication for protected agent access |

### Connect and deploy

| Goal | Guide | Description |
| --- | --- | --- |
| Build with React components | [ElevenLabs UI](https://ui.elevenlabs.io/) | Pre-built components library for audio & agent apps (shadcn-based) |
| Embed widget in website | [Widget](https://elevenlabs.io/docs/agents-platform/customization/widget) | Add a customizable web widget to any website |
| Build React web apps | [React SDK](https://elevenlabs.io/docs/agents-platform/libraries/react) | Voice-enabled React hooks and components |
| Build iOS apps | [Swift SDK](https://elevenlabs.io/docs/agents-platform/libraries/swift) | Native iOS SDK for voice agents |
| Build Android apps | [Kotlin SDK](https://elevenlabs.io/docs/agents-platform/libraries/kotlin) | Native Android SDK for voice agents |
| Build React Native apps | [React Native SDK](https://elevenlabs.io/docs/agents-platform/libraries/react-native) | Cross-platform iOS and Android with React Native |
| Connect via SIP trunk | [SIP trunk](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking) | Integrate with existing telephony infrastructure |
| Make batch outbound calls | [Batch calls](https://elevenlabs.io/docs/agents-platform/phone-numbers/batch-calls) | Trigger multiple calls programmatically |
| Use Twilio integration | [Twilio](https://elevenlabs.io/docs/agents-platform/phone-numbers/twilio-integration/native-integration) | Native Twilio integration for phone calls |
| Build custom integrations | [WebSocket API](https://elevenlabs.io/docs/agents-platform/libraries/web-sockets) | Low-level WebSocket protocol for custom implementations |
| Receive real-time events | [Events](https://elevenlabs.io/docs/agents-platform/customization/events) | Subscribe to conversation events and updates |

### Monitor and optimize

| Goal | Guide | Description |
| --- | --- | --- |
| Run A/B tests | [Experiments](https://elevenlabs.io/docs/agents-platform/operate/experiments) | Test agent configuration changes with live traffic |
| Test agent behavior | [Testing](https://elevenlabs.io/docs/agents-platform/customization/agent-testing) | Create and run automated tests for your agents |
| Analyze conversation quality | [Conversation analysis](https://elevenlabs.io/docs/agents-platform/customization/agent-analysis) | Extract insights and evaluate conversation outcomes |
| Track metrics & analytics | [Analytics](https://elevenlabs.io/docs/agents-platform/dashboard) | Monitor performance metrics and conversation history |
| Configure data retention | [Privacy](https://elevenlabs.io/docs/agents-platform/customization/privacy) | Set retention policies for conversations and audio |
| Reduce LLM costs | [Cost optimization](https://elevenlabs.io/docs/agents-platform/customization/llm/optimizing-costs) | Monitor and optimize language model expenses |

## Architecture

ElevenAgents coordinates 4 core components:

1. A fine-tuned Speech to Text (ASR) model for speech recognition
2. Your choice of language model or [custom](https://elevenlabs.io/docs/agents-platform/customization/llm/custom-llm) LLM
3. A low-latency Text to Speech (TTS) model across 5k+ voices and 70+ languages
4. A proprietary turn-taking model that handles conversation timing

[Quickstart\\
\\
Build your first agent in 5 minutes](https://elevenlabs.io/docs/agents-platform/quickstart)
