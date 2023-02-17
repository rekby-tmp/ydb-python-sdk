from __future__ import annotations

import abc
import asyncio
import bisect
import enum
from collections import deque
from dataclasses import dataclass, field
import datetime
from typing import Mapping, Union, Any, List, Dict, Deque, Optional, NamedTuple

from ydb._grpc.grpcwrapper.ydb_topic import OffsetsRange


class ICommittable(abc.ABC):
    @abc.abstractmethod
    def _commit_get_partition_session(self) -> PartitionSession:
        ...

    @abc.abstractmethod
    def _commit_get_offsets_range(self) -> OffsetsRange:
        ...


class ISessionAlive(abc.ABC):
    @property
    @abc.abstractmethod
    def is_alive(self) -> bool:
        pass


@dataclass
class PublicMessage(ICommittable, ISessionAlive):
    seqno: int
    created_at: datetime.datetime
    message_group_id: str
    session_metadata: Dict[str, str]
    offset: int
    written_at: datetime.datetime
    producer_id: str
    data: Union[
        bytes, Any
    ]  # set as original decompressed bytes or deserialized object if deserializer set in reader
    _partition_session: PartitionSession
    _commit_start_offset: int
    _commit_end_offset: int

    def _commit_get_partition_session(self) -> PartitionSession:
        return self._partition_session

    def _commit_get_offsets_range(self) -> OffsetsRange:
        return OffsetsRange(self._commit_start_offset, self._commit_end_offset)

    # ISessionAlive implementation
    @property
    def is_alive(self) -> bool:
        raise NotImplementedError()


@dataclass
class PartitionSession:
    id: int
    state: "PartitionSession.State"
    topic_path: str
    partition_id: int
    committed_offset: int  # last commit offset, acked from server. Processed messages up to the field-1 offset.
    reader_reconnector_id: int
    reader_stream_id: int
    _next_message_start_commit_offset: int = field(init=False)
    _send_commit_window_start: int = field(init=False)
    _commits: Deque[OffsetsRange] = field(init=False, default_factory=lambda: deque())
    _ack_waiters: Deque["PartitionSession.CommitAckWaiter"] = field(init=False, default_factory=lambda: deque())
    _loop: Optional[asyncio.AbstractEventLoop] = field(init=False)  # may be None in tests

    def __post_init__(self):
        self._next_message_start_commit_offset = self.committed_offset
        self._send_commit_window_start = self.committed_offset

        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = None

    def stop(self):
        self.state = PartitionSession.State.Stopped

    def add_commit(self, new_commit: OffsetsRange) -> "PartitionSession.CommitAckWaiter":
        self._add_to_commits(new_commit)
        return self._add_waiter(new_commit.end)

    def _add_to_commits(self, new_commit: OffsetsRange):
        index = bisect.bisect_left(self._commits, new_commit)

        prev_commit = self._commits[index - 1] if index > 0 else None
        commit = self._commits[index] if index < len(self._commits) else None

        for c in (prev_commit, commit):
            if c is not None and new_commit.is_intersected_with(c):
                raise ValueError("new commit intersected with existed. New range: %s, existed: %s" % (new_commit, c))

        if commit is not None and commit.start == new_commit.end:
            commit.start = new_commit.start
        elif prev_commit is not None and prev_commit.end == new_commit.start:
            prev_commit.end = new_commit.end
        else:
            self._commits.insert(index, new_commit)

    def _add_waiter(self, end_offset: int) -> "PartitionSession.CommitAckWaiter":
        waiter = PartitionSession.CommitAckWaiter(end_offset, self._create_future())
        bisect.insort(self._ack_waiters, waiter)
        return waiter

    def _create_future(self) -> asyncio.Future:
        if self._loop:
            return self._loop.create_future()
        else:
            return asyncio.Future()

    def pop_commit_range(self) -> Optional[OffsetsRange]:
        if len(self._commits) == 0:
            return None

        if self._commits[0].start != self._send_commit_window_start:
            return None

        res = self._commits.popleft()
        while len(self._commits) > 0 and self._commits[0].start == res.end:
            commit = self._commits.popleft()
            res.end = commit.end

        self._send_commit_window_start = res.end

        return res

    class State(enum.Enum):
        Active = 1
        GracefulShutdown = 2
        Stopped = 3

    @dataclass(order=True)
    class CommitAckWaiter:
        end_offset: int
        future: asyncio.Future = field(compare=False)


@dataclass
class PublicBatch(ICommittable, ISessionAlive):
    session_metadata: Mapping[str, str]
    messages: List[PublicMessage]
    _partition_session: PartitionSession
    _bytes_size: int

    def _commit_get_partition_session(self) -> PartitionSession:
        return self.messages[0]._commit_get_partition_session()

    def _commit_get_offsets_range(self) -> OffsetsRange:
        return OffsetsRange(
            self.messages[0]._commit_get_offsets_range().start,
            self.messages[-1]._commit_get_offsets_range().end,
        )

    # ISessionAlive implementation
    @property
    def is_alive(self) -> bool:
        state = self._partition_session.state
        return (
                state == PartitionSession.State.Active
                or state == PartitionSession.State.GracefulShutdown
        )
