from multiprocess import Pool

from tqdm import tqdm

from octopipes.dataset import Dataloader
from octopipes.workflow import Workflow
from octopipes.aggregate_flows import AggregateFlows, AggregateFlowsFactory, DefaultAggregateFlowsFactory


class Benchmark:
    def __init__(self, dataloader: Dataloader, workflows: list[Workflow],
                 flows_factory: AggregateFlowsFactory | None = None) -> None:
        self.dataloader = dataloader
        self.workflows = workflows
        self.results: list[AggregateFlows] = []

        self.factory: AggregateFlowsFactory = DefaultAggregateFlowsFactory(hooks=[]) if flows_factory is None else flows_factory

    @staticmethod
    def run_sample(factory: AggregateFlowsFactory, workflows, sample):
        try:
            feature, _ = sample
        except TypeError:
            feature = sample

        aggregate = factory.get_aggregate_flows(feature, workflows)
        aggregate.run_workflows()
        return aggregate

    def run_tests(self):
        for batch in tqdm(self.dataloader):
            with Pool(processes=len(batch)) as pool:
                for result in pool.map(func=Run(self.factory, self.workflows), iterable=batch):
                    self.results.append(result)


class Run:
    def __init__(self, factory, workflows) -> None:
        self.factory = factory
        self.workflows = workflows

    def __call__(self, sample):
        return Benchmark.run_sample(self.factory, self.workflows, sample)
