from octopipes.benchmark import Benchmark
from octopipes.dataset import Dataloader, Dataset, InputWithDeps
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


def test_benchmark_with_dependencies():
    wf1 = Workflow('test_wf_1')\
            .add(lambda x, y: x + y, requires='d0')

    wf2 = Workflow('test_wf_2')\
            .add(lambda x, y: x - y, requires='d0')

    # This dataset defines inputs with dependencies without ground truth
    dataset: Dataset = MockDataset([InputWithDeps(2, dependencies=[2]), InputWithDeps(1, dependencies=[2])])
    dataloader = Dataloader(dataset=dataset, batch_size=2, drop_last_batch=True)
    benchmark = Benchmark(dataloader=dataloader, workflows=[wf1, wf2])
    benchmark.run_tests()
    assert len(benchmark.results) == 2
    assert benchmark.results[0].results[0].output == 4
    assert benchmark.results[0].results[1].output == 0
    assert benchmark.results[1].results[0].output == 3
    assert benchmark.results[1].results[1].output == -1

    # this dataset defines inputs with dependencies with a ground truth value
    dataset: Dataset = MockDataset([
        (InputWithDeps(2, dependencies=[2]), 24),
        (InputWithDeps(1, dependencies=[2]), 24)
    ])
    dataloader = Dataloader(dataset=dataset, batch_size=2, drop_last_batch=True)
    benchmark = Benchmark(dataloader=dataloader, workflows=[wf1, wf2])
    benchmark.run_tests()
    assert len(benchmark.results) == 2
    assert benchmark.results[0].results[0].output == 4
    assert benchmark.results[0].results[1].output == 0
    assert benchmark.results[1].results[0].output == 3
    assert benchmark.results[1].results[1].output == -1
