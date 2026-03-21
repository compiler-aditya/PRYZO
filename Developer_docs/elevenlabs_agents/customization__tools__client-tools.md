<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools -->

**Client tools** enable your assistant to execute client-side functions. Unlike [server-side tools](https://elevenlabs.io/docs/agents-platform/customization/tools), client tools allow the assistant to perform actions such as triggering browser events, running client-side functions, or sending notifications to a UI.

Give Your Agent Control of the UI – Client Tools & Front-End Actions Explained - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Give Your Agent Control of the UI – Client Tools & Front-End Actions Explained](https://www.youtube.com/watch?v=XeDT92mR7oE)

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

[Watch on](https://www.youtube.com/watch?v=XeDT92mR7oE&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 10:01

•Live

•

## Overview

Applications may require assistants to interact directly with the user’s environment. Client-side tools give your assistant the ability to perform client-side operations.

Here are a few examples where client tools can be useful:

- **Triggering UI events**: Allow an assistant to trigger browser events, such as alerts, modals or notifications.
- **Interacting with the DOM**: Enable an assistant to manipulate the Document Object Model (DOM) for dynamic content updates or to guide users through complex interfaces.

To perform operations server-side, use
[server-tools](https://elevenlabs.io/docs/agents-platform/customization/tools/server-tools) instead.

## Guide

### Prerequisites

- An [ElevenLabs account](https://elevenlabs.io/)
- A configured ElevenLabs Conversational Agent ( [create one here](https://elevenlabs.io/app/agents))

[1](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools#create-a-new-client-side-tool)

### Create a new client-side tool

Navigate to your agent dashboard. In the **Tools** section, click **Add Tool**. Ensure the **Tool Type** is set to **Client**. Then configure the following:

| Setting | Parameter |
| --- | --- |
| Name | logMessage |
| Description | Use this client-side tool to log a message to the user’s client. |

Then create a new parameter `message` with the following configuration:

| Setting | Parameter |
| --- | --- |
| Data Type | String |
| Identifier | message |
| Required | true |
| Description | The message to log in the console. Ensure the message is informative and relevant. |

![logMessage client-tool setup](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/f7ed25d49a2a814b76112f3e385d471e0dc8444705e11f2f6fad0bd23f1eae12/assets/images/conversational-ai/client-tool-example.jpg)

[2](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools#register-the-client-tool-in-your-code)

### Register the client tool in your code

Unlike server-side tools, client tools need to be registered in your code.

Use the following code to register the client tool:

PythonJavaScriptSwift

```
from elevenlabs import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation, ClientTools

def log_message(parameters):
    message = parameters.get("message")
    print(message)

client_tools = ClientTools()
client_tools.register("logMessage", log_message)

conversation = Conversation(
    client=ElevenLabs(api_key="your-api-key"),
    agent_id="your-agent-id",
    client_tools=client_tools,
    # ...
)

conversation.start_session()
```

The tool and parameter names in the agent configuration are case-sensitive and **must** match those registered in your code.

[3](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools#testing)

### Testing

Initiate a conversation with your agent and say something like:

> _Log a message to the console that says Hello World_

You should see a `Hello World` log appear in your console.

[4](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools#next-steps)

### Next steps

Now that you’ve set up a basic client-side event, you can:

- Explore more complex client tools like opening modals, navigating to pages, or interacting with the DOM.
- Combine client tools with server-side webhooks for full-stack interactions.
- Use client tools to enhance user engagement and provide real-time feedback during conversations.

### Passing client tool results to the conversation context

When you want your agent to receive data back from a client tool, ensure that you tick the **Wait for response** option in the tool configuration.

![Wait for response option in client tool configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/0ecc615fc9f25446b67369fd3e010e34b39549a22146a2483ea17251206caf1e/assets/images/conversational-ai/wait-until-tool-result.png)

Once the client tool is added, when the function is called the agent will wait for its response and append the response to the conversation context.

PythonJavaScript

```
def get_customer_details():
    # Fetch customer details (e.g., from an API or database)
    customer_data = {
        "id": 123,
        "name": "Alice",
        "subscription": "Pro"
    }
    # Return the customer data; it can also be a JSON string if needed.
    return customer_data

client_tools = ClientTools()
client_tools.register("getCustomerDetails", get_customer_details)

conversation = Conversation(
    client=ElevenLabs(api_key="your-api-key"),
    agent_id="your-agent-id",
    client_tools=client_tools,
    # ...
)

conversation.start_session()
```

In this example, when the agent calls **getCustomerDetails**, the function will execute on the client and the agent will receive the returned data, which is then used as part of the conversation context. The values from the response can also optionally be assigned to dynamic variables, similar to [server tools](https://elevenlabs.io/docs/agents-platform/customization/tools/server-tools). Note system tools cannot update dynamic variables.

### Troubleshooting

###### Tools not being triggered

- Ensure the tool and parameter names in the agent configuration match those registered in your code.
- View the conversation transcript in the agent dashboard to verify the tool is being executed.

###### Console errors

- Open the browser console to check for any errors.
- Ensure that your code has necessary error handling for undefined or unexpected parameters.

## Best practices

#### Name tools intuitively, with detailed descriptions

If you find the assistant does not make calls to the correct tools, you may need to update your tool names and descriptions so the assistant more clearly understands when it should select each tool. Avoid using abbreviations or acronyms to shorten tool and argument names.

You can also include detailed descriptions for when a tool should be called. For complex tools, you should include descriptions for each of the arguments to help the assistant know what it needs to ask the user to collect that argument.

#### Name tool parameters intuitively, with detailed descriptions

Use clear and descriptive names for tool parameters. If applicable, specify the expected format for a parameter in the description (e.g., YYYY-mm-dd or dd/mm/yy for a date).

#### Consider providing additional information about how and when to call tools in your assistant’s system prompt

Providing clear instructions in your system prompt can significantly improve the assistant’s tool calling accuracy. For example, guide the assistant with instructions like the following:

```
Use `check_order_status` when the user inquires about the status of their order, such as 'Where is my order?' or 'Has my order shipped yet?'.
```

Provide context for complex scenarios. For example:

```
Before scheduling a meeting with `schedule_meeting`, check the user's calendar for availability using check_availability to avoid conflicts.
```

#### LLM selection

When using tools, we recommend picking high intelligence models like GPT-4o mini or Claude 3.5
Sonnet and avoiding Gemini 1.5 Flash.

It’s important to note that the choice of LLM matters to the success of function calls. Some LLMs can struggle with extracting the relevant parameters from the conversation.
