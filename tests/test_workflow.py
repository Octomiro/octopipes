from dataclasses import dataclass
from octopipes.handlers import DefaultHandler
from octopipes.workflow import Workflow, WorkflowInput, workflow_step


def test_workflow():
    wf = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x))\
            .add(workflow_step(lambda x: x))
    assert wf.nsteps == 2
    wf_iter = wf(1)
    for _, result in wf_iter:
        assert result == 1

    wf_iter.recap()
    wf_iter.freeze()


def test_process_requires():
    wf = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x + 1))\
            .add(workflow_step(lambda x, y: x - y))

    wf_iter = wf(1)
    for _ in wf_iter:
        pass
    
    assert wf_iter.outputs[-1] == 1
        

    wf = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x + 'step1'))\
            .add(workflow_step(lambda x: x + 'step2'))\
            .add(workflow_step(lambda x, y, z: x + y + z))

    wf_iter = wf('input')
    for _ in wf_iter:
        pass
    
    assert wf_iter.outputs[-1] == 'inputstep1step2inputinputstep1'

def test_process_dependencies():
    wf = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x + 1))\
            .add(lambda x, y: (x.dep, DefaultHandler(output=x.dep)))

    @dataclass
    class Input(WorkflowInput):
        dep: str

    wf_iter = wf(Input(input='w1', dep='some_dep'))
    for _ in wf_iter:
        pass
    
    assert wf_iter.outputs[-1] == 'some_dep'

def test_process_requires_with_dependencies():
    """Test requires flags when previous outputs and dependencies are injected"""
    wf = Workflow('test_wf_1')\
            .add(workflow_step(lambda x: x[0]))\
            .add(lambda x, y: (y + x.input + x.dep, DefaultHandler(output=y + x.input + x.dep)))

    @dataclass
    class Input(WorkflowInput):
        dep: str

    wf_iter = wf(Input(input='input', dep='some_dep'))
    for _ in wf_iter:
        pass
    
    assert wf_iter.outputs[-1] == 'i' + 'input' + 'some_dep'
