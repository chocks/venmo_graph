#!/usr/bin/env python
# coding: utf-8

import json
import sys
import datetime as dt
from copy import deepcopy

__author__ = "Chocks Eswaramurthy"
__version__ = "1.0"
__email__ = "chocks@outlook.com"

class Median(object):

    """
    Median class to calculate the rolling median for a given dataset
    """
    def __init__(self):
        self.last_processed_timestamp = None
        self.edge_list = []
        self.node_weight = {}

    """
    Generic utility to calculate median from the given list.
    :param lst: List of integers to calculate the median
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
    Generic utility to calculate the time difference in seconds btween two time stamp strings. ts2 - ts1 is calcualted.
    :param ts1: Time stamp string 1 to compare
    :param ts2: Time stamp string 2
    """
    def seconds_diff(self, ts1, ts2):
        dt1 = dt.datetime.strptime(ts1, "%Y-%m-%dT%H:%M:%SZ")
        dt2 = dt.datetime.strptime(ts2, "%Y-%m-%dT%H:%M:%SZ")
        return (dt2 - dt1).total_seconds()

    """
    Prune weights for the edges that are already pruned
    """
    def prune_weights(self):
        nodes = deepcopy(self.node_weight)
        for key, val in nodes.iteritems():
            if val == 0:
                self.node_weight.pop(key)

    """
    Prune the edges from the list that don't fit the 60 second time window.
    :param edge: The edge that is currently being processed
    """
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

    """
         The method calculated the weights of the specific nodes. Increment the weights if they are already in the graph
         within the 60 sec time frame window.
         :param edge: The edge that is currently being processed.

    """
    def calculate_weights(self, edge):
        found_actor = False
        found_target = False
        already_updated = [] # List to maintain nodes that are already processed.
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

    """
     Given a input data set, calculates the rolling median for it. The results are populated to the give output file
    :param input_file: The input file that contains the venmo payments data.
    :param output_file: The file to output the results to
    """
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
"""
Main invocation point to run as standalone script
"""
if __name__ == '__main__':
    try:
        file_n = sys.argv[1]
        file_o = sys.argv[2]
    except IndexError as inExp:
        print "Usage python find_median.py <input_filename> <output_filename>"
        exit(0)

    median = Median()
    median.find_median(input_file=file_n, output_file=file_o)