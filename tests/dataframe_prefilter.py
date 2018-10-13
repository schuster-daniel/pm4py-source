from tests.constants import INPUT_DATA_DIR
from pm4py.objects.log.adapters.pandas import csv_import_adapter as csv_import_adapter
from pm4py.objects.log.importer.csv.versions import pandas_df_imp
from pm4py.algo.filtering.pandas.auto_filter import auto_filter
from pm4py.algo.filtering.pandas.attributes import attributes_filter
from pm4py.algo.filtering.pandas.cases import case_filter
from pm4py.algo.filtering.pandas.variants import variants_filter
from pm4py.statistics.traces.pandas import case_statistics
from pm4py.objects.log import transform
from pm4py.algo.filtering.pandas.paths import paths_filter
from pm4py.algo.filtering.pandas.timestamp import timestamp_filter
import unittest
import os

class DataframePrefilteringTest(unittest.TestCase):
    def test_prefiltering_dataframe(self):
        input_log = os.path.join(INPUT_DATA_DIR, "running-example.csv")
        dataframe = csv_import_adapter.import_dataframe_from_path_wo_timeconversion(input_log, sep=',')
        dataframe = attributes_filter.filter_df_keeping_specno_activities(dataframe, activity_key="concept:name")
        dataframe = case_filter.filter_on_ncases(dataframe, case_id_glue="case:concept:name")
        # dataframe = case_filter.filter_df_on_case_length(dataframe, case_id_glue="case:concept:name")
        dataframe = csv_import_adapter.convert_timestamp_columns_in_df(dataframe)
        dataframe = dataframe.sort_values('time:timestamp')
        event_log = pandas_df_imp.convert_dataframe_to_event_log(dataframe)
        trace_log = transform.transform_event_log_to_trace_log(event_log)

    def test_autofiltering_dataframe(self):
        input_log = os.path.join(INPUT_DATA_DIR, "running-example.csv")
        dataframe = csv_import_adapter.import_dataframe_from_path_wo_timeconversion(input_log, sep=',')
        dataframe = auto_filter.apply_auto_filter(dataframe)

    def test_filtering_variants(self):
        input_log = os.path.join(INPUT_DATA_DIR, "running-example.csv")
        dataframe = csv_import_adapter.import_dataframe_from_path_wo_timeconversion(input_log, sep=',')
        variants = case_statistics.get_variants_statistics(dataframe)
        chosen_variants = [variants[0]["variant"]]
        dataframe = variants_filter.apply(dataframe, chosen_variants)

    def test_filtering_attr_events(self):
        input_log = os.path.join(INPUT_DATA_DIR, "running-example.csv")
        dataframe = csv_import_adapter.import_dataframe_from_path_wo_timeconversion(input_log, sep=',')
        df1 = attributes_filter.apply_events(dataframe, ["reject request"], parameters={"positive": True})
        df2 = attributes_filter.apply_events(dataframe, ["reject request"], parameters={"positive": False})

    def test_filtering_paths(self):
        input_log = os.path.join(INPUT_DATA_DIR, "running-example.csv")
        dataframe = csv_import_adapter.import_dataframe_from_path(input_log, sep=',')
        df3 = paths_filter.apply(dataframe, [("examine casually", "check ticket")], {"positive": False})
        df3 = paths_filter.apply(dataframe, [("examine casually", "check ticket")], {"positive": True})

    def test_filtering_timeframe(self):
        input_log = os.path.join(INPUT_DATA_DIR, "receipt.csv")
        df = csv_import_adapter.import_dataframe_from_path(input_log, sep=',')
        df1 = timestamp_filter.apply_events(df, "2011-03-09 00:00:00", "2012-01-18 23:59:59")
        df2 = timestamp_filter.filter_traces_intersecting(df, "2011-03-09 00:00:00", "2012-01-18 23:59:59")
        df3 = timestamp_filter.filter_traces_contained(df, "2011-03-09 00:00:00", "2012-01-18 23:59:59")


if __name__ == "__main__":
    unittest.main()
