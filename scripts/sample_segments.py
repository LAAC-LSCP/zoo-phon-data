import os
import pandas as pd

from ChildProject.projects import ChildProject
from ChildProject.annotations import AnnotationManager
from ChildProject.pipelines.samplers import HighVolubilitySampler, RandomVocalizationSampler

project = ChildProject('.')
project.read()

# get the top 20 1-minute regions per recording,
# sorted by 'cvc' (https://github.com/LAAC-LSCP/ChildRecordsData/blob/12aaceaf6307b2f32d7a0faf5e0a36f8db1dcf15/ChildProject/pipelines/samplers.py#L305)
high_volubility_sampler = HighVolubilitySampler(
    project,
    annotation_set = 'its',
    windows_length = 60 * 1000,
    windows_count = 20,
    metric = 'cvc',
    threads = 1
)
high_volubility_sampler.sample()

am = AnnotationManager(project)
am.read()
annotations = am.annotations[am.annotations['set'] == 'its']

# get ALL child vocalizations from these regions
high_volubility_samples = []
for recording, windows in high_volubility_sampler.segments.groupby('recording_filename'):
    segments = am.get_segments(annotations[annotations['recording_filename'] == recording])
    segments = segments[['recording_filename', 'segment_onset', 'segment_offset', 'speaker_type']]
    segments = segments[segments['speaker_type'] == 'CHI']
    segments['chunk'] = (segments['segment_offset'] // 60000 + 1)
    windows['chunk'] = (windows['segment_offset'] // 60000 + 1)
    segments = segments[segments['chunk'].isin(windows['chunk'].tolist())]
    high_volubility_samples.append(segments)

high_volubility_samples = pd.concat(high_volubility_samples)

os.makedirs('samples/gold/high', exist_ok = True)
high_volubility_samples.to_csv('samples/gold/high/samples.csv', index = False)
high_volubility_sampler.segments = high_volubility_samples
high_volubility_sampler.export_audio('samples/gold/high/audio')

random_sampler = RandomVocalizationSampler(
    project,
    annotation_set = 'its',
    target_speaker_type = ['CHI'],
    sample_size = 250
)
random_sampler.sample()
os.makedirs('samples/gold/random', exist_ok = True)
random_sampler.segments[['recording_filename', 'segment_onset', 'segment_offset']].to_csv('samples/gold/random/samples.csv', index = False)
random_sampler.export_audio('samples/gold/random/audio')