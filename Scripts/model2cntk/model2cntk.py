# ==============================================================================
# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root
# for full license information.
# ==============================================================================

import sys
import getopt
import adapter

from unimodel import cntkinstance
from utils import globalconf
from validation import validcore


class CntkModelAssister(object):
    @staticmethod
    def script_conversion(script_path, model_path=None, in_type='Caffe', ex_type='bs', test_dataset=None):
        # try:
        #     adapter_impl = adapter.ADAPTER_DICT[in_type]
        # except KeyError:
        #     sys.stderr.write('Un-implemented platform type\n')
        # cntk_model_desc = adapter_impl.load_description(script_path, model_path)
        # sys.stdout.write('begin export model script into %s format\n' % ex_type)
        # export_path = os.path.dirname(script_path)
        # sys.stdout.write('export %s scripts into %s\n' % (ex_type, export_path))
        # try:
        #     exporter_impl = exporter.EXPORTER_DICT[ex_type](cntk_model_desc)
        # except KeyError:
        #     sys.stderr.write('Un-implemented cntk script type\n')
        # exporter_impl.export_scripts(export_path)
        # sys.stdout.write('finished model exporting\n')
        #
        # cntk_instance = cntkinstance.CntkApiInstance(cntk_model_desc, export_path)
        # if test_dataset is not None:
        #     cntk_instance.eval_model(test_dataset)
        # cntk_instance.export_model(export_path)
        raise AssertionError('Discard for now')

    @staticmethod
    def convert_model(conf):
        try:
            adapter_impl = adapter.ADAPTER_DICT[conf.source_solver.source]
        except KeyError:
            sys.stderr.write('un-implemented platform type\n')
        cntk_model_desc = adapter_impl.load_model(conf)

        instance = cntkinstance.CntkApiInstance(cntk_model_desc, global_conf=conf)
        instance.export_model()

        # valid the network
        validator = validcore.Validator(global_conf=conf, functions=instance.get_functions())
        if validator.val_network():
            validator.activate()

        # default to classification
        evaluator = cntkinstance.Evaluator(global_conf=conf, models=instance.get_model())
        evaluator.eval_model()


if __name__ == '__main__':
    sys.stdout = open('log.txt', 'w')
    try:
        options, args = getopt.getopt(sys.argv[1:], "o:f:", ['option=', 'conf='])
    except getopt.GetoptError:
        sys.stderr.write('incorrect usage of model2cntk command\n')
        sys.exit()

    global_conf = globalconf.load_conf(options[1][1])

    getattr(CntkModelAssister, options[0][1])(global_conf)