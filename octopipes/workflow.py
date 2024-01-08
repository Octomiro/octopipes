import time
import logging
from typing import Any
from collections.abc import Callable

from octopipes.results import Results, Step
from octopipes.handlers import DefaultHandler, HandlerInterface


logger = logging.getLogger(__name__)


class Workflow:
    """Workflow allows the difinition of multiple processes/steps"""
    
    def __init__(self, name: str,
                 steps: list[tuple[Callable, HandlerInterface]] = list(),
                 metadata: dict = {}) -> None:
        self.name = name
        self.metadata = dict(metadata)
        
        try:
            processes, handlers = zip(*list(steps))
        except ValueError:
            processes, handlers = [], []

        self.processes: list[Callable] = list(processes)  # type: ignore
        self.handlers: list[HandlerInterface] = list(handlers)  # type: ignore

    @property
    def metadata_name(self):
        return f'{self.name}{"".join(f"({key}:{value})" for key, value in self.metadata)}'

    @property
    def nsteps(self):
        return len(self.processes)

    def __len__(self):
        return self.nsteps

    def add(self, process: Callable, handler: HandlerInterface = DefaultHandler()):
        self.processes.append(process)
        self.handlers.append(handler)
        return self

    def __call__(self, input: Any, *args: Any, **kwds: Any) -> 'WorkflowIter':
        return Workflow.WorkflowIter(self, input)

    class WorkflowIter:
        def __init__(self, workflow: 'Workflow', input) -> None:
            self.workflow = workflow
            self.input = input
            self.outputs = []
            self.durations : list[float] = []

        def __iter__(self):
            self.current_step = 0
            self.current_output = self.input
            return self

        def __next__(self):
            if self.current_step < self.workflow.nsteps:
                self.current_step += 1

                start = time.perf_counter()
                self.current_output = self.workflow.processes[self.current_step - 1](self.current_output)
                end = time.perf_counter()
                self.outputs.append(self.current_output)
                self.durations.append(end - start)
                return self.current_output
            raise StopIteration

        def recap(self, capture=False):
            output = ''
            for process, d in zip(self.workflow.processes, self.durations):
                output += f'{process.__name__} took {d:.4f}s'
            if capture:
                return output
            print(output)

        def steps_recap(self) -> tuple[Step, ...]:
            return tuple({'step': process.__name__, 'duration': d} for process, d in zip(self.workflow.processes, self.durations))

        @property
        def total_duration(self):
            return sum(self.durations)

        @property
        def final_output(self):
            return self.outputs[-1]

        def len_output(self):
            return len(self.current_output) if hasattr(self.current_output, '__len__') else None

        def freeze(self) -> Results:
            return Results(name=self.workflow.name,
                           metadata_name=self.workflow.metadata_name,
                           metadata=self.workflow.metadata,
                           nsteps=self.workflow.nsteps,
                           current_step=self.current_step,
                           output=self.current_output,
                           len_output=self.len_output(),
                           total_duration=self.total_duration,
                           output_recap=self.steps_recap())
