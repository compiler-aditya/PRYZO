<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/widget -->

Embed Your ElevenLabs Voice Agent Anywhere – Widget Setup & Customization - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Embed Your ElevenLabs Voice Agent Anywhere – Widget Setup & Customization](https://www.youtube.com/watch?v=XweA70b45Ws)

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

[Watch on](https://www.youtube.com/watch?v=XweA70b45Ws&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 4:09

•Live

•

**Widgets** enable instant integration of ElevenAgents into any website. You can either customize your widget through the UI or through our type-safe [ElevenAgents SDKs](https://elevenlabs.io/docs/developers/resources/libraries) for complete control over styling and behavior. The SDK overrides take priority over UI customization.
Our widget is multimodal and able to process both text and audio.

Introducing Multimodal Conversational AI - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Introducing Multimodal Conversational AI](https://www.youtube.com/watch?v=TyPbeheubcs)

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

[Watch on](https://www.youtube.com/watch?v=TyPbeheubcs&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 3:02

•Live

•

Multimodal conversational agents

## Modality configuration

The widget supports flexible input modes to match your use case. Configure these options in the [dashboard](https://elevenlabs.io/app/agents/dashboard) **Widget** tab under the **Interface** section.

Multimodality is fully supported in our client SDKs, see more
[here](https://elevenlabs.io/docs/developers/resources/libraries).

![Widget interface options](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/cf851dd7a29b4bd23f7d36097ebf57c0bfe1b6a7a3b35687ddea20d9920a93c0/assets/images/conversational-ai/widget-options.png)

**Available modes:**

- **Voice only** (default): Users interact through speech only.
- **Voice + text**: Users can switch between voice and text input during conversations.
- **Chat Mode**: Conversations start in chat (text-only) mode without voice capabilities when initiated with a text message.

For more information on using chat (text-only) mode via our SDKs, see our [chat mode guide](https://elevenlabs.io/docs/agents-platform/guides/chat-mode).

The widget defaults to voice-only mode. Enable the text input toggle to allow multimodal
interactions, or enable text-only mode support for purely text-based conversations when initiated
via text.

## Embedding the widget

Widgets currently require public agents with authentication disabled. Ensure this is disabled in
the **Advanced** tab of your agent settings.

Add this code snippet to your website’s `<body>` section. Place it in your main `index.html` file for site-wide availability:

Widget embed code

```
<elevenlabs-convai agent-id="<replace-with-your-agent-id>"></elevenlabs-convai>
<script
  src="https://unpkg.com/@elevenlabs/convai-widget-embed"
  async
  type="text/javascript"
></script>
```

For enhanced security, define allowed domains in your agent’s **Allowlist** (located in the
**Security** tab). This restricts access to specified hosts only.

## Widget attributes

This basic embed code will display the widget with the default configuration defined in the agent’s dashboard.
The widget supports various HTML attributes for further customization:

###### Core configuration

```
<elevenlabs-convai
  agent-id="agent_id"              // Required: Your agent ID
  signed-url="signed_url"          // Alternative to agent-id
  server-location="us"             // Optional: "us" or default
  variant="expanded"               // Optional: Widget display mode
  dismissible="true"               // Optional: Allow the user to minimize the widget
></elevenlabs-convai>
```

###### Visual customization

```
<elevenlabs-convai
  avatar-image-url="https://..." // Optional: Custom avatar image
  avatar-orb-color-1="#6DB035" // Optional: Orb gradient color 1
  avatar-orb-color-2="#F5CABB" // Optional: Orb gradient color 2
></elevenlabs-convai>
```

###### Text customization

```
<elevenlabs-convai
  action-text="Need assistance?" // Optional: CTA button text
  start-call-text="Begin conversation" // Optional: Start call button
  end-call-text="End call" // Optional: End call button
  expand-text="Open chat" // Optional: Expand widget text
  listening-text="Listening..." // Optional: Listening state
  speaking-text="Assistant speaking" // Optional: Speaking state
></elevenlabs-convai>
```

###### Markdown rendering

The widget renders markdown in agent responses. Links display as plain text by default to prevent phishing.

```
<elevenlabs-convai
  markdown-link-allowed-hosts="example.com"  // Domains where links are clickable (use "*" for all)
  markdown-link-include-www="true"           // Also allow www variants (default: true)
  markdown-link-allow-http="true"            // Allow http:// links (default: true)
  syntax-highlight-theme="dark"              // Code block theme: "dark", "light", or "auto"
></elevenlabs-convai>
```

## Runtime configuration

Two more html attributes can be used to customize the agent’s behavior at runtime. These two features can be used together, separately, or not at all

### Dynamic variables

Dynamic variables allow you to inject runtime values into your agent’s messages, system prompts, and tools.

```
<elevenlabs-convai
  agent-id="your-agent-id"
  dynamic-variables='{"user_name": "John", "account_type": "premium"}'
></elevenlabs-convai>
```

All dynamic variables that the agent requires must be passed in the widget.

See more in our [dynamic variables\\
guide](https://elevenlabs.io/docs/agents-platform/customization/personalization/dynamic-variables).

### Overrides

Overrides enable complete customization of your agent’s behavior at runtime:

```
<elevenlabs-convai
  agent-id="your-agent-id"
  override-language="es"
  override-prompt="Custom system prompt for this user"
  override-first-message="Hi! How can I help you today?"
  override-voice-id="axXgspJ2msm3clMCkdW3"
></elevenlabs-convai>
```

Overrides can be enabled for specific fields, and are entirely optional.

See more in our [overrides guide](https://elevenlabs.io/docs/agents-platform/customization/personalization/overrides).

## Visual customization

Customize the widget’s appearance, text content, language selection, and more in the [dashboard](https://elevenlabs.io/app/agents/dashboard) **Widget** tab.

![Widget customization](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/1f773d01a3c0925a47f11cf57153db23bc8bc03b93efe5d7085919886ae392cf/assets/images/conversational-ai/widget-overview.png)

###### Appearance

###### Feedback

###### Avatar

###### Display text

###### Terms

###### Language

###### Muting

###### Shareable page

Customize the widget colors and shapes to match your brand identity.

![Widget appearance](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/0c07c4569f8c5ad3b93933711c268601af411085aa7df1bb8e8ec547a01f2d8e/assets/images/conversational-ai/appearance.gif)

* * *

## Advanced implementation

For more advanced customization, you should use the type-safe [ElevenAgents\\
SDKs](https://elevenlabs.io/docs/developers/resources/libraries) with a Next.js, React, or Python application.

### Client Tools

Client tools allow you to extend the functionality of the widget by adding event listeners. This enables the widget to perform actions such as:

- Redirecting the user to a specific page
- Sending an email to your support team
- Redirecting the user to an external URL

To see examples of these tools in action, start a call with the agent in the bottom right corner of this page. The [source code is available on GitHub](https://github.com/elevenlabs/elevenlabs-docs/blob/main/fern/assets/scripts/widget.js) for reference.

#### Creating a Client Tool

To create your first client tool, follow the [client tools guide](https://elevenlabs.io/docs/agents-platform/customization/tools/client-tools).

Example: Creating the `redirectToExternalURL` Tool

![Client tool configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/d800b8c60cba2ab0a1d0aaaecc0652a678998a4161adaf10d83df51b928a7734/assets/images/conversational-ai/widget-client-tool-setup.png)

#### Example Implementation

Below is an example of how to handle the `redirectToExternalURL` tool triggered by the widget in your JavaScript code:

index.js

```
document.addEventListener('DOMContentLoaded', () => {
  const widget = document.querySelector('elevenlabs-convai');

  if (widget) {
    // Listen for the widget's "call" event to trigger client-side tools
    widget.addEventListener('elevenlabs-convai:call', (event) => {
      event.detail.config.clientTools = {
        // Note: To use this example, the client tool called "redirectToExternalURL" (case-sensitive) must have been created with the configuration defined above.
        redirectToExternalURL: ({ url }) => {
          window.open(url, '_blank', 'noopener,noreferrer');
        },
      };
    });
  }
});
```

Explore our type-safe [SDKs](https://elevenlabs.io/docs/developers/resources/libraries) for React, Next.js, and Python
implementations.

![Widget appearance](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/0c07c4569f8c5ad3b93933711c268601af411085aa7df1bb8e8ec547a01f2d8e/assets/images/conversational-ai/appearance.gif)
