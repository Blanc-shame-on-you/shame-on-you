sys.path.append('C:/workspace/2020_kdn/shame-on-you/models/mask_detect/')
from tensorflow_mask_detect import inference
from .convention import bitOperation

def detect(img_raw):
        result, locations =inference(img_raw)
        
        if result > 0:
            return bitOperation(locations)
            pass
        else:
            pass
        
        print("infer time:%f" % (write_frame_stamp - inference_stamp))