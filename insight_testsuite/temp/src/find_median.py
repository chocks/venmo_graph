#!/usr/bin/env python
# coding: utf-8

"""

"""

import json
import sys
import datetime as dt
from copy import deepcopy


class Median(object):

    def __init__(self):
        self.last_processed_timestamp = None
        self.edge_list = []
        self.node_weight = {}

    """
    Calculate median from the given list.
    """
    def calc_median(self, lst):
        sortedLst = sorted(lst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2

        if lstLen % 2:
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0
    """
    Calculate the time difference in seconds btween two time stamp strings
    """
    def seconds_diff(self, ts1, ts2):
        dt1 = dt.datetime.strptime(ts1, "%Y-%m-%dT%H:%M:%SZ")
        dt2 = dt.datetime.strptime(ts2, "%Y-%m-%dT%H:%M:%SZ")
        return (dt2 - dt1).total_seconds()


    def prune_weights(self):
        nodes = deepcopy(self.node_weight)
        for key, val in nodes.iteritems():
            if val == 0:
                self.node_weight.pop(key)

    def prune_edges(self, edge):
        temp_list = deepcopy(self.edge_list)
        for curr_edge in temp_list:
            sec_diff = self.seconds_diff(curr_edge['created_time'], edge['created_time'])
            if sec_diff > 60:
                self.edge_list.remove(curr_edge)
                # Prune weights
                if curr_edge['actor'] in self.node_weight:
                    self.node_weight[curr_edge['actor']] -= 1
                if curr_edge['target'] in self.node_weight:
                    self.node_weight[curr_edge['target']] -= 1
        self.prune_weights()
        self.edge_list.append(edge)

    def calculate_weights(self, edge):
        found_actor = False
        found_target = False
        already_updated = []
        for edge_item in self.edge_list:
            if edge['actor'] == edge_item['actor'] and \
                            edge['target'] == edge_item['target'] and \
                            edge['created_time'] == edge_item['created_time']:
                # This is duplicate entry
                continue
            try:
                if edge['actor'] == edge_item['actor'] or edge['actor'] == edge_item['target']:
                    if edge['actor'] not in already_updated:
                        self.node_weight[edge['actor']] += 1
                    found_actor = True
                    already_updated.append(edge['actor'])
                elif edge['target'] == edge_item['target'] or edge['target'] == edge_item['actor']:
                    if edge['target'] not in already_updated:
                        self.node_weight[edge['target']] += 1
                    found_target = True
                    already_updated.append(edge['target'])
            except KeyError:
                continue

        if found_actor is False:
            self.node_weight[edge['actor']] = 1

        if found_target is False:
            self.node_weight[edge['target']] = 1

    def find_median(self, input_file=None, output_file=None):
        try:
            with open(input_file) as f:
                lines = f.read().splitlines()
            out_file = open(output_file,'w')
        except (OSError, IOError) as e:
            print str(e.errorno)
            return

        for line in lines:
            edge = json.loads(line)
            if self.last_processed_timestamp is not None:
                # Skip out of order and outside the 60 second window
                secs_diff = self.seconds_diff(self.last_processed_timestamp, edge['created_time'])
                if secs_diff < 0 and abs(secs_diff) > 60:
                    m = self.calc_median(self.node_weight.values())
                    out_file.write('%.2f\n' % m)
                    continue
            self.prune_edges(edge)
            self.calculate_weights(edge)
            self.last_processed_timestamp = edge['created_time']
            out_file.write('%.2f\n' % self.calc_median(self.node_weight.values()))
        out_file.close()

if __name__ == '__main__':
    try:
        file_n = sys.argv[1]
        file_o = sys.argv[2]
    except IndexError as inExp:
        print "Usage python find_median.py <input_filename> <output_filename>"
        exit(0)

    median = Median()
    median.find_median(input_file=file_n, output_file=file_o)