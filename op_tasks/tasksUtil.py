# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from op_tasks.models import Dataset, Product, OpTask, UserProfile, TaskListItem, Experiment

def appendAllTasks(user):
    """
    This function is responsible for adding all available tasks
    to the indicated user. It respects whether tasks and products
    are active (available) and only associates the correct
    tasking with the product that is applicable.
    
    This is used in at least two places: when the user activiates
    the Free Play achievement, and when a new user is registered
    under All Products.
    """
    userprofile = user.userprofile
    index = userprofile.tasklistitem_set.all().count()
    datasets = Dataset.objects.all()        
    for dataset in datasets:
        products = dataset.product_set.all()
        products = products.filter(is_active=True)
        for product in products:
            tasks = dataset.optask_set.all()
            tasks = tasks.filter(is_active=True)
            for task in tasks:
                newtasklistitem = TaskListItem()
                newtasklistitem.userprofile = userprofile
                newtasklistitem.op_task = task
                newtasklistitem.product = product
                newtasklistitem.index = index
                index = index + 1
                newtasklistitem.task_active = True
                newtasklistitem.save()