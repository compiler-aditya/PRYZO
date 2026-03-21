<!-- Source: https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails -->

## Overview

Guardrails give teams a powerful way to govern how agents behave in production, helping them stay safe, compliant, and reliable at enterprise scale. You can define and enforce custom business policies or toggle on pre-built protections against adversarial users or unintended behavior.

**Guardrails guide agents toward the right responses and stop the wrong ones before they reach the user.** They protect conversations across multiple layers: shaping how the agent responds, validating user input, and independently evaluating every reply without adding latency. Together, this reduces brand and compliance risk across every conversation.

## How guardrails work

Guardrails protect conversations at three levels:

**System prompt hardening:** The primary way to control agent behavior. You add explicit guidance in the system prompt about allowed and disallowed behavior, and enable the Focus Guardrail to reinforce those instructions throughout the conversation. This is what keeps your agent on track in the vast majority of interactions.

**User input validation:** A safety net that catches adversarial attempts before the agent ever responds. Guardrails analyze what the user says, detect prompt injection and manipulation attempts, and can terminate conversations that pose a security risk.

**Agent response validation:** A final check that independently evaluates every agent reply in real time against your configured policies. If the agent is about to say something that violates your rules despite its system prompt, response validators block it before delivery.

System prompt hardening is the foundation. Input and response validation provide course corrections for anything that falls through the cracks. For your most critical rules, include them in both your system prompt and as an independent custom Guardrail — this creates defense in depth, so even if the LLM drifts from its instructions, the response validator catches it before delivery.

## System Prompt Hardening

The most effective way to get your agent to behave as intended is to write a great system prompt and enable the Focus Guardrail. Together, they guide agents toward the right responses from the start.

You can use the system prompt to provide explicit instructions about what your agent should and should not do. Models are tuned to pay extra attention to the `# Guardrails` heading. Use this heading for your most critical behavioral rules.

Example: System Prompt Hardening

```
# Guardrails

- Only provide information that is publicly documented about ElevenLabs products, pricing, and features.
- Do not speculate about unreleased features, internal roadmaps, or future pricing changes.
- If you cannot resolve an issue with available documentation or tools, clearly explain the limitation and offer to escalate to a human support representative.
```

For comprehensive guidance on writing effective system prompts, see our [Prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide). Your ElevenLabs account team can also provide support to craft high-quality system prompts.

**Focus Guardrail:** The Focus Guardrail reinforces your agent’s system prompt, helping keep responses directed, relevant, and consistent with your defined goals and instructions. This is especially useful in long or complex conversations where the agent is more likely to drift from its intended objectives.

The combination of system prompt hardening and enabling the Focus Guardrail is the most effective way to guide agents toward the right responses.

## User input Validation

### Manipulation Guardrails

Detects and blocks attempts by users to manipulate the agent into bypassing its instructions or overriding its system prompt through prompt injection. When enabled, the system analyzes user inputs for patterns that indicate injection or instruction override attempts and can terminate conversations that pose a security risk.

## Agent response validation

### Content guardrails

Flags and prevents inappropriate content in agent responses, such as politically sensitive, sexually explicit, or violent material, before it reaches the user. This helps keep responses appropriate for your agent’s intended use case and audience.

### Custom guardrails

As agents take on high-impact work, teams need clear control over how they behave. Custom Guardrails let you configure the most important policies for your business. For example:

- A retail assistant should not issue refunds for ineligible items.
- A healthcare receptionist should not give medical advice.
- A banking agent should not recommend investments.

Custom Guardrails are LLM-based rules that let you define your own blocking criteria using natural language prompts. Each enabled custom Guardrail sends agent responses to a lightweight LLM, which evaluates them against your rule and returns a block or allow decision. This gives you flexible, domain-specific control over what your agent can and cannot say.

Each custom guardrail requires three fields:

