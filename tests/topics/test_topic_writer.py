import pytest

import ydb.aio


@pytest.mark.asyncio
class TestTopicWriterAsyncIO:
    async def test_send_message(self, driver: ydb.aio.Driver, topic_path):
        writer = driver.topic_client.topic_writer(
            topic_path, producer_and_message_group_id="test"
        )
        await writer.write(ydb.TopicWriterMessage(data="123".encode()))
        await writer.close()

    async def test_wait_last_seqno(self, driver: ydb.aio.Driver, topic_path):
        async with driver.topic_client.topic_writer(
            topic_path,
            producer_and_message_group_id="test",
            auto_seqno=False,
        ) as writer:
            await writer.write_with_ack_future(
                ydb.TopicWriterMessage(data="123".encode(), seqno=5)
            )

        async with driver.topic_client.topic_writer(
            topic_path,
            producer_and_message_group_id="test",
            get_last_seqno=True,
        ) as writer2:
            init_info = await writer2.wait_init()
            assert init_info.last_seqno == 5

    async def test_auto_flush_on_close(self, driver: ydb.aio.Driver, topic_path):
        async with driver.topic_client.topic_writer(
            topic_path,
            producer_and_message_group_id="test",
            auto_seqno=False,
        ) as writer:
            last_seqno = 0
            for i in range(10):
                last_seqno = i + 1
                await writer.write(
                    ydb.TopicWriterMessage(data=f"msg-{i}", seqno=last_seqno)
                )

        async with driver.topic_client.topic_writer(
            topic_path,
            producer_and_message_group_id="test",
            get_last_seqno=True,
        ) as writer:
            init_info = await writer.wait_init()
            assert init_info.last_seqno == last_seqno
