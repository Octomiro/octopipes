from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from octopipes.dataset import Dataloader
from octopipes.workflow import Workflow
from octopipes.aggregate_flows import AggregateFlows, AggregateFlowsFactory, DefaultAggregateFlowsFactory


class Benchmark:
    def __init__(self, dataloader: Dataloader, workflows: list[Workflow],
                 flows_factory: AggregateFlowsFactory | None = None, mode: str = "threaded") -> None:

        """
        :param str mode: "single" for sequential execution, "threaded" for multithreading.
        """

        self.dataloader = dataloader
        self.workflows = workflows
        self.mode=mode
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
        if self.mode == "single":
            self._run_sequential()
        elif self.mode == "threaded":
            self._run_multithreaded()
        else:
            raise ValueError(f"Invalid model: {self.mode}. Choose 'single' or 'threaded' ")       
         

    def _run_sequential(self):
        """Runs workflows sequentially (single-threaded execution)."""
        for batch in tqdm(self.dataloader, desc= "processing batches"):
            for sample in batch:
                result=self.run_sample(self.factory, self.workflows, sample)
                self.results.append(result)

    def _run_multithreaded(self):
        """Runs workflows using multithreading (threaded execution)."""
        for batch_idx, batch in enumerate(tqdm(self.dataloader, desc="processing batches")):
            with ThreadPoolExecutor(max_workers=len(batch)) as executor:
                future_to_index = {
                    executor.submit(self.run_sample, self.factory, self.workflows, sample): (batch_idx, i)
                    for i, sample in enumerate(batch)
                }
                
                results_dict = {}  # Store results by batch index
                
                for future in as_completed(future_to_index):
                    try:
                        batch_idx, i = future_to_index[future]
                        result = future.result()
                        results_dict[(batch_idx, i)] = result
                    except Exception as e:
                        print(f"Error processing sample: {e}")

                # Append results in correct order
                for key in sorted(results_dict.keys()):
                    self.results.append(results_dict[key])
    