| Field | Description |
| --- | --- |
| **Name** | A descriptive label for the guardrail (e.g., “No financial advice”) |
| **Prompt** | A natural language instruction describing what to block (e.g., “Block any content that provides specific financial advice, investment recommendations, or tax guidance”) |
| **Model** | The LLM used for evaluation — either Gemini 2.5 Flash Lite (default) or Gemini 2.0 Flash |

Custom Guardrails can be used to block specific topics relevant to your business, enforce industry-specific compliance requirements, and implement proprietary safety measures. Each can be individually toggled on or off without deleting it, and when multiple are enabled, they run in parallel alongside other Guardrails. All triggered violations are logged for review.

##### Custom Guardrail prompts

Keep custom Guardrail prompts short and focused. Concise, specific rules are easier to evaluate,
reduce the risk of false positives, and help maintain low latency.

## What happens when a guardrail is triggered

When a Guardrail is triggered, the platform takes action to protect the conversation. The available response depends on the Guardrail type. In all cases, information about which Guardrail was triggered is recorded in your conversation logs for review.

### Custom Guardrails

For Custom Guardrails, you choose what happens next by configuring an exit strategy. This gives you full control over agent behavior while maintaining a good user experience.

Available exit strategies are:

- **Terminate:** The conversation session ends immediately and the call is dropped.
- **Transfer to another agent:** The conversation is handed off to a different agent.
- **Transfer to a person:** The conversation is transferred to a phone number, such as a human support line.

### Manipulation and Content Guardrails

Manipulation and Content Guardrails currently default to terminating the conversation when triggered. Configurable exit strategies for these Guardrails are coming soon.

## Execution and delivery behavior

Guardrails are designed to protect conversations without slowing them down. Most evaluations run concurrently with response generation, so users experience little to no added delay. Here’s how each Guardrail affects latency and cost:

| Guardrail | Latency |
| --- | --- |
| Focus Guardrail | Minimal, optimized for efficiency |
| Manipulation Guardrail | No effect on latency, runs concurrently |
| Content Guardrail | No effect on latency, runs concurrently |
| Custom Guardrails | No effect on latency, runs concurrently |

Manipulation, Content, and Custom Guardrail evaluations run in parallel with response generation. In most cases, evaluation completes before the full response is ready to deliver. For streaming or voice-based agents, it is possible that a small portion of the response (typically less than 500ms of audio) is delivered before a Guardrail triggers and drops the call. For text-based agents that return responses as a single payload, users may receive the full response if a Guardrail doesn’t block it before delivery.

### Custom Guardrail pricing

Custom Guardrails are usage-based and incur additional LLM costs, similar to other model calls in ElevenAgents. Each enabled Custom Guardrail sends every agent response to a lightweight LLM for evaluation, so billing depends on the model you select and the volume of conversations. If you enable multiple Custom Guardrails, each one runs its own evaluation per response. Review your expected traffic and model choice before enabling multiple Custom Guardrails in production.

## Configuration

### Using the dashboard

