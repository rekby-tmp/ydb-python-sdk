import asyncio
import bisect
import copy
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Type, TypeVar, Union

import pytest

from ydb._grpc.grpcwrapper.ydb_topic import OffsetsRange
from ydb._topic_reader.datatypes import PartitionSession


class TestPartitionSession:
    session_comitted_offset = 10

    @pytest.fixture
    def session(self) -> PartitionSession:
        return PartitionSession(
            id=1,
            state=PartitionSession.State.Active,
            topic_path="",
            partition_id=1,
            committed_offset=self.session_comitted_offset,
            reader_reconnector_id=1,
            reader_stream_id=1,
        )

    def test_add_commit(self, session):
        commit = OffsetsRange(self.session_comitted_offset, self.session_comitted_offset+5)
        waiter = session.add_commit(commit)
        assert waiter.end_offset == commit.end

    @pytest.mark.parametrize(
        "original,add,result",
        [
            (
                    [],
                    OffsetsRange(1, 10),
                    [OffsetsRange(1, 10)],
            ),
            (
                [OffsetsRange(1, 10)],
                OffsetsRange(15, 20),
                [OffsetsRange(1, 10), OffsetsRange(15, 20)],
            ),
            (
                [OffsetsRange(15, 20)],
                OffsetsRange(1, 10),
                [OffsetsRange(1, 10), OffsetsRange(15, 20)],
            ),
            (
                [OffsetsRange(1, 10)],
                OffsetsRange(10, 20),
                [OffsetsRange(1, 20)],
            ),
            (
                [OffsetsRange(10, 20)],
                OffsetsRange(1, 10),
                [OffsetsRange(1, 20)],
            ),
            (
                [OffsetsRange(1, 2), OffsetsRange(3, 4)],
                OffsetsRange(2, 3),
                [OffsetsRange(1, 2), OffsetsRange(2, 4)],
            ),
            (
                [OffsetsRange(1, 10)],
                OffsetsRange(5, 6),
                ValueError,
            ),
        ]
    )
    def test_add_to_commits(self,
                        session,
                        original: List[OffsetsRange],
                        add: OffsetsRange,
                        result: Union[List[OffsetsRange], Type[Exception]],
                        ):
        session._commits = copy.deepcopy(original)
        if isinstance(result, type) and issubclass(result, Exception):
            with pytest.raises(result):
                session._add_to_commits(add)
        else:
            session._add_to_commits(add)
            assert session._commits == result

    # noinspection PyTypeChecker
    @pytest.mark.parametrize(
        "original,add,result",
        [
            (
                [],
                5,
                [PartitionSession.CommitAckWaiter(5, None)],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None)],
                6,
                [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(6, None)],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None)],
                4,
                [PartitionSession.CommitAckWaiter(4, None), PartitionSession.CommitAckWaiter(5, None)],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None)],
                0,
                [PartitionSession.CommitAckWaiter(0, None), PartitionSession.CommitAckWaiter(5, None)],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None)],
                100,
                [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(100, None)],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(100, None)],
                50,
                [
                    PartitionSession.CommitAckWaiter(5, None),
                    PartitionSession.CommitAckWaiter(50, None),
                    PartitionSession.CommitAckWaiter(100, None),
                ],
            ),
            (
                [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(7, None)],
                6,
                [
                    PartitionSession.CommitAckWaiter(5, None),
                    PartitionSession.CommitAckWaiter(6, None),
                    PartitionSession.CommitAckWaiter(7, None),
                ],
            ),
            (
                    [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(100, None)],
                    6,
                    [
                        PartitionSession.CommitAckWaiter(5, None),
                        PartitionSession.CommitAckWaiter(6, None),
                        PartitionSession.CommitAckWaiter(100, None),
                    ],
            ),
            (
                    [PartitionSession.CommitAckWaiter(5, None), PartitionSession.CommitAckWaiter(100, None)],
                    99,
                    [
                        PartitionSession.CommitAckWaiter(5, None),
                        PartitionSession.CommitAckWaiter(99, None),
                        PartitionSession.CommitAckWaiter(100, None),
                    ],
            ),
        ]
    )
    def test_add_waiter(self,
                        session,
                        original: List[PartitionSession.CommitAckWaiter],
                        add: int,
                        result: List[PartitionSession.CommitAckWaiter],
                        ):
        session._ack_waiters = copy.deepcopy(original)
        res = session._add_waiter(add)
        assert result == session._ack_waiters

        index = bisect.bisect_left(session._ack_waiters, res)
        assert res is session._ack_waiters[index]

    @pytest.mark.parametrize(
        "commits,result,rest",
        [
            (
                [],
                None,
                []
            ),
            (
                [OffsetsRange(session_comitted_offset+1, 20)],
                None,
                [OffsetsRange(session_comitted_offset+1, 20)],
            ),
            (
                [OffsetsRange(session_comitted_offset, session_comitted_offset+1)],
                OffsetsRange(session_comitted_offset, session_comitted_offset+1),
                [],
            ),
            (
                [
                    OffsetsRange(session_comitted_offset, session_comitted_offset+1),
                    OffsetsRange(session_comitted_offset+1, session_comitted_offset+2),
                ],
                OffsetsRange(session_comitted_offset, session_comitted_offset+2),
                [],
            ),
            (
                [
                    OffsetsRange(session_comitted_offset, session_comitted_offset+1),
                    OffsetsRange(session_comitted_offset+1, session_comitted_offset+2),
                    OffsetsRange(session_comitted_offset+10, session_comitted_offset+20),
                ],
                OffsetsRange(session_comitted_offset, session_comitted_offset+2),
                [OffsetsRange(session_comitted_offset+10, session_comitted_offset+20)],
            ),
        ]
    )
    def test_get_commit_range(self,
                              session,
                              commits: List[OffsetsRange],
                              result: Optional[OffsetsRange],
                              rest: List[OffsetsRange],
                              ):
        send_commit_window_start = session._send_commit_window_start

        session._commits = deque(commits)
        res = session.pop_commit_range()
        assert res == result
        assert session._commits == deque(rest)

        if res is None:
            assert session._send_commit_window_start == send_commit_window_start
        else:
            assert session._send_commit_window_start != send_commit_window_start
            assert session._send_commit_window_start == res.end

