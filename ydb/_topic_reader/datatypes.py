from __future__ import annotations

import abc
import enum
from collections import deque
from dataclasses import dataclass, field
import datetime
from typing import Mapping, Union, Any, List, Dict, Deque, Optional

from ydb._grpc.grpcwrapper.ydb_topic import OffsetsRange
from . import topic_reader_asyncio


class ICommittable(abc.ABC):
    @abc.abstractmethod
    def _commit_get_partition_session(self) -> PartitionSession:
        ...

    @abc.abstractmethod
    def _commit_get_start_offset(self) -> int:
        ...

    @abc.abstractmethod
    def _commit_get_end_offset(self) -> int:
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

    @property
    def _commit_get_start_offset(self) -> int:
        return self._commit_start_offset

    @property
    def _commit_get_end_offset(self) -> int:
        return self._commit_end_offset

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
    next_message_start_commit_offset: int = field(init=False)
    send_commit_window_start: int = field(init=False)
    commits: Deque[OffsetsRange] = field(init=False, default_factory=lambda: deque())

    def __post_init__(self):
        self.next_message_start_commit_offset = self.committed_offset
        self.send_commit_window_start = self.committed_offset

    def stop(self):
        self.state = PartitionSession.State.Stopped

    def add_commit(self, new_commit: OffsetsRange):
        for commit in self.commits:
            if commit.is_intersected_with(new_commit):
                raise ValueError("the range")

        for index, commit in enumerate(self.commits):
            if new_commit.start == commit.end:
                commit.end = new_commit.end
                return
            if new_commit.end == commit.start:
                commit.start = new_commit.start
                return
            if new_commit.start < commit.start:
                self.commits.insert(index, new_commit)
                return

        self.commits.append(new_commit)

    def pop_commit_range(self) -> Optional[OffsetsRange]:
        if len(self.commits) == 0:
            return None

        if self.commits[0].start != self.send_commit_window_start:
            return None

        res = self.commits.popleft()
        while len(self.commits) > 0 and self.commits[0].start == res.end:
            commit = self.commits.popleft()
            res.end = commit.end

        self.send_commit_window_start = res.end

        return res

    class State(enum.Enum):
        Active = 1
        GracefulShutdown = 2
        Stopped = 3


@dataclass
class PublicBatch(ICommittable, ISessionAlive):
    session_metadata: Mapping[str, str]
    messages: List[PublicMessage]
    _partition_session: PartitionSession
    _bytes_size: int

    def _commit_get_partition_session(self) -> PartitionSession:
        return self.messages[0]._commit_get_partition_session()

    def _commit_get_start_offset(self) -> int:
        return self.messages[0]._commit_get_start_offset()

    def _commit_get_end_offset(self) -> int:
        return self.messages[-1]._commit_get_end_offset()

    # ISessionAlive implementation
    @property
    def is_alive(self) -> bool:
        state = self._partition_session.state
        return (
            state == PartitionSession.State.Active
            or state == PartitionSession.State.GracefulShutdown
        )
