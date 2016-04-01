"""ASV Benchmarks for loading things using Iris."""

import iris


class TimeMetricPPLoad:
    """
    Time loading things using Iris with ASV.

    """
    def setup(self):
        """Set stuff up."""
        self.dataset = '/data/local/dataZoo/PP/aPPglob1/global.pp'

    # Time benchmarks have the prefix "time_".
    def time_load_pp(self):
        iris.load(self.dataset)
