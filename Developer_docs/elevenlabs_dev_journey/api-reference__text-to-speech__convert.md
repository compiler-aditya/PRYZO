<!-- Source: https://elevenlabs.io/docs/api-reference/text-to-speech/convert -->

Converts text into speech using a voice of your choice and returns audio.

### Path parameters

voice\_idstringRequired

ID of the voice to be used. Use the [Get voices](https://elevenlabs.io/docs/api-reference/voices/search) endpoint list all the available voices.

### Headers

xi-api-keystringOptional

### Query parameters

enable\_loggingbooleanOptionalDefaults to `true`

When enable\_logging is set to false zero retention mode will be used for the request. This will mean history features are unavailable for this request, including request stitching. Zero retention mode may only be used by enterprise customers.

optimize\_streaming\_latencyintegerOptionalDeprecated

You can turn on latency optimizations at some cost of quality. The best possible final latency varies by model. Possible values:
0 - default mode (no latency optimizations)
1 - normal latency optimizations (about 50% of possible latency improvement of option 3)
2 - strong latency optimizations (about 75% of possible latency improvement of option 3)
3 - max latency optimizations
4 - max latency optimizations, but also with text normalizer turned off for even more latency savings (best latency, but can mispronounce eg numbers and dates).

Defaults to None.

output\_formatenumOptionalDefaults to `mp3_44100_128`

Output format of the generated audio. Formatted as codec\_sample\_rate\_bitrate. So an mp3 with 22.05kHz sample rate at 32kbs is represented as mp3\_22050\_32. MP3 with 192kbps bitrate requires you to be subscribed to Creator tier or above. PCM and WAV formats with 44.1kHz sample rate requires you to be subscribed to Pro tier or above. Note that the μ-law format (sometimes written mu-law, often approximated as u-law) is commonly used for Twilio audio inputs.

Show 28 enum values

### Request

This endpoint expects an object.

textstringRequired

The text that will get converted into speech.

model\_idstringOptionalDefaults to `eleven_multilingual_v2`

Identifier of the model that will be used, you can query them using GET /v1/models. The model needs to have support for text to speech, you can check this using the can\_do\_text\_to\_speech property.

language\_codestringOptional

Language code (ISO 639-1) used to enforce a language for the model and text normalization. If the model does not support provided language code, an error will be returned.

voice\_settingsobjectOptional

Voice settings overriding stored settings for the given voice. They are applied only on the given request.

Show 5 properties

pronunciation\_dictionary\_locatorslist of objectsOptional

A list of pronunciation dictionary locators (id, version\_id) to be applied to the text. They will be applied in order. You may have up to 3 locators per request

Show 2 properties

seedintegerOptional

If specified, our system will make a best effort to sample deterministically, such that repeated requests with the same seed and parameters should return the same result. Determinism is not guaranteed. Must be integer between 0 and 4294967295.

previous\_textstringOptional

The text that came before the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.

next\_textstringOptional

The text that comes after the text of the current request. Can be used to improve the speech's continuity when concatenating together multiple generations or to influence the speech's continuity in the current generation.

previous\_request\_idslist of stringsOptional

A list of request\_id of the samples that were generated before this generation. Can be used to improve the speech’s continuity when splitting up a large task into multiple requests. The results will be best when the same model is used across the generations. In case both previous\_text and previous\_request\_ids is send, previous\_text will be ignored. A maximum of 3 request\_ids can be send.

next\_request\_idslist of stringsOptional

A list of request\_id of the samples that come after this generation. next\_request\_ids is especially useful for maintaining the speech’s continuity when regenerating a sample that has had some audio quality issues. For example, if you have generated 3 speech clips, and you want to improve clip 2, passing the request id of clip 3 as a next\_request\_id (and that of clip 1 as a previous\_request\_id) will help maintain natural flow in the combined speech. The results will be best when the same model is used across the generations. In case both next\_text and next\_request\_ids is send, next\_text will be ignored. A maximum of 3 request\_ids can be send.

apply\_text\_normalizationenumOptionalDefaults to `auto`

This parameter controls text normalization with three modes: ‘auto’, ‘on’, and ‘off’. When set to ‘auto’, the system will automatically decide whether to apply text normalization (e.g., spelling out numbers). With ‘on’, text normalization will always be applied, while with ‘off’, it will be skipped.

Allowed values:autoonoff

apply\_language\_text\_normalizationbooleanOptionalDefaults to `false`

This parameter controls language text normalization. This helps with proper pronunciation of text in some supported languages. WARNING: This parameter can heavily increase the latency of the request. Currently only supported for Japanese.

use\_pvc\_as\_ivcbooleanOptionalDefaults to `false`Deprecated

If true, we won't use PVC version of the voice for the generation but the IVC version. This is a temporary workaround for higher latency in PVC versions.

### Response

The generated audio file

### Errors

422

Text to Speech Convert Request Unprocessable Entity Error
