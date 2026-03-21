<!-- Source: https://elevenlabs.io/docs/eleven-api/resources/errors -->

## API errors

ElevenLabs uses standard HTTP status codes to indicate the success or failure of a request. Additionally, all API requests return a JSON object with a `detail` property that contains information about the error.

In general, a `200` HTTP status code indicates a successful request. A `4xx` code indicates a problem with the request, like an invalid parameter or missing required field. A `500` HTTP status code indicates a problem with ElevenLabs’ servers, which should be rare.

### Error properties

| Property | Description |
| --- | --- |
| `type` | The type of error that occurred. See the table below for possible values. |
| `code` | The code of the error. These are more specific than the type, and can be used to determine the cause of the error. |
| `message` | The message of the error. This provides more details about the error. |
| `status` | The status of the error. This is a legacy field that is no longer used, instead use the `code` property. |
| `request_id` | The request ID of the error. This is a unique identifier for the request that can be used to troubleshoot the error. |
| `param` | The parameter that caused the error. In the case of a validation error, this will indicate the parameter that is invalid. |

### Example error response

Here’s the response for an API request that used an incorrect model ID:

```
{
  "detail": {
    "type": "validation_error",
    "code": "invalid_parameters",
    "message": "The 'keyterms' parameter is only supported with the 'scribe_v2' model. You specified 'scribe_v1'.",
    "status": "invalid_parameters",
    "request_id": "3c807fc4c3a1705f9638ecc764a91c01",
    "param": "keyterms"
  }
}
```

Using the error properties, we can see that the error is a validation error, and the code is `invalid_parameters`. The message provides more details about the error, and the `request_id` is a unique identifier for the request that can be used to troubleshoot the error. The `param` property indicates the parameter that caused the error.

### SDK error handling

The ElevenLabs SDKs provide typed error classes that give you access to the error details.

PythonTypeScript

```
from elevenlabs import ElevenLabs, ApiError

elevenlabs = ElevenLabs()

try:
    audio = elevenlabs.text_to_speech.convert(
        voice_id="invalid-voice-id",
        model_id="eleven_v3",
        text="Hello, world!",
    )
except ApiError as e:
    print(f"Status code: {e.status_code}")

    # Access the error body
    if e.body and "detail" in e.body:
        detail = e.body["detail"]
        print(f"Error type: {detail.get('type')}")
        print(f"Error code: {detail.get('code')}")
        print(f"Message: {detail.get('message')}")
        print(f"Request ID: {detail.get('request_id')}")

        # Handle specific error types
        if detail.get("type") == "rate_limit_error":
            print("Rate limited - implement exponential backoff")
        elif detail.get("type") == "authentication_error":
            print("Check your API key")
```

#### Rate limiting and concurrency

If you receive a 429 HTTP status code, it means you have either made too many requests in a short period of time and exceeded the rate limit for the API endpoint, or you have exceeded the concurrency limit for the API endpoint. The error `code` will be `rate_limit_exceeded` or `concurrent_limit_exceeded` respectively.

In the case of rate limiting, you should implement exponential backoff in your code when a 429 error is received. This means adding a delay before retrying the request.

