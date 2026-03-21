<!-- Source: https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration -->

Connect Your Voice Agent to Twilio – Telephony Setup & Inbound Calls - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Connect Your Voice Agent to Twilio – Telephony Setup & Inbound Calls](https://www.youtube.com/watch?v=1_ebl-acp6M)

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

[Watch on](https://www.youtube.com/watch?v=1_ebl-acp6M&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 4:54

•Live

•

## Overview

This guide shows you how to connect a Twilio phone number to your ElevenLabs agent to handle both inbound and outbound calls.

You will learn to:

- Import an existing Twilio phone number.
- Link it to your agent to handle inbound calls.
- Initiate outbound calls using your agent.

## Phone Number Types & Capabilities

ElevenLabs supports two types of Twilio phone numbers with different capabilities:

### Purchased Twilio Numbers (Full Support)

- **Inbound calls**: Supported - Can receive calls and route them to agents
- **Outbound calls**: Supported - Can make calls using agents
- **Requirements**: Number must be purchased through Twilio and appear in your “Phone Numbers” section

### Verified Caller IDs (Outbound Only)

- **Inbound calls**: Not supported - Cannot receive calls or be assigned to agents
- **Outbound calls**: Supported - Can make calls using agents
- **Requirements**: Number must be verified in Twilio’s “Verified Caller IDs” section
- **Use case**: Ideal for using your existing business number for outbound AI calls

Learn more about [verifying caller IDs at scale](https://www.twilio.com/docs/voice/api/verifying-caller-ids-scale) in Twilio’s documentation.

During phone number import, ElevenLabs automatically detects the capabilities of your number based
on its configuration in Twilio.

## Guide

### Prerequisites

- A [Twilio account](https://twilio.com/).
- Either:
  - A purchased & provisioned Twilio [phone number](https://www.twilio.com/docs/phone-numbers) (for inbound + outbound)
  - OR a [verified caller ID](https://www.twilio.com/docs/voice/make-calls#verify-your-caller-id) in Twilio (for outbound only)

[1](https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration#import-a-twilio-phone-number)

### Import a Twilio phone number

In the ElevenAgents dashboard, go to the [**Phone Numbers**](https://elevenlabs.io/app/agents/phone-numbers) tab.

![ElevenAgents phone numbers page](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/7efb681147acd8f04803f84ed7f3289f0e90eb1fb0173e2a825836408cee89d1/assets/images/conversational-ai/phone-numbers-page.png)

Next, fill in the following details:

- **Label:** A descriptive name (e.g., `Customer Support Line`).
- **Phone Number:** The Twilio number you want to use.
- **Twilio SID:** Your Twilio Account SID.
- **Twilio Token:** Your Twilio Auth Token.

You can find your account SID and auth token [**in the Twilio admin console**](https://www.twilio.com/console).

###### ElevenAgents dashboard

###### Twilio admin console

![Phone number configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/9501110d58bfeca27cb9983bc44035864504bdc2ed9c78d9decbd04802f64418/assets/images/conversational-ai/phone-numbers-new.png)

ElevenLabs automatically configures the Twilio phone number with the correct settings.

###### Applied settings

![Twilio phone number configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/b11d57a0aa588964bbd0117d2135c55592569a4bf051f00f17aa3ee632833a47/assets/images/conversational-ai/twilio-configuration.png)

**Phone Number Detection**: ElevenLabs will automatically detect whether your number supports:

- **Inbound + Outbound**: Numbers purchased through Twilio
- **Outbound Only**: Numbers verified as caller IDs in Twilio

If your number is not found in either category, you’ll receive an error asking you to verify it exists in your Twilio account.

[2](https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration#assign-your-agent-inbound-capable-numbers-only)

### Assign your agent (Inbound-capable numbers only)

If your phone number supports inbound calls, you can assign an agent to handle incoming calls.

![Select agent for inbound calls](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/b85c122ef8607527041516e789b0a19047cbf85a13cd3237ee5a7670683815a7/assets/images/conversational-ai/twilio-assigned-agent.png)

Numbers that only support outbound calls (verified caller IDs) cannot be assigned to agents and
will show as disabled in the agent dropdown.

Test the agent by giving the phone number a call. Your agent is now ready to handle inbound calls and engage with your customers.

Monitor your first few calls in the [Calls History\\
dashboard](https://elevenlabs.io/app/agents/history) to ensure everything is working as expected.

## Making Outbound Calls

Both purchased Twilio numbers and verified caller IDs can be used for outbound calls. The outbound
call button will be disabled for numbers that don’t support outbound calling.

Your imported Twilio phone number can also be used to initiate outbound calls where your agent calls a specified phone number.

[1](https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration#initiate-an-outbound-call)

### Initiate an outbound call

From the [**Phone Numbers**](https://elevenlabs.io/app/agents/phone-numbers) tab, locate your imported Twilio number and click the **Outbound call** button.

![Outbound call button](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/953a870b0ab0c0aa30872b3692260f0879f390d4b4b83c7f82e816385504034f/assets/images/conversational-ai/outbound-button.png)

[2](https://elevenlabs.io/docs/eleven-agents/phone-numbers/twilio-integration/native-integration#configure-the-call)

### Configure the call

In the Outbound Call modal:

1. Select the agent that will handle the conversation
2. Enter the phone number you want to call
3. Click **Send Test Call** to initiate the call

![Outbound call configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/f6b01412a68217661028e6924ce90089bdd5eaa693c8aeafbc321c632de921b7/assets/images/conversational-ai/outbound-modal.png)

Once initiated, the recipient will receive a call from your Twilio number. When they answer, your agent will begin the conversation.

Outbound calls appear in your [Calls History dashboard](https://elevenlabs.io/app/agents/history)
alongside inbound calls, allowing you to review all conversations.

When making outbound calls, your agent will be the initiator of the conversation, so ensure your
agent has appropriate initial messages configured to start the conversation effectively.
