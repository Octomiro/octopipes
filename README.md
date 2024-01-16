<img src="octopipes-logo.png" width="500"/>

# Octopipes
*Octopipes* is a pipeline library for AI workflows. Not only it allows
for easy definition of multi-step pipelines, but also handles testing
and collection of information of multiple workflows.

```bash
pip install octopipes
```

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

## Get started
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

### AggregateFlows
`AggregateFlows` allows running **multiple** workflows on the same input. This is usually used when either benchmarking multiple
pipelines at the same time or wanting to select the "best" output out of different workflows.

```python
from octopipes.workflow import Workflow
from octopipes.aggreage_flows import AggregateFlows

wf1 = Workflow('wf_name').add(some_func, some_handler)
wf2 = Workflow('wf_name').add(some_func, some_handler)

flows = AggregateFlows(input, workflows=[wf1, wf2])
flows.run_workflows()

# get results for wf1
flows.results[0]
```

### Benchmark
As the name suggest, `Benchmark` allows testing your workflows on a dataset and then being able to calculate easily your metrics.
Depending on the batch size of the dataset loader, the tests will be run simultaniously (as many processes as the batch size). Take note
however that as of now, a single `AggregateFlow` is run synchronously.

If you're using `pytorch` or `tensorflow`, some memory freeing hooks might be needed. For that, you can pass an instance of
`DefaultAggregateFlowsFactory` with the specific hooks needed. Otherwise, you can always define implement your own `AggregateFlowsFactory`.

Here's a simple example:
```python
from octopipes.workflow import Workflow
from octopipes.benchmark import Benchmark

dataloader = ...

wf1 = Workflow('wf1_name').add(some_func, some_handler)
wf2 = Workflow('wf2_name').add(some_func, some_handler)

bench = Benchmark(dataloader=dataloader, workflows=[wf1, wf2])
bench.run_tests()
```

## Requirements & Installation
The module is tested against versions `>=3.10`. However, this requirement is due to using type hinting so the module can be
altered to work on lower version of the interpreter.

Installing the package is pretty standard:
```sh
git clone https://github.com/octomiro/octopipes

pip install -r requirements.txt
# or requirements.in

pip install -r dev-requirements.in

# Running tests
pytest
# or
tox
```
## Contributions 
PRs are more than welcome! If the change is big enough to require some discussion, it's better to open an issue for it.
To keep the history of the repo clean, all PRs are rebased instead of merged so make sure everything is correct be submitting anything.

## Why Octopipes?
This library was born from a need to define, benchmark, and debug in an easy way workflows that use foundational models. In the course of
our work, we did not find something that met that need in terms of flexibility or features. So we created octopipes internaly, and decided
to open source it.

Octopipes is developed and mainted by [octomiro](https://octomiro.ai), an AI company that makes ERP systems intelligent.


