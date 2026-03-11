import time
import logging
from typing import Any, Protocol, Tuple
from collections.abc import Callable
from dataclasses import dataclass

from octopipes.results import Results, Step
from octopipes.handlers import DefaultHandler, HandlerInterface
from octopipes import utils

logger = logging.getLogger(__name__)


@dataclass
class WorkflowInput:
    input: Any
    dependency: Any = None

class WorkflowStep(Protocol):
    def __call__(self, wi: WorkflowInput, /, *args: Any, **kwargs: Any) -> Tuple[Any, HandlerInterface]:
        ...

def workflow_step(fn: Callable) -> WorkflowStep:
    def inner(_: WorkflowInput, *args, **kwargs):
        output : Any = fn(*args, **kwargs)
        return (output, DefaultHandler(output=output))
    return inner

def wrap_default_handler(fn: Callable):
    def inner(*args, **kwargs):
        out = fn(*args, **kwargs)
        return (out, DefaultHandler(output=out))
    return inner

class Workflow:
    """Workflow allows the difinition of multiple processes/steps"""
    
    def __init__(self, name: str,
                 steps: list[Callable] = list(),
                 metadata: dict = {}) -> None:
        self.name = name
        self.metadata = dict(metadata)
        
        self.processes: list[Callable] = list(steps)

    @property
    def metadata_name(self):
        return f'{self.name}{"".join(f"({key}:{value})" for key, value in self.metadata)}'

    @property
    def nsteps(self):
        return len(self.processes)

    def __len__(self):
        return self.nsteps

    def add(self, process: WorkflowStep):
        """Adds a new process to the workflow.

        Parameters:
            process: the function/process to be added
            handler: Additional handler for the output of the process
        """
        self.processes.append(process)
        return self

    def __call__(self, input: Any, *args: Any, **kwds: Any) -> 'WorkflowIter':
        if not isinstance(input, WorkflowInput):
            input = WorkflowInput(input=input)

        return Workflow.WorkflowIter(self, input)

    class WorkflowIter:
        def __init__(self, workflow: 'Workflow', input: WorkflowInput) -> None:
            self.workflow = workflow
            self.input = input
            self.outputs = []
            self.handlers: list[HandlerInterface] = []
            self.durations : list[float] = []

        def __iter__(self):
            self.current_step = 0
            self.current_output = self.input.input
            self.current_handler = None
            return self

        def __next__(self):
            if self.current_step < self.workflow.nsteps:
                self.current_step += 1

                start = time.perf_counter()
                self.current_output, self.current_handler = self.workflow.processes[self.current_step - 1](
                    self.input, self.current_output
                )
                end = time.perf_counter()

                self.outputs.append(self.current_output)
                self.handlers.append(self.current_handler)
                self.durations.append(end - start)
                step_name = self.workflow.processes[self.current_step - 1].__name__

                return step_name, self.current_output

            raise StopIteration

        def recap(self, capture=False):
            output = ''
            for process, d in zip(self.workflow.processes, self.durations):
                output += f'{process.__name__} took {d:.4f}s'
            if capture:
                return output
            print(output)

        
        def viz(self, output=-1, save_to_file=True, path: str | None = None) -> None:
            import cv2

            handler = self.handlers[output]
            output = self.outputs[output]
            if output is None:
                return

            outputs = handler.viz()

            if save_to_file:
                for i, output in enumerate(outputs):
                    if path is not None:
                        utils.write_image(output, path + '/' + str(i))
                    else:
                        raise ValueError('save_to_file set but path is None')
            else:
                for output in outputs:
                    cv2.imshow(self.workflow.name, output)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        def json_output(self, output: int = -1) -> str:
            """Returns the json output of a step using the corresponding handler"""
            handler = self.handlers[output]

            return handler.to_json()

        def steps_recap(self) -> tuple[Step, ...]:
            return tuple({'step': process.__name__, 'duration': d} for process, d in zip(self.workflow.processes, self.durations))

        @property
        def total_duration(self):
            return sum(self.durations)

        @property
        def final_output(self):
            return self.outputs[-1]

        def size(self, output: int = -1) -> int | None:
            """Returns the length of the output of a step using the corresponding handler"""
            handler = self.handlers[output]

            return handler.size()

        def freeze(self) -> Results:
            return Results(name=self.workflow.name,
                           metadata_name=self.workflow.metadata_name,
                           metadata=self.workflow.metadata,
                           nsteps=self.workflow.nsteps,
                           current_step=self.current_step,
                           output=self.current_output,
                           len_output=self.size(),
                           total_duration=self.total_duration,
                           output_recap=self.steps_recap(),
                           json_output=self.json_output())
