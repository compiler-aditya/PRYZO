<!-- Source: https://elevenlabs.io/docs/api-reference/speech-to-text/convert -->

Transcribe an audio or video file. If webhook is set to true, the request will be processed asynchronously and results sent to configured webhooks. When use\_multi\_channel is true and the provided audio has multiple channels, a ‘transcripts’ object with separate transcripts for each channel is returned. Otherwise, returns a single transcript. The optional webhook\_metadata parameter allows you to attach custom data that will be included in webhook responses for request correlation and tracking.

### Headers

xi-api-keystringOptional

### Query parameters

enable\_loggingbooleanOptionalDefaults to `true`

When enable\_logging is set to false zero retention mode will be used for the request. This will mean log and transcript storage features are unavailable for this request. Zero retention mode may only be used by enterprise customers.

### Request

This endpoint expects a multipart form containing an optional file.

model\_idenumRequired

The ID of the model to use for transcription.

Allowed values:scribe\_v2scribe\_v1

filefileOptional

The file to transcribe. All major audio and video formats are supported. Exactly one of the file or cloud\_storage\_url parameters must be provided. The file size must be less than 3.0GB.

language\_codestringOptional

An ISO-639-1 or ISO-639-3 language\_code corresponding to the language of the audio file. Can sometimes improve transcription performance if known beforehand. Defaults to null, in this case the language is predicted automatically.

tag\_audio\_eventsbooleanOptionalDefaults to `true`

Whether to tag audio events like (laughter), (footsteps), etc. in the transcription.

num\_speakersintegerOptional`1-32`

The maximum amount of speakers talking in the uploaded file. Can help with predicting who speaks when. The maximum amount of speakers that can be predicted is 32. Defaults to null, in this case the amount of speakers is set to the maximum value the model supports.

timestamps\_granularityenumOptionalDefaults to `word`

The granularity of the timestamps in the transcription. ‘word’ provides word-level timestamps and ‘character’ provides character-level timestamps per word.

Allowed values:nonewordcharacter

diarizebooleanOptionalDefaults to `false`

Whether to annotate which speaker is currently talking in the uploaded file.

diarization\_thresholddoubleOptional`0.1-0.4`

Diarization threshold to apply during speaker diarization. A higher value means there will be a lower chance of one speaker being diarized as two different speakers but also a higher chance of two different speakers being diarized as one speaker (less total speakers predicted). A low value means there will be a higher chance of one speaker being diarized as two different speakers but also a lower chance of two different speakers being diarized as one speaker (more total speakers predicted). Can only be set when diarize=True and num\_speakers=None. Defaults to None, in which case we will choose a threshold based on the model\_id (0.22 usually).

additional\_formatslist of objectsOptional

A list of additional formats to export the transcript to.

Show 6 variants

file\_formatenumOptionalDefaults to `other`

The format of input audio. Options are ‘pcm\_s16le\_16’ or ‘other’ For `pcm_s16le_16`, the input audio must be 16-bit PCM at a 16kHz sample rate, single channel (mono), and little-endian byte order. Latency will be lower than with passing an encoded waveform.

Allowed values:pcm\_s16le\_16other

cloud\_storage\_urlstringOptional

The HTTPS URL of the file to transcribe. Exactly one of the file or cloud\_storage\_url parameters must be provided. The file must be accessible via HTTPS and the file size must be less than 2GB. Any valid HTTPS URL is accepted, including URLs from cloud storage providers (AWS S3, Google Cloud Storage, Cloudflare R2, etc.), CDNs, or any other HTTPS source. URLs can be pre-signed or include authentication tokens in query parameters.

webhookbooleanOptionalDefaults to `false`

Whether to send the transcription result to configured speech-to-text webhooks. If set the request will return early without the transcription, which will be delivered later via webhook.

webhook\_idstringOptional

Optional specific webhook ID to send the transcription result to. Only valid when webhook is set to true. If not provided, transcription will be sent to all configured speech-to-text webhooks.

temperaturedoubleOptional`0-2`

Controls the randomness of the transcription output. Accepts values between 0.0 and 2.0, where higher values result in more diverse and less deterministic results. If omitted, we will use a temperature based on the model you selected which is usually 0.

seedintegerOptional`0-2147483647`

If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be an integer between 0 and 2147483647.

use\_multi\_channelbooleanOptionalDefaults to `false`

Whether the audio file contains multiple channels where each channel contains a single speaker. When enabled, each channel will be transcribed independently and the results will be combined. Each word in the response will include a ‘channel\_index’ field indicating which channel it was spoken on. A maximum of 5 channels is supported.

webhook\_metadatastring or map from strings to anyOptional

Optional metadata to be included in the webhook response. This should be a JSON string representing an object with a maximum depth of 2 levels and maximum size of 16KB. Useful for tracking internal IDs, job references, or other contextual information.

Show 2 variants

entity\_detectionstring or list of stringsOptional

Detect entities in the transcript. Can be ‘all’ to detect all entities, a single entity type or category string, or a list of entity types/categories. Categories include ‘pii’, ‘phi’, ‘pci’, ‘other’, ‘offensive\_language’. When enabled, detected entities will be returned in the ‘entities’ field with their text, type, and character positions. Usage of this parameter will incur additional costs.

Show 2 variants

no\_verbatimbooleanOptionalDefaults to `false`

If true, the transcription will not have any filler words, false starts and non-speech sounds. Only supported with scribe\_v2 model.

entity\_redactionstring or list of stringsOptional

Redact entities from the transcript text. Accepts the same format as entity\_detection: ‘all’, a category (‘pii’, ‘phi’), or specific entity types. Must be a subset of entity\_detection. When redaction is enabled, the entities field will not be returned.

Show 2 variants

entity\_redaction\_modestringOptionalDefaults to `enumerated_entity_type`

How to format redacted entities. ‘redacted’ replaces with {REDACTED}, ‘entity\_type’ replaces with {ENTITY\_TYPE}, ‘enumerated\_entity\_type’ replaces with {ENTITY\_TYPE\_N} where N enumerates each occurrence. Only used when entity\_redaction is set.

keytermslist of stringsOptional

A list of keyterms to bias the transcription towards. The keyterms are words or phrases you want the model to recognise more accurately. The number of keyterms cannot exceed 100. The length of each keyterm must be less than 50 characters. Keyterms can contain at most 5 words (after normalisation). For example \[“hello”, “world”, “technical term”\]. Usage of this parameter will incur additional costs.

### Response

Synchronous transcription result

Speech to Text Chunk Response Modelobject

Show 8 properties

OR

Multichannel Speech to Text Response Modelobject

Show 2 properties

OR

Speech to Text Webhook Response Modelobject

Show 3 properties

### Errors

422

Speech to Text Convert Request Unprocessable Entity Error
