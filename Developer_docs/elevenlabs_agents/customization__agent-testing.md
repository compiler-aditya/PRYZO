<!-- Source: https://elevenlabs.io/docs/eleven-agents/customization/agent-testing -->

The agent testing framework enables you to move from slow, manual phone calls to a fast, automated, and repeatable testing process. Create comprehensive test suites that verify both conversational responses and tool usage, ensuring your agents behave exactly as intended before deploying to production.

## Video Walkthrough

Intro to ElevenLabs Agent Testing - YouTube

[Photo image of ElevenLabs](https://www.youtube.com/channel/UC-ew9TfeD887qUSiWWAAj1w?embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

ElevenLabs

117K subscribers

[Intro to ElevenLabs Agent Testing](https://www.youtube.com/watch?v=SvyrPTNpWas)

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

[Watch on](https://www.youtube.com/watch?v=SvyrPTNpWas&embeds_referring_euri=https%3A%2F%2Felevenlabs.io%2F)

0:00

0:00 / 2:04

•Live

•

## Overview

The framework consists of two complementary testing approaches:

- **Scenario Testing (LLM Evaluation)** \- Validates conversational abilities and response quality
- **Tool Call Testing** \- Ensures proper tool usage and parameter validation

Both test types can be created from scratch or directly from existing conversations, allowing you to quickly turn real-world interactions into repeatable test cases.

## Scenario Testing (LLM Evaluation)

Scenario testing evaluates your agent’s conversational abilities by simulating interactions and assessing responses against defined success criteria.

### Creating a Scenario Test

![Scenario Testing Interface](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/62de63965584fd1b2368edfb204bd90495d03ba87fe137889a5f396859dc4dbc/assets/images/conversational-ai/agent-llm-eval-test.png)

[1](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#define-the-scenario)

### Define the scenario

Create context for the text. This can be multiple turns of interaction that sets up the specific scenario you want to evaluate. Our testing framework currently only supports evaluating a single next step in the conversation. For simulating entire conversations, see our [simulate conversation endpoint](https://elevenlabs.io/docs/api-reference/agents/simulate-conversation) and [conversation simulation guide](https://elevenlabs.io/docs/agents-platform/guides/simulate-conversations).

**Example scenario:**

```
User: "I'd like to cancel my subscription. I've been charged twice this month and I'm frustrated."
```

[2](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#set-success-criteria)

### Set success criteria

Describe in plain language what the agent’s response should achieve. Be specific about the
expected behavior, tone, and actions.

**Example criteria:**

- The agent should acknowledge the customer’s frustration with empathy
- The agent should offer to investigate the duplicate charge
- The agent should provide clear next steps for cancellation or resolution
- The agent should maintain a professional and helpful tone

[3](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#provide-examples)

### Provide examples

Supply both success and failure examples to help the evaluator understand the nuances of your
criteria.

**Success Example:**

> “I understand how frustrating duplicate charges can be. Let me look into this right away for you. I can see there were indeed two charges this month - I’ll process a refund for the duplicate charge immediately. Would you still like to proceed with cancellation, or would you prefer to continue once this is resolved?”

**Failure Example:**

> “You need to contact billing department for refund issues. Your subscription will be cancelled.”

[4](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#run-the-test)

### Run the test

Execute the test to simulate the conversation with your agent. An LLM evaluator compares the
actual response against your success criteria and examples to determine pass/fail status.

### Creating Tests from Conversations

Transform real conversations into test cases with a single click. This powerful feature creates a feedback loop for continuous improvement based on actual performance.

![Creating test from conversation](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/7b0762965b7edb46ed6b693c126c00e9aa3e7c98dae7aa89a981b5465b949750/assets/images/conversational-ai/agent-test-from-conv.gif)

When reviewing call history, if you identify a conversation where the agent didn’t perform well:

1. Click “Create test from this conversation”
2. The framework automatically populates the scenario with the actual conversation context
3. Define what the correct behavior should have been
4. Add the test to your suite to prevent similar issues in the future

## Tool Call Testing

Tool call testing verifies that your agent correctly uses tools and passes the right parameters in specific situations. This is critical for actions like call transfers, data lookups, or external integrations.

### Creating a Tool Call Test

![Tool Call Testing Interface](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/291c48ac70376efa1991014f7b3ff90eb9910c9adffe250f2bf521c707c5c755/assets/images/conversational-ai/agent-tool-call-test.png)

[1](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#select-the-tool)

### Select the tool

Choose which tool you expect the agent to call in the given scenario (e.g.,
`transfer_to_number`, `end_call`, `lookup_order`).

[2](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#define-expected-parameters)

### Define expected parameters

Specify what data the agent should pass to the tool. You have three validation methods:

###### Validation Methods

**Exact Match**

The parameter must exactly match your specified value.

```
Transfer number: +447771117777
```

**Regex Pattern**
The parameter must match a specific pattern.

```
Order ID: ^ORD-[0-9]{8}$
```

**LLM Evaluation**
An LLM evaluates if the parameter is semantically correct based on context.

```
Message: "Should be a polite message mentioning the connection"
```

[3](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#configure-dynamic-variables)

### Configure dynamic variables

When testing in development, use dynamic variable values that match those that would be actual
values in production. Example: `{{ customer_name }}` or `{{ order_id }}`

[4](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#run-and-validate)

### Run and validate

Execute the test to ensure the agent calls the correct tool with proper parameters.

### Critical Use Cases

Tool call testing is essential for high-stakes scenarios:

- **Emergency Transfers**: Ensure medical emergencies always route to the correct number
- **Data Security**: Verify sensitive information is never passed to unauthorized tools
- **Business Logic**: Confirm order lookups use valid formats and authentication

## Development Workflow

The framework supports an iterative development cycle that accelerates agent refinement:

[1](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#write-tests-first)

### Write tests first

Define the desired behavior by creating tests for new features or identified issues.

[2](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#test-and-iterate)

### Test and iterate

Run tests instantly without saving changes. Watch them fail, then adjust your agent’s prompts or
configuration.

[3](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#refine-until-passing)

### Refine until passing

Continue tweaking and re-running tests until all pass. The framework provides immediate feedback
without requiring deployment.

[4](https://elevenlabs.io/docs/eleven-agents/customization/agent-testing#save-with-confidence)

### Save with confidence

Once tests pass, save your changes knowing the agent behaves as intended.

## Running Tests

Navigate to the Tests tab in your agent’s interface. From there, you can run individual tests or execute your entire test suite at once using the “Run All Tests” button.

![Running tests on an agent](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/b1becf589a1373a780dad1109fd25e0e910d7aa821b09b047133553b1895914b/assets/images/conversational-ai/testrun.gif)

## Batch Testing and CI/CD Integration

### Running Test Suites

Execute all tests at once to ensure comprehensive coverage:

1. Select multiple tests from your test library
2. Run as a batch to identify any regressions
3. Review consolidated results showing pass/fail status for each test

### CLI Integration

Integrate testing into your development pipeline using the ElevenLabs CLI:

```
# Run all tests for an agent
elevenlabs agents test <your_agent_id>
```

This enables:

- Automated testing on every code change
- Prevention of regressions before deployment
- Consistent agent behavior across environments

## Best Practices

Evaluate agent persona consistency

Test that your agent maintains its defined personality, tone, and behavioral boundaries across
diverse conversation scenarios and emotional contexts.

Verify complex multi-turn reasoning

Create scenarios that test the agent’s ability to maintain context, follow conditional logic,
and handle state transitions across extended conversations.

Test against prompt injection attempts

Evaluate how your agent responds to attempts to override its instructions or extract sensitive
system information through adversarial inputs.

Assess ambiguous intent resolution

Test how effectively your agent clarifies vague requests, handles conflicting information, and
navigates situations where user intent is unclear.

## Next Steps

- [View CLI Documentation](https://elevenlabs.io/docs/agents-platform/operate/cli) for automated testing setup
- [Explore Tool Configuration](https://elevenlabs.io/docs/agents-platform/customization/tools) to understand available tools
- [Read the Prompting Guide](https://elevenlabs.io/docs/agents-platform/best-practices/prompting-guide) for writing testable prompts

![Creating test from conversation](https://files.buildwithfern.com/https://elevenlabs.docs.buildwithfern.com/docs/7b0762965b7edb46ed6b693c126c00e9aa3e7c98dae7aa89a981b5465b949750/assets/images/conversational-ai/agent-test-from-conv.gif)
