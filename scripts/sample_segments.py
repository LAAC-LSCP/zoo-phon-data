import pandas as pd

from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager
from ChildProject.pipelines.samplers import HighVolubilitySampler

project = ChildProject('.')
project.read()

# get the top 20 1-minute regions per recording,
# sorted by 'cvc' (https://github.com/LAAC-LSCP/ChildRecordsData/blob/12aaceaf6307b2f32d7a0faf5e0a36f8db1dcf15/ChildProject/pipelines/samplers.py#L305)
sampler = HighVolubilitySampler(
    project,
    annotation_set = 'its',
    windows_length = 60 * 1000,
    windows_count = 20#,
#    metric = 'cvc'
)
sampler.sample()

am = AnnotationManager(project)
am.read()
annotations = am.annotations[am.annotations['set'] == 'its']

# get ALL child vocalizations from these regions
sample = []
for recording, windows in sampler.segments.groupby('recording_filename'):
    segments = am.get_segments(annotations[annotations['recording_filename'] == recording])
    segments = segments[['recording_filename', 'segment_onset', 'segment_offset', 'speaker_type']]
    segments = segments[segments['speaker_type'] == 'CHI']
    segments['chunk'] = (segments['segment_offset'] // 60000 + 1)
    windows['chunk'] = (windows['segment_offset'] // 60000 + 1)

    sample.append(segments[segments['chunk'].isin(windows['chunk'].tolist())])

print(pd.concat(sample))