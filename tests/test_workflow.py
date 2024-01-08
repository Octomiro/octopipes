from octopipes.workflow import Workflow


def test_workflow():
    wf = Workflow('test_wf_1')\
            .add(lambda x: x)\
            .add(lambda x: x)
    assert wf.nsteps == 2
    wf_iter = wf(1)
    for result in wf_iter:
        assert result == 1

    wf_iter.recap()
    wf_iter.freeze()
