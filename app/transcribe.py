from watson_developer_cloud import SpeechToTextV1
import cPickle as pickle
import os

stt = SpeechToTextV1(username="56076909-791e-498c-84b9-b56ee1b47932",
                     password="5BKPF3HxSvVq")

def transcribe_audio_watson(string, is_file):
    if not string:
        return
    if is_file:
        with open(string, "rb") as f:
            data = f.read()
    else:
        data = string
    return stt.recognize(
            data, content_type='audio/wav',
            timestamps = True
            )

def parse_watson_result(result):
    """
        Parse the watson speech to text api.
        :rtype ret_list: A list of sentences, should be in ascending order of
                         start_time, each of which is a dictionary.
                         The sentence has the following attributes:
                            text: string, sentence text
                            confidence: float, waston confidence level
                            start_time: float, start time of the sentence in seconds
                            end_time: float, end time of the sentence in seconds
    """
    if "results" not in result:
        raise ValueError("Result does not have \"results\" attribute")
    ret_list = []
    for sen_item in result["results"]:
        if len(sen_item) == 0:
            raise ValueError("No results")
        # Watson by default return the first sentence
        sentence_dict = sen_item["alternatives"][0]
        timestamps = sentence_dict["timestamps"]
        confidence = sentence_dict["confidence"]
        text = sentence_dict["transcript"].strip()
        start_time = timestamps[0][1]
        end_time = timestamps[-1][2]
        sentence = {"text": text,
                    "confidence": confidence,
                    "start_time": start_time,
                    "end_time": end_time
                    }
        ret_list.append(sentence)
    return ret_list

def get_text(sentence_list):
    ret = ". ".join([s["text"].capitalize() for s in sentence_list])
    return ret + "."

def get_sentences(data, save = False):
    """
        :params data: string, can be bytes or file_name for the audio
        :rtype ret: list, a list of sentences
    """
    if os.path.exists("data/demo.txt"):
        with open("data/demo.txt", "r") as f:
            audio_text = f.read()
    else:
        audio_text = transcribe_audio_watson(data, False)
    if audio_text:
        ret = parse_watson_result(audio_text)
        if save:
            with(open("data/demo.txt"), "w") as f:
                f.write(ret)
        return ret
    else:
        print("No result from Watson")


def export_watson_result(result, file_name):
    with open(file_name, "wr") as f:
        pickle.dump(result, f)

def export_transcript(result, file_name):
    parsed_result = parse_watson_result(result)
    with open(file_name, "w") as f:
        f.write(get_text(parsed_result))

if __name__=="__main__":
    result = transcribe_audio_watson("../plan2.wav", True)
    export_watson_result(result, "data/plan2_result.txt")
    export_transcript(result, "data/test4.txt")