In the case of concurrency, you should wait for the current requests to complete before making new ones. See the [Concurrency and priority](https://elevenlabs.io/docs/overview/models#concurrency-and-priority) section for more information.

### Error types

An error comes with a `type` property that indicates the type of error that occurred. See the table below for possible values.

| Type | Description | HTTP Status Code |
| --- | --- | --- |
| `validation_error` | The request contains invalid parameter values. | 400 |
| `invalid_request` | The request structure is malformed or missing required fields. | 400 |
| `authentication_error` | Authentication failed - invalid or missing API key/token. | 401 |
| `payment_required` | User has insufficient credits or payment is required. | 402 |
| `authorization_error` | The authenticated user doesn’t have the required permissions for this action. | 403 |
| `not_found` | The requested resource was not found. | 404 |
| `conflict` | The request conflicts with the current state of the resource. | 409 |
| `rate_limit_error` | Too many requests - try again later. | 429 |
| `internal_error` | An unexpected server error occurred. | 500 |
| `service_unavailable` | The service is temporarily unavailable, this should be a rare occurrence. | 503 |

### Error codes

| Code | Type | Description |
| --- | --- | --- |
| `voice_not_found` | `not_found` | The specified voice ID does not exist. Verify the voice ID and try again. |
| `sample_not_found` | `not_found` | The specified voice sample was not found. |
| `voice_collection_not_found` | `not_found` | The specified voice collection does not exist. |
| `user_not_found` | `not_found` | The specified user was not found. |
| `auth_account_not_found` | `not_found` | The authentication account was not found. |
| `workspace_not_found` | `not_found` | The specified workspace does not exist. |
| `project_not_found` | `not_found` | The specified project was not found. |
| `history_item_not_found` | `not_found` | The specified history item does not exist. |
| `collection_not_found` | `not_found` | The specified collection was not found. |
| `document_not_found` | `not_found` | The specified document does not exist. |
| `file_not_found` | `not_found` | The specified file was not found. |
| `conversation_not_found` | `not_found` | The specified conversation does not exist. |
| `agent_not_found` | `not_found` | The specified agent was not found. |
| `dubbing_not_found` | `not_found` | The specified dubbing project does not exist. |
| `song_not_found` | `not_found` | The specified song was not found. |
| `read_not_found` | `not_found` | The specified read was not found. |
| `pronunciation_dictionary_not_found` | `not_found` | The specified pronunciation dictionary does not exist. |
| `knowledge_base_not_found` | `not_found` | The specified knowledge base was not found. |
| `phone_number_not_found` | `not_found` | The specified phone number does not exist. |
| `tool_not_found` | `not_found` | The specified tool was not found. |
| `snapshot_not_found` | `not_found` | The specified snapshot does not exist. |
| `task_not_found` | `not_found` | The specified task was not found. |
| `model_not_found` | `not_found` | The specified model does not exist. |
| `transcript_not_found` | `not_found` | The specified transcript was not found. |
| `keywords_list_not_found` | `not_found` | The specified keywords list was not found. |
| `category_not_found` | `not_found` | The specified category was not found. |
| `text_too_long` | `validation_error` | The provided text exceeds the maximum allowed length. |
| `text_too_short` | `validation_error` | The provided text is shorter than the minimum required length. |
| `invalid_text` | `validation_error` | The provided text contains invalid characters or formatting. |
| `empty_text` | `validation_error` | The text field cannot be empty. |
| `invalid_parameters` | `validation_error` | One or more request parameters are invalid. Check the `param` property for the invalid<br>parameter. |
| `missing_required_field` | `validation_error` | A required field is missing from the request. Check the `param` property for the missing<br>field. |
| `invalid_voice_settings` | `validation_error` | The voice settings contain invalid values. Check the `param` property for the invalid voice<br>settings. |
| `invalid_voice_id` | `validation_error` | The voice ID format is invalid. |
| `unsupported_model` | `validation_error` | The specified model is not supported for this operation. |
| `invalid_audio` | `validation_error` | The provided audio is invalid or corrupted. |
| `invalid_audio_format` | `validation_error` | The specified audio format is not supported. |
| `invalid_output_format` | `validation_error` | The requested output format is not supported. |
| `audio_too_long` | `validation_error` | The audio exceeds the maximum allowed duration. |
| `audio_too_short` | `validation_error` | The audio is shorter than the minimum required duration. |
| `invalid_file_type` | `validation_error` | The file type is not supported. |
| `invalid_page_size` | `validation_error` | The page size parameter is outside the allowed range. |
| `invalid_cursor` | `validation_error` | The pagination cursor is invalid or expired. |
| `bad_request` | `invalid_request` | The request could not be understood by the server. |
| `malformed_json` | `invalid_request` | The request body contains invalid JSON. |
| `invalid_content_type` | `invalid_request` | The Content-Type header is missing or invalid. |
| `request_too_large` | `invalid_request` | The request body exceeds the maximum allowed size. |
| `invalid_api_key` | `authentication_error` | The provided API key is invalid. |
| `missing_api_key` | `authentication_error` | No API key was provided in the request. |
| `invalid_authorization_header` | `authentication_error` | The Authorization header format is invalid. |
| `unauthorized` | `authentication_error` | Authentication is required to access this resource. |
| `sign_in_required` | `authentication_error` | You must be signed in to perform this action. |
| `forbidden` | `authorization_error` | Access to this resource is forbidden. |
| `insufficient_permissions` | `authorization_error` | You do not have the required permissions for this action. |
| `workspace_access_denied` | `authorization_error` | You do not have access to this workspace. |
| `feature_not_available` | `authorization_error` | This feature is not available on your current plan. |
| `subscription_required` | `authorization_error` | A paid subscription is required to access this feature. |
| `voice_access_denied` | `authorization_error` | You do not have access to this voice. |
| `model_access_denied` | `authorization_error` | You do not have access to this model. |
| `conflict` | `conflict` | A conflict occurred. |
| `resource_already_exists` | `conflict` | A resource with the same identifier already exists. |
| `voice_already_exists` | `conflict` | A voice with this name already exists. |
| `already_running` | `conflict` | The operation is already running. |
| `already_processing` | `conflict` | The resource is already being processed. |
| `concurrent_modification` | `conflict` | The resource was modified by another request. Retry with the latest version. |
| `slug_already_exists` | `conflict` | A resource with this slug already exists. |
| `rate_limit_exceeded` | `rate_limit_error` | Too many requests. Wait before retrying. |
| `concurrent_limit_exceeded` | `rate_limit_error` | Maximum number of concurrent requests exceeded. Higher subscription tiers have a higher<br>concurrency limit. |
| `system_busy` | `rate_limit_error` | The system is currently busy. Try again later. |
| `insufficient_credits` | `payment_required` | Your account does not have enough credits for this operation. |
| `internal_error` | `internal_error` | An unexpected error occurred. Contact support if this persists. |
| `service_unavailable` | `service_unavailable` | The service is temporarily unavailable. Try again later. |
| `maintenance` | `service_unavailable` | The service is undergoing scheduled maintenance. |
