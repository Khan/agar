import datetime

from agar.counter import WriteBehindCounter, TimedWriteBehindCounter, HourlyWriteBehindCounter, DailyWriteBehindCounter
from agar.test import BaseTest


class WriteBehindCounterTest(BaseTest):
    def setUp(self):
        super(WriteBehindCounterTest, self).setUp()
        self.now = datetime.datetime.now()

    def test_counter(self):
        self.assertEqual(WriteBehindCounter.get_value('test'), 0)
        self.assertEqual(WriteBehindCounter.get_value('test2'), 0)
        self.assertMemcacheItems(0)
        WriteBehindCounter.incr('test')
        self.assertMemcacheHits(0)
        self.assertTasksInQueue(1)
        self.assertEqual(WriteBehindCounter.get_value('test'), 1)
        self.assertEqual(WriteBehindCounter.get_value('test2'), 0)
        WriteBehindCounter.incr('test')
        self.assertMemcacheHits(1)
        self.assertTasksInQueue(1)
        self.assertEqual(WriteBehindCounter.get_value('test'), 2)
        self.assertEqual(WriteBehindCounter.get_value('test2'), 0)
        WriteBehindCounter.incr('test2')
        self.assertMemcacheHits(2)
        self.assertTasksInQueue(2)
        self.assertEqual(WriteBehindCounter.get_value('test2'), 1)
        self.assertEqual(WriteBehindCounter.get_value('test'), 2)

    def test_timed_counter(self):
        self.assertEqual(TimedWriteBehindCounter.get_value('test', self.now), 0)
        self.assertEqual(TimedWriteBehindCounter.get_value('test2', self.now), 0)
        self.assertMemcacheItems(0)
        self.assertEqual(TimedWriteBehindCounter.get_value('test', self.now), 0)
        TimedWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(0)
        self.assertTasksInQueue(1)
        self.assertEqual(TimedWriteBehindCounter.get_value('test', self.now), 1)
        self.assertEqual(TimedWriteBehindCounter.get_value('test2', self.now), 0)
        TimedWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(1)
        self.assertTasksInQueue(1)
        self.assertEqual(TimedWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(TimedWriteBehindCounter.get_value('test2', self.now), 0)
        TimedWriteBehindCounter.incr('test2', now=self.now)
        self.assertMemcacheHits(2)
        self.assertTasksInQueue(2)
        self.assertEqual(TimedWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(TimedWriteBehindCounter.get_value('test2', self.now), 1)

    def test_hourly_counter(self):
        self.assertEqual(HourlyWriteBehindCounter.get_value('test', self.now), 0)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test2', self.now), 0)
        self.assertMemcacheItems(0)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test', self.now), 0)
        HourlyWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(0)
        self.assertTasksInQueue(1)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test', self.now), 1)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test2', self.now), 0)
        HourlyWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(1)
        self.assertTasksInQueue(1)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test2', self.now), 0)
        HourlyWriteBehindCounter.incr('test2', now=self.now)
        self.assertMemcacheHits(2)
        self.assertTasksInQueue(2)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(HourlyWriteBehindCounter.get_value('test2', self.now), 1)

    def test_daily_counter(self):
        self.assertEqual(DailyWriteBehindCounter.get_value('test', self.now), 0)
        self.assertEqual(DailyWriteBehindCounter.get_value('test2', self.now), 0)
        self.assertMemcacheItems(0)
        self.assertEqual(DailyWriteBehindCounter.get_value('test', self.now), 0)
        DailyWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(0)
        self.assertTasksInQueue(1)
        self.assertEqual(DailyWriteBehindCounter.get_value('test', self.now), 1)
        self.assertEqual(DailyWriteBehindCounter.get_value('test2', self.now), 0)
        DailyWriteBehindCounter.incr('test', now=self.now)
        self.assertMemcacheHits(1)
        self.assertTasksInQueue(1)
        self.assertEqual(DailyWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(DailyWriteBehindCounter.get_value('test2', self.now), 0)
        DailyWriteBehindCounter.incr('test2', now=self.now)
        self.assertMemcacheHits(2)
        self.assertTasksInQueue(2)
        self.assertEqual(DailyWriteBehindCounter.get_value('test', self.now), 2)
        self.assertEqual(DailyWriteBehindCounter.get_value('test2', self.now), 1)