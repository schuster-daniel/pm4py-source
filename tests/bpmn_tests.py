import inspect
import os
import sys

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import os
import unittest

from pm4py.objects.bpmn.importer import bpmn20 as bpmn_importer
from tests.constants import INPUT_DATA_DIR, OUTPUT_DATA_DIR
from pm4py.objects.conversion.bpmn_to_petri import factory as bpmn_to_petri
from pm4py.objects.petri.importer import pnml as petri_importer
from pm4py.objects.conversion.petri_to_bpmn import factory as petri_to_bpmn
from pm4py.objects.bpmn.exporter import bpmn20 as bpmn_exporter
from pm4py.visualization.bpmn import factory as bpmn_vis_factory
from pm4py.objects.log.importer.xes import factory as xes_importer


class BpmnTests(unittest.TestCase):
    def test_bpmn_conversion_to_petri(self):
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        net, initial_marking, final_marking, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_to_petri.apply(
            bpmn_graph)
        del net
        del initial_marking
        del final_marking
        del elements_correspondence
        del inv_elements_correspondence
        del el_corr_keys_map

    def test_petri_conversion_to_bpmn(self):
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.pnml")
        net, initial_marking, final_marking = petri_importer.import_net(obj_path)
        bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = petri_to_bpmn.apply(net, initial_marking, final_marking)
        del bpmn_graph
        del elements_correspondence
        del inv_elements_correspondence
        del el_corr_keys_map

    def test_bpmn_exporting(self):
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        output_path = os.path.join(OUTPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        bpmn_exporter.export_bpmn(bpmn_graph, output_path)
        os.remove(output_path)

    def test_bpmn_simple_vis(self):
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        gviz = bpmn_vis_factory.apply(bpmn_graph, parameters={"format":"svg"})
        del gviz

    def test_bpmn_freqperf_vis_conv(self):
        log = xes_importer.apply(os.path.join(INPUT_DATA_DIR, "running-example.xes"))
        obj_path = os.path.join(INPUT_DATA_DIR, "running-example.bpmn")
        bpmn_graph = bpmn_importer.import_bpmn(obj_path)
        gviz = bpmn_vis_factory.apply_through_conv(bpmn_graph, log=log, variant="frequency")
        del gviz
        gviz = bpmn_vis_factory.apply_through_conv(bpmn_graph, log=log, variant="performance")
        del gviz


if __name__ == "__main__":
    unittest.main()
