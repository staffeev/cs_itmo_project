#!/usr/bin/env python3
# -*-coding:utf-8 -*
from mrjob.job import MRJob
from mrjob.job import MRStep
from datetime import datetime
import json


class Make(MRJob):
    def configure_args(self):
        super().configure_args()
        self.add_file_arg('--currencies')

    def mapper_init(self):
        if not getattr(self, "currencies", False):
            self.currencies=json.load(open(self.options.currencies))

    def mapper_hour(self, key, value):
        timestamp, region, currency, category, profit = value.split("\t")
        date = datetime.fromtimestamp(int(timestamp)).isoformat()[:13]
        yield (date, region, category), float(profit) * (1 / self.currencies[currency])

    def reducer_sum(self, key, values):
        yield key, sum(values)

    def steps(self):
        return [
            MRStep(
                mapper_init=self.mapper_init,
                mapper=self.mapper_hour,
                reducer=self.reducer_sum,
            )
        ]


if __name__ == '__main__':
    Make.run()
