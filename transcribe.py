from watson_developer_cloud import SpeechToTextV1
stt = SpeechToTextV1(username="56076909-791e-498c-84b9-b56ee1b47932",
                     password="5BKPF3HxSvVq")

def transcribe_file_watson(file_name):
    with open(file_name,
          'rb') as audio_file:
        return stt.recognize(
            audio_file, content_type='audio/wav',
            speaker_labels=True)

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
    return ".".join([s["text"].capitalize() for s in sentence_list])


if __name__=="__main__":
    result = transcribe_file_watson("part1.wav")

