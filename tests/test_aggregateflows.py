from octopipes.aggregate_flows import AggregateFlows
from octopipes.workflow import Workflow


def test_aggregateflows():
    wf1 = Workflow('test_wf_1')\
            .add(lambda x: x + 1)
    wf2 = Workflow('test_wf_2')\
            .add(lambda x: x * 2)
    flows = AggregateFlows(2, workflows=[wf1, wf2])
    flows.run_workflows()

    assert len(flows.results) == 2
    assert flows.results[0].output == 3
    assert flows.results[1].output == 4


def test_aggregateflows_with_dependencies():
    wf1 = Workflow('test_wf_1')\
            .add(lambda x, y: x + y, requires='d0')

    wf2 = Workflow('test_wf_2')\
            .add(lambda x, y: x - y, requires='d0')

    flows = AggregateFlows(2, dependencies=[2], workflows=[wf1, wf2])
    flows.run_workflows()

    assert len(flows.results) == 2
    assert flows.results[0].output == 4
    assert flows.results[1].output == 0

