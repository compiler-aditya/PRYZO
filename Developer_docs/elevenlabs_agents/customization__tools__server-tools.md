<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/tools/server-tools -->

**Tools** enable your assistant to connect to external data and systems. You can define a set of tools that the assistant has access to, and the assistant will use them where appropriate based on the conversation.

Add Real‑Time Data to Your Agent – Server Webhook Tools Explained - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Add Real‑Time Data to Your Agent – Server Webhook Tools Explained](https://www.youtube.com/watch?v=pB33QxKN8P8)

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

[Watch on](https://www.youtube.com/watch?v=pB33QxKN8P8&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 8:02

•Live

•

## Overview

Many applications require assistants to call external APIs to get real-time information. Tools give your assistant the ability to make external function calls to third party apps so you can get real-time information.

Here are a few examples where tools can be useful:

- **Fetching data**: enable an assistant to retrieve real-time data from any REST-enabled database or 3rd party integration before responding to the user.
- **Taking action**: allow an assistant to trigger authenticated actions based on the conversation, like scheduling meetings or initiating order returns.

To interact with Application UIs or trigger client-side events use [client\\
tools](https://elevenlabs.io/docs/agents-platform/customization/tools/client-tools) instead.

## Tool configuration

ElevenLabs agents can be equipped with tools to interact with external APIs. Unlike traditional requests, the assistant generates query, body, and path parameters dynamically based on the conversation and parameter descriptions you provide.

All tool configurations and parameter descriptions help the assistant determine **when** and **how** to use these tools. To orchestrate tool usage effectively, update the assistant’s system prompt to specify the sequence and logic for making these calls. This includes:

- **Which tool** to use and under what conditions.
- **What parameters** the tool needs to function properly.
- **How to handle** the responses.

###### Configuration

###### Authentication

###### Headers

###### Path parameters

###### Body parameters

###### Query parameters

###### Dynamic variable assignment

Define a high-level `Name` and `Description` to describe the tool’s purpose. This helps the LLM understand the tool and know when to call it.

If the API requires path parameters, include variables in the URL path by wrapping them in curly
braces `{}`, for example: `/api/resource/{id}` where `id` is a path parameter.

![Configuration](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/fb6e6619e4e7a5f19c2a86f9c2a489f5cb33cfb0883c14a06f0eec3cb35d71d5/assets/images/conversational-ai/tool-configuration.jpg)

## Guide

In this guide, we’ll create a weather assistant that can provide real-time weather information for any location. The assistant will use its geographic knowledge to convert location names into coordinates and fetch accurate weather data.

weatheragent from Angelo Giacco on Vimeo

![video thumbnail](https://i.vimeocdn.com/video/1988095008-2b29c09efc1e27ba6fe7d345bc07c24dfb8136cfac93876ff723c335ee7bf3cc-d?mw=80&q=85)

Playing in picture-in-picture

Like

Add to Watch Later

Play

00:00

02:36

Settings

QualityAuto

SpeedNormal

Picture-in-PictureFullscreen

[Watch on Vimeo](https://vimeo.com/1061374724/bd9bdb535e?fl=pl&fe=vl)

[1](https://elevenlabs.io/docs/eleven-agents/customization/tools/server-tools#configure-the-weather-tool)

### Configure the weather tool

First, on the **Agent** section of your agent settings page, choose **Add Tool**. Select **Webhook** as the Tool Type, then configure the weather API integration:

###### Weather Tool Configuration

###### Configuration

###### Path Parameters

| Field | Value |
| --- | --- |
| Name | get\_weather |
| Description | Gets the current weather forecast for a location |
| Method | GET |
| URL | [https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature\_2m,wind\_speed\_10m&hourly=temperature\_2m,relative\_humidity\_2m,wind\_speed\_10m](https://api.open-meteo.com/v1/forecast?latitude=%7Blatitude%7D&longitude=%7Blongitude%7D&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m) |

An API key is not required for this tool. If one is required, this should be passed in the headers and stored as a secret.

[2](https://elevenlabs.io/docs/eleven-agents/customization/tools/server-tools#orchestration)

### Orchestration

Configure your assistant to handle weather queries intelligently with this system prompt:

System prompt

```
You are a helpful conversational agent with access to a weather tool. When users ask about
weather conditions, use the get_weather tool to fetch accurate, real-time data. The tool requires
a latitude and longitude - use your geographic knowledge to convert location names to coordinates
accurately.

Never ask users for coordinates - you must determine these yourself. Always report weather
information conversationally, referring to locations by name only. For weather requests:

1. Extract the location from the user's message
2. Convert the location to coordinates and call get_weather
3. Present the information naturally and helpfully

For non-weather queries, provide friendly assistance within your knowledge boundaries. Always be
concise, accurate, and helpful.

First message: "Hey, how can I help you today?"
```

Test your assistant by asking about the weather in different locations. The assistant should
handle specific locations (“What’s the weather in Tokyo?”) and ask for clarification after general queries (“How’s
the weather looking today?”).

## Supported Authentication Methods

ElevenLabs Agents supports multiple authentication methods to securely connect your tools with external APIs. Authentication methods are configured in your agent settings and then connected to individual tools as needed.

![Workspace Auth Connection](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/131f7e017f01eaba444cddc672efdb77415db1a4c3a39f05b92a1678c5cd68f1/assets/images/conversational-ai/workspace-auth-connection.png)

Once configured, you can connect these authentication methods to your tools and manage custom headers in the tool configuration:

![Tool Auth Connection](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/c018c5bf11266512a6d6157e33274b1a12f8c20768e5ab18da0f20f933f8aea9/assets/images/conversational-ai/tool-auth-config.png)

#### OAuth2 Client Credentials

Automatically handles the OAuth2 client credentials flow. Configure with your client ID, client secret, and token URL (e.g., `https://api.example.com/oauth/token`). Optionally specify scopes as comma-separated values and additional JSON parameters. Set up by clicking **Add Auth** on **Workspace Auth Connections** on the **Agent** section of your agent settings page.

#### OAuth2 JWT

Uses JSON Web Token authentication for OAuth 2.0 JWT Bearer flow. Requires your JWT signing secret, token URL, and algorithm (default: HS256). Configure JWT claims including issuer, audience, and subject. Optionally set key ID, expiration (default: 3600 seconds), scopes, and extra parameters. Set up by clicking **Add Auth** on **Workspace Auth Connections** on the **Agent** section of your agent settings page.

#### Basic Authentication

Simple username and password authentication for APIs that support HTTP Basic Auth. Set up by clicking **Add Auth** on **Workspace Auth Connections** in the **Agent** section of your agent settings page.

#### Bearer Tokens

Token-based authentication that adds your bearer token value to the request header. Configure by adding a header to the tool configuration, selecting **Secret** as the header type, and clicking **Create New Secret**.

#### Custom Headers

Add custom authentication headers with any name and value for proprietary authentication methods. Configure by adding a header to the tool configuration and specifying its **name** and **value**.

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

## Tool Call Sounds

You can configure ambient audio to play during tool execution to enhance the user experience. Learn more about [Tool Call Sounds](https://elevenlabs.io/agents-platform/customization/tools/tool-configuration/tool-call-sounds).
