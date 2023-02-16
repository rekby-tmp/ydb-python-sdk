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
                [OffsetsRange(1, 3), OffsetsRange(3, 4)],
            ),
            (
                [OffsetsRange(1, 10)],
                OffsetsRange(5, 6),
                ValueError,
            ),
        ]
    )
    def test_add_commit(self,
                        session,
                        original: List[OffsetsRange],
                        add: OffsetsRange,
                        result: Union[List[OffsetsRange], Type[Exception]],
                        ):
        session.commits = original
        if isinstance(result, type) and issubclass(result, Exception):
            with pytest.raises(result):
                session.add_commit(add)
        else:
            session.add_commit(add)
            assert session.commits == result

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
        send_commit_window_start = session.send_commit_window_start

        session.commits = deque(commits)
        res = session.pop_commit_range()
        assert res == result
        assert session.commits == deque(rest)

        if res is None:
            assert session.send_commit_window_start == send_commit_window_start
        else:
            assert session.send_commit_window_start != send_commit_window_start
            assert session.send_commit_window_start == res.end

