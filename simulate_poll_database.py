#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate Poll Database - This program simulates processing of poll database
process - the first step is to produce product exposure and then customer
exposure

Created on Wed Jun 15 05:56:32 2022

@author: brett
"""

import simpy
import random
import statistics

prod_wait_times = [0]
cust_wait_times = [0]

class PollDB(object):
    def __init__(self, env):
        self.env = env
        self.prodexp = simpy.Resource(env)
        self.custexp = simpy.Resource(env)
                
    def calc_prod_exp(self, product):
        yield self.env.timeout(.2/60)
        
    def calc_cust_exp(self, customers):
        yield self.env.timeout(.02/60)
        
def calc_prod_exposure(env, product, exp_svc):    
    prod_arrival_time = env.now
    
    with exp_svc.prodexp.request() as request:
        yield request
        yield env.process(exp_svc.calc_prod_exp(product))
    prod_wait_times.append(env.now - prod_arrival_time)
        
def calc_cust_exposure(env, customers, exp_svc):
    cust_arrival_time = env.now
    
    with exp_svc.custexp.request() as request:
        yield request
        yield env.process(exp_svc.calc_cust_exp(customers))
     
    cust_wait_times.append(env.now - cust_arrival_time)
    
def run_exp(env):
    exp_svc = PollDB(env)
    # Customer exposure uncomment to make go first 
#    for customers in range(23071):
#        env.process(calc_cust_exposure(env, customers, exp_svc))
#        
#    while True:
#        yield env.timeout(0.20)
#        
#        customers += 1
#        env.process(calc_cust_exposure(env, customers, exp_svc))
        
    # Product exposure
    for product in range(14711):
        env.process(calc_prod_exposure(env, product, exp_svc))
        
    while True:
        yield env.timeout(0.20)
        
        product += 1
        env.process(calc_prod_exposure(env, product, exp_svc))
    # Customer exposure    
    for customers in range(23071):
        env.process(calc_cust_exposure(env, customers, exp_svc))
        
    while True:
        yield env.timeout(0.20)
        
        customers += 1
        env.process(calc_cust_exposure(env, customers, exp_svc))
        
def get_average_prod_wait_time(arrival_times):
    average_prod_wait = statistics.mean(prod_wait_times)
    # pretty print results
    minutes, frac_minutes = divmod(average_prod_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def get_average_cust_wait_time(arrival_times):
    average_cust_wait = statistics.mean(cust_wait_times)
    # pretty print results
    minutes, frac_minutes = divmod(average_cust_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

def main():
  # Setup
  random.seed(42)
  
  # Run the simulation
  env = simpy.Environment()
  env.process(run_exp(env))
  env.run(until=54)

  # View the results
  mins, secs = get_average_prod_wait_time(prod_wait_times)
  print(
      "Running simulation...",
      f"\nThe average product wait time is {mins} minutes and {secs} seconds.",
  )
 
  mins, secs = get_average_cust_wait_time(cust_wait_times)
  print(f"\nThe average customer wait time is {mins} minutes and {secs} seconds.")
       
if __name__ == "__main__":
    main()       
        
