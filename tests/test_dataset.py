import pytest

from octopipes.dataset import Dataloader, Dataset

class MockDataset:
    def __init__(self, values):
        self.l = values

    def __len__(self):
        return len(self.l)

    def __getitem__(self, index):
        return self.l[index]


def test_dataset():
    dataset: Dataset = MockDataset([])
    assert len(dataset) == 0

    dataset: Dataset = MockDataset([1, 2, 3, 4, 5])
    assert len(dataset) == 5
    assert dataset[0] == 1
    assert dataset[4] == 5

    dataset: Dataset = MockDataset([([1, 2, 3], 1)])
    assert len(dataset) == 1
    assert dataset[0] == ([1, 2, 3], 1)

    dataset: Dataset = MockDataset([([1, 2, 3], 1), ([4, 5, 6], 2)])
    assert dataset[1][1] == 2


def test_dataloader():
    dataset: Dataset = MockDataset([])
    dataloader = Dataloader(dataset=dataset,
                            batch_size=1,
                            limit=1)
    batch_iter = iter(dataloader)
    assert next(batch_iter) == []

    dataset: Dataset = MockDataset([1, 2, 3, 4, 5])
    dataloader = Dataloader(dataset=dataset,
                            batch_size=2)
    batch_iter = iter(dataloader)
    assert next(batch_iter) == [1, 2]
    assert next(batch_iter) == [3, 4]
    assert next(batch_iter) == [5]
    with pytest.raises(StopIteration):
        next(batch_iter)

    # Test when limit = batch_size
    dataloader = Dataloader(dataset=dataset,
                            batch_size=3,
                            limit=3)
    batch_iter = iter(dataloader)
    assert next(batch_iter) == [1, 2, 3]
    with pytest.raises(StopIteration):
        next(batch_iter)

    # Test when batch_size > limit
    dataloader = Dataloader(dataset=dataset,
                            batch_size=3,
                            limit=2)
    batch_iter = iter(dataloader)
    assert next(batch_iter) == [1, 2]
    with pytest.raises(StopIteration):
        next(batch_iter)

    # Test when limit > batch_size
    dataloader = Dataloader(dataset=dataset,
                            batch_size=3,
                            limit=4)
    batch_iter = iter(dataloader)
    assert next(batch_iter) == [1, 2, 3]
    assert next(batch_iter) == [4]
    with pytest.raises(StopIteration):
        next(batch_iter)
