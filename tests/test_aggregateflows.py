from octopipes.aggregate_flows import AggregateFlows
from octopipes.workflow import Workflow, WorkflowInput, workflow_step, wrap_default_handler


def test_aggregateflows():
    wf1 = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x + 1))
    wf2 = Workflow('test_wf_2')\
            .add(workflow_step(lambda x: x * 2))
    flows = AggregateFlows(2, workflows=[wf1, wf2])
    flows.run_workflows()

    assert len(flows.results) == 2
    assert flows.results[0].output == 3
    assert flows.results[1].output == 4


def test_aggregateflows_with_dependencies():
    wf1 = Workflow('test_wf_1')\
            .add(wrap_default_handler(lambda wi, x: wi.dependency + x))

    wf2 = Workflow('test_wf_2')\
            .add(wrap_default_handler(lambda wi, x: wi.dependency - x))

    flows = AggregateFlows(WorkflowInput(2, dependency=2), workflows=[wf1, wf2])
    flows.run_workflows()

    assert len(flows.results) == 2
    assert flows.results[0].output == 4
    assert flows.results[1].output == 0

