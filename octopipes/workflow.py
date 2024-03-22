import time
import logging
from typing import Any
from collections.abc import Callable

from octopipes.results import Results, Step
from octopipes.handlers import DefaultHandler, HandlerInterface
from octopipes import utils


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
        self.requires: list[str | None] = []

    @property
    def metadata_name(self):
        return f'{self.name}{"".join(f"({key}:{value})" for key, value in self.metadata)}'

    @property
    def nsteps(self):
        return len(self.processes)

    def __len__(self):
        return self.nsteps

    def add(self, process: Callable, handler: HandlerInterface = DefaultHandler(), requires: str | None = None):
        """Adds a new process to the workflow.

        Parameters:
            process: the function/process to be added
            handler: Additional handler for the output of the process
            requires: Set additional inputs required other than the strictly previous one.
                        The requires string should be in this form '0,1,2' where the numbers are the output of the process to inject.
        """
        self.processes.append(process)
        self.handlers.append(handler)
        self.requires.append(requires)
        return self

    def __call__(self, input: Any, dependencies: list | None = None, *args: Any, **kwds: Any) -> 'WorkflowIter':
        return Workflow.WorkflowIter(self, input, dependencies=dependencies)

    class WorkflowIter:
        def __init__(self, workflow: 'Workflow', input, dependencies: list | None = None) -> None:
            self.workflow = workflow
            self.input = input
            self.outputs = []
            self.dependencies = list(dependencies) if dependencies else []
            self.durations : list[float] = []

        def __iter__(self):
            self.current_step = 0
            self.current_output = self.input
            self.outputs.append(self.current_output)
            return self

        def __next__(self):
            if self.current_step < self.workflow.nsteps:
                self.current_step += 1

                start = time.perf_counter()
                if (requires := self.workflow.requires[self.current_step - 1]) is not None:
                    injected_inputs = self._parse_requires(requires)
                    input = [self.current_output] + injected_inputs

                    self.current_output = self.workflow.processes[self.current_step - 1](*input)
                else:
                    self.current_output = self.workflow.processes[self.current_step - 1](self.current_output)

                end = time.perf_counter()
                self.outputs.append(self.current_output)
                self.durations.append(end - start)
                step_name = self.workflow.processes[self.current_step - 1].__name__

                return step_name, self.current_output

            raise StopIteration

        def _parse_requires(self, requires: str) -> list[Any]:
            # get the outputs that need to be injected.
            # if the previous step is in the requires string, it should ignored (as it injected automatically).
            input = []
            for step in requires.split(','):
                if step.startswith('d'):
                    step = step[1:]
                    try:
                        input.append(self.dependencies[int(step)])
                    except Exception as e:
                        logger.error(f'encountered an error while parsing requires string {requires!r} due to {e}')
                else:
                    try:
                        output = int(step)
                        if output != self.current_step - 1:
                            input.append(self.outputs[output])
                    except Exception as e:
                        logger.error(f'encountered an error while parsing requires string {requires!r} due to {e}')

            return input

        def recap(self, capture=False):
            output = ''
            for process, d in zip(self.workflow.processes, self.durations):
                output += f'{process.__name__} took {d:.4f}s'
            if capture:
                return output
            print(output)

        
        def output_on_image(self, image, output=-1, save_to_file=True, path: str | None = None) -> None:
            import cv2

            handler = self.workflow.handlers[output]
            output = self.outputs[output]
            if output is None:
                return

            img = image.copy()
            img : Any = handler.output_on_image(img, output)

            if save_to_file:
                if path is not None:
                    utils.write_image(img, path)
                else:
                    raise ValueError('save_to_file set but path is None')

            else:
                cv2.imshow(self.workflow.name, img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

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
