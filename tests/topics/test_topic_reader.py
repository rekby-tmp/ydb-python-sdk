import pytest


@pytest.mark.asyncio
class TestTopicWriterAsyncIO:
    async def test_read_message(
        self, driver, topic_path, topic_with_messages, topic_consumer
    ):
        reader = driver.topic_client.topic_reader(topic_consumer, topic_path)

        assert await reader.receive_batch() is not None

    async def test_read_and_commit_message(
            self, driver, topic_path, topic_with_messages, topic_consumer
    ):

        reader = driver.topic_client.topic_reader(topic_consumer, topic_path)
        batch = await reader.receive_batch()
        await reader.commit_with_ack(batch)

        reader = driver.topic_client.topic_reader(topic_consumer, topic_path)
        batch2 = await reader.receive_batch()
        assert batch.messages[0] != batch2.messages[0]
