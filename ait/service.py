import bentoml
from bentoml.io import Image, JSON

from sd_ait_runnable import SDAITRunnable

sd_ait_runner = bentoml.Runner(SDAITRunnable, name='sd_ait_runner', max_batch_size=10)

svc = bentoml.Service(name="sd_ait", runners=[sd_ait_runner])

@svc.api(input=JSON(), output=Image())
def txt2img(input_data):
    return sd_ait_runner.txt2img.run(input_data)
