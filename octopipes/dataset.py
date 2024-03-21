from dataclasses import dataclass
from typing import Protocol, Any


class Dataset(Protocol):
    def __getitem__(self, index) -> Any:
        pass

    def __len__(self) -> int:
        return 0


@dataclass
class Dataloader:
    dataset: Dataset
    batch_size: int = 1
    limit: int | None = None
    drop_last_batch: bool = False

    def __iter__(self):
        return iter(DataloaderIter(self))


class DataloaderIter:
    def __init__(self, dataloader) -> None:
        self.dataset = dataloader.dataset
        self.batch_size = dataloader.batch_size
        self.limit = dataloader.limit
        self.drop_last_batch = dataloader.drop_last_batch

        self.size = len(self.dataset)
        self.batches = self.size // self.batch_size
        self.total_yield = self.batch_size * self.batches
        if not dataloader.drop_last_batch:
            self.batches += 1 if self.size % self.batch_size != 0 else 0
            self.total_yield += self.size % self.batch_size
        if self.limit is not None:
            self.total_yield = self.limit

    def __iter__(self):
        self.current_index = 0
        self.total_yielded = 0
        return self

    def __next__(self):
        if self.total_yielded < self.total_yield:
            end = self.current_index + self.batch_size
            batch = self.dataset[self.current_index:end]
            if self.total_yielded + len(batch) > self.total_yield:
                batch = batch[:self.total_yield - self.total_yielded]
            self.current_index = end
            self.total_yielded += len(batch)
            return batch
        raise StopIteration


@dataclass
class InputWithDeps:
    input: Any
    dependencies: list
