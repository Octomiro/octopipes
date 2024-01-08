import logging
from collections.abc import Callable
from typing import Protocol

from tqdm import tqdm

from octopipes.results import Results
from octopipes.workflow import Workflow

logger = logging.getLogger(__name__)

class AggregateFlows:
    """AggregateFlows enables running multiple workflows on the same input"""

    def __init__(self, input, workflows: list[Workflow]):
        self.input = input
        self.workflows = workflows
        self.results: list[Results] = []
        self._hooks = []

    def add_hook(self, hook: Callable):
        """Adds a hook for post-workflow callbacks"""
        self._hooks.append(hook)

    def add_hooks(self, hooks: list[Callable]):
        """Adds multiple hooks for post-workflow callbacks"""
        [self.add_hook(h) for h in hooks]

    def _run_hook(self, hook, workflow):
        hook(workflow)

    def run_hooks(self, workflow):
        for hook in self._hooks:
            self._run_hook(hook, workflow)

    def _run(self, workflow: Workflow) -> Results:
        wf_iter = workflow(self.input)
        for _ in tqdm(wf_iter, desc=f'{workflow.name} Steps', leave=False):
            pass

        result = wf_iter.freeze()
        self.results.append(result)

        # running hooks
        self.run_hooks(wf_iter)
        return result

    def run_workflows(self):
        for wf in tqdm(self.workflows, desc='workflows', leave=False):
            self._run(wf)


class AggregateFlowsFactory(Protocol):
    def get_aggregate_flows(self, input, workflows) -> AggregateFlows: # type: ignore
        pass

class DefaultAggregateFlowsFactory:
    def __init__(self, hooks: list[Callable]):
        self.hooks = hooks

    def get_aggregate_flows(self, input, workflows) -> AggregateFlows:
        aggr = AggregateFlows(input, workflows=workflows)
        aggr.add_hooks(self.hooks)
        return aggr
