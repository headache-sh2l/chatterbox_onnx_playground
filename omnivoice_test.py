# uv add omnivoice
from omnivoice import OmniVoice
import soundfile as sf
import torch

# Load the model
model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0", 
    dtype=torch.float16
)


# [laughter], [sigh], [confirmation-en], [question-en], [question-ah], [question-oh], [question-ei], [question-yi], [surprise-ah], [surprise-oh], [surprise-wa], [surprise-yo], [dissatisfaction-hnn].

# Reference audio for cloning
ref_audio = "/home/jvk/workspace/playground/playground/huggingface/tts/source/B_MALE1.wav"
ref_text  = "Against the odds, the wild lobster has found a new vessel for its voice. And with it, the possibility to realise its full potential."


# Generate audio
# audio = model.generate(
#     text="Hello, this is a test of zero-shot voice cloning.",
#     ref_audio=ref_audio,
#     ref_text=ref_text, #optional, but can help improve cloning quality if the reference audio is long and contains a lot of phonetic diversity
# ) # audio is a list of `np.ndarray` with shape (T,) at 24 kHz.

# sf.write("out.wav", audio[0], 24000)


# Generate audio without reference text or audio
audio1 = model.generate(
    text="[surprise-oh] You really got me. I didn't see that coming at all [laughter]. Wow, I'm speechless... Wow, just wow. [laughter] . How did you do that?. [question-en]",
    instruct="female, low pitch, british accent",
) # audio is a list of `np.ndarray` with shape (T,) at 24 kHz.
sf.write("audio1.wav", audio1[0], 24000)


audio2 = model.generate(
    text="[surprise-oh] You really got me. I didn't see that coming at all [laughter]. Wow, I'm speechless... Wow, just wow. [laughter] . How did you do that?. [question-en]",
    # instruct="male, child, high pitch, american accent"
    )
sf.write("audio2.wav", audio2[0], 24000)



# audio2 = model.generate(
#     text="[surprise-oh] You really got me. I didn't see that coming at all [laughter]. Wow, I'm speechless... Wow, just wow. [laughter] . How did you do that?. [question-yi]",
# #     instruct="male, child, high pitch, american accent"
# )
# sf.write("audio2.wav", audio2[0], 24000)



# _INSTRUCT_CATEGORIES = [
#     {"male": "男", "female": "女"},
#     {"child": "儿童", "teenager": "少年", "young adult": "青年",
#      "middle-aged": "中年", "elderly": "老年"},
#     {"very low pitch": "极低音调", "low pitch": "低音调",
#      "moderate pitch": "中音调", "high pitch": "高音调",
#      "very high pitch": "极高音调"},
#     {"whisper": "耳语"},
#     # Accent (English-only, no Chinese counterpart)
#     {"american accent", "british accent", "australian accent",
#      "chinese accent", "canadian accent", "indian accent",
#      "korean accent", "portuguese accent", "russian accent", "japanese accent"},
#     # Dialect (Chinese-only, no English counterpart)
#     {"河南话", "陕西话", "四川话", "贵州话", "云南话", "桂林话",
#      "济南话", "石家庄话", "甘肃话", "宁夏话", "青岛话", "东北话"},
# ]