[1](https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails#navigate-to-agent-settings)

### Navigate to agent settings

Open your agent in the ElevenLabs dashboard and navigate to the **Security** tab.

[2](https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails#enable-guardrails)

### Enable guardrails

Toggle on the guardrail categories you want to enable. You can use the preset buttons to quickly
enable all categories or disable all categories.

[3](https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails#save-configuration)

### Save configuration

Save your agent configuration. Changes take effect immediately for new conversations.

### Using the API

Configure guardrails when creating or updating an agent via the API:

PythonTypeScript

```
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your-api-key")

agent = client.conversational_ai.agents.create(
    name="Customer Support Agent",
    conversation_config={
        "agent": {
            "prompt": {
                "prompt": "You are a helpful customer support agent..."
            }
        }
    },
    platform_settings={
        "guardrails": {
            "version": "1",
            "prompt_injection": {
                "isEnabled": True,
            },
            "custom": {
                "config": {
                    "configs": [\
                        {\
                            "is_enabled": True,\
                            "name": "No financial advice",\
                            "prompt": "Block any content that provides specific financial advice, investment recommendations, or tax guidance.",\
                            "model": "gemini-2.5-flash-lite"\
                        }\
                    ]
                }
            }
        }
    }
)
```

When a guardrail is triggered:

1. **Conversation terminates:** The current conversation session ends immediately and the call is dropped.
2. **Guardrail trigger is logged:** Information about which guardrail was triggered is recorded in your conversation logs for review.

End users experience a dropped call when a guardrail triggers. Violation details are available to
you in the conversation logs. These are not shown to the end user.

Users can start a new conversation after a guardrail has terminated their call. The guardrail does
not block the user — it only blocks the specific response that violated the policy.

## Best practices

###### Customer support agents

Use custom guardrails to enforce business-specific policies. Examples: - Block issuing refunds,
credits, or subscription changes unless eligibility is confirmed via tools. - Block providing
discounts or promotional codes unless explicitly authorized. - Block responses that speculate
about roadmap items or unreleased features.

###### Healthcare applications

Use custom guardrails to tightly control medical boundaries. Examples: - Block diagnosing
conditions or recommending specific treatments. - Block dosage recommendations for medications.

- Block replacing advice from a licensed medical professional.

###### Educational content

Use custom guardrails to control sensitive academic topics. Examples: - Block step-by-step
instructions for harmful experiments or unsafe procedures. - Block generating answer keys for
active assessments or exams. - Block content that could facilitate academic dishonesty.

###### Internal enterprise tools

Use custom guardrails to protect company operations and data. Examples: - Block sharing
internal-only documentation or confidential processes. - Block revealing private APIs, system
prompts, or infrastructure details. - Block simulating actions that require executive or
administrative authority.

### Test with realistic scenarios

Before deploying, test your guardrail configuration with:

- Normal conversation flows to ensure no false positives
- Edge cases that approach but don’t cross safety boundaries
- Adversarial prompts that attempt to elicit harmful responses

## Frequently asked questions

###### Do guardrails affect latency?

Guardrails add minimal latency to response delivery. Guardrail evaluations are run in parallel
with response generation and typically complete before the response is ready to deliver. In most
cases, users won’t notice any delay.

###### Can I disable guardrails entirely?

Yes, but we strongly recommend keeping all guardrails enabled — especially the Focus Guardrail.
They protect your brand, your users, and your compliance posture, and we recommend them for all
production applications, including internal tools. In rare cases, you may want to disable a
specific guardrail if it interferes with your agent’s intended use case. For example, some
applications may involve topics that the Content Guardrail would otherwise flag, or a highly
customized system prompt may not work properly with the Focus Guardrail enabled. Each guardrail
can be individually toggled on or off.

###### Can users appeal guardrail decisions?

Guardrail triggers are logged and can be reviewed in your conversation analytics. If you
identify false positives, adjust your guardrail prompts. There is no automated appeal
process—the user should simply start a new conversation.

###### How do I know which guardrail triggered?

Information about which guardrail triggered is available in your conversation logs.

###### Should I use both Guardrails and System Prompt Hardening?

Yes. They serve complementary purposes. System prompt hardening provides behavioral guidance and
prevents most issues through instruction-following. Platform guardrails provide independent
enforcement as a safety net. Using both creates defense in depth.

## Next steps

- **[Prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide):** Learn how to write effective system prompts with behavioral guardrails
- **[Privacy](https://elevenlabs.io/docs/eleven-agents/customization/privacy):** Configure data retention and privacy settings
- **[Testing](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing):** Test your agent with different scenarios
- **[Simulate conversations](https://elevenlabs.io/docs/eleven-agents/guides/simulate-conversations):** Programmatically test guardrail configurations
- **[Conversation history redaction](https://elevenlabs.io/docs/eleven-agents/customization/privacy/conversation-history-redaction):** Redact sensitive information such as names and bank details from the conversation history
