from octopipes.benchmark import Benchmark
from octopipes.dataset import Dataloader, Dataset
from octopipes.workflow import Workflow

from tests.test_dataset import MockDataset


def test_benchmark():
    wf1 = Workflow('test_wf_1')\
            .add(lambda x: x + 1)
    wf2 = Workflow('test_wf_2')\
            .add(lambda x: x * 2)
    dataset: Dataset = MockDataset([1, 2, 3, 4, 5])
    dataloader = Dataloader(dataset=dataset, batch_size=2, drop_last_batch=True)
    benchmark = Benchmark(dataloader=dataloader, workflows=[wf1, wf2])
    benchmark.run_tests()
    assert len(benchmark.results) == 4
    assert benchmark.results[0].results[0].output == 2
    assert benchmark.results[0].results[1].output == 2
    assert benchmark.results[1].results[0].output == 3
    assert benchmark.results[1].results[1].output == 4
