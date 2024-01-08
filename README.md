<img src="octopipes-logo.png" width="500"/>

# Octopipes
*Octopipes* is a pipeline library for AI workflows. Not only it allows
for easy definition of multi-step workflows, but also handles testing
and collection of information of multiple workflows.

## Introduction
When using multiple-step (AI) pipelines, **octopipes** helps you define
workflows and work with workflows in an easy way. It allows for instance, adding post-workflow
hooks that can clean up GPU memory (or anything else).

Workflows are defined through the `Workflow` class, each worklfow can contain a chain of `processes` (some common ones are already defined).
Every step of the pipeline is saved and can be used later. For easier managements of different outputs, we can provide an output handler for each 
specific step (Some basic ones are already defined as well such `BboxesHandler` etc.).

To run multiple worklfows on the same input, you can use the `AggregateFlows` class for that. The library also provides a way to read datasets
and run benchmarks 

To keep `octopipes` ML library agnostic, it does not require `pytorch` or `tensorflow` to be installed
as it can work with both just fine.

## Examples
### Workflows
This shows how to define a simple workflow:
```python
from octopipes.workflow import Workflow

# Define a workflow with a single step
wf = Workflow('wf_name').add(lambda x: x ** 2)
print(wf.nsteps)
# output: 1
wf_iter = wf(1)
for result in wf_iter:
    pass

# return a frozen instance of the workflow run.
# This is especially important, when working with memory intensive GPU workflows
frozen_res = wf_iter.freeze()

# Get the duration recap of each step of the worklfow
wf_iter.recap()

# Define a workflow with some metadata attached
# this metadata can then be used to differentiate
# workflows with the same name but different params
wf = Workflow('wf_name', metadata={'thresh': 0.4}).add(lambda x: x ** 2)
```

### Output handlers
When adding a new step that outputs a certain results that you want to be processed in a perticular way, you can pass a class that
implements the `OutputHandler` interface.

The interface has 3 methods:
* **output_on_image**: used when outputing the results on an image (Used in computer vision mostly)
* **len_output**: give the output size of the result
* **to_json**: returns a serialized json object of the result

The library already provides some basic ones such as:
* BboxesHandler
* SegmentationMaskHandler
* CmapBboxesHandler
* CirclesHandler

Handlers are added this way. If None were supplied, `DefaultHandler` is used. *(In most cases a handler needs to be passed)*
```python
wf = Workflow('wf_name').add(some_func, some_handler)
```
