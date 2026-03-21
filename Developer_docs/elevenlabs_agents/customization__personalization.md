<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/personalization -->

## Overview

Personalization allows you to adapt your agent’s behavior for each individual user, enabling more natural and contextually relevant conversations. ElevenLabs offers multiple approaches to personalization:

1. **Dynamic Variables** \- Inject runtime values into prompts and messages
2. **Overrides** \- Completely replace system prompts or messages
3. **Twilio Integration** \- Personalize inbound call experiences via webhooks

## Personalization Methods

[Dynamic Variables\\
\\
Define runtime values using `{{ var_name }}` syntax to personalize your agent’s messages, system\\
prompts, and tools.](https://elevenlabs.io/docs/agents-platform/customization/personalization/dynamic-variables) [Overrides\\
\\
Completely replace system prompts, first messages, language, or voice settings for each\\
conversation.](https://elevenlabs.io/docs/agents-platform/customization/personalization/overrides) [Twilio Integration\\
\\
Dynamically personalize inbound Twilio calls using webhook data.](https://elevenlabs.io/docs/agents-platform/customization/personalization/twilio-personalization)

## Conversation Initiation Client Data Structure

The `conversation_initiation_client_data` object defines what can be customized when starting a conversation:

```
{
  "type": "conversation_initiation_client_data",
  "conversation_config_override": {
    "agent": {
      "prompt": {
        "prompt": "overriding system prompt"
      },
      "first_message": "overriding first message",
      "language": "en"
    },
    "tts": {
      "voice_id": "voice-id-here"
    }
  },
  "custom_llm_extra_body": {
    "temperature": 0.7,
    "max_tokens": 100
  },
  "dynamic_variables": {
    "string_var": "text value",
    "number_var": 1.2,
    "integer_var": 123,
    "boolean_var": true
  },
  "user_id": "your_custom_user_id"
}
```

System dynamic variables (those prefixed with `system__`) cannot be sent or overridden in the
client initiation payload. Only custom dynamic variables can be set via the `dynamic_variables`
field.

## Choosing the Right Approach

| Method | Best For | Implementation |
| --- | --- | --- |
| **Dynamic Variables** | - Inserting user-specific data into templated content - Maintaining consistent agent<br>  behavior with personalized details - Personalizing tool parameters | Define variables with `{{ variable_name }}` and pass values at runtime |
| **Overrides** | - Completely changing agent behavior per user - Switching languages or voices - Legacy<br>  applications (consider migrating to Dynamic Variables) | Enable specific override permissions in security settings and pass complete replacement<br>content |

## Learn More

- [Dynamic Variables Documentation](https://elevenlabs.io/docs/agents-platform/customization/personalization/dynamic-variables)
- [Overrides Documentation](https://elevenlabs.io/docs/agents-platform/customization/personalization/overrides)
- [Twilio Integration Documentation](https://elevenlabs.io/docs/agents-platform/customization/personalization/twilio-personalization)
